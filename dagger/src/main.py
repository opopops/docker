"""Dagger module"""

from typing import Annotated, Self

import logging
import asyncio

import dagger
from dagger import Arg, Doc, dag, field, function, object_type
from dagger.log import configure_logging

configure_logging(logging.INFO)


@object_type
class Docker:
    """Docker module"""

    containers: Annotated[tuple[dagger.Container, ...], Doc("Container to use.")] = field(
        name="container", default=()
    )
    digest: str = ""

    @function(name="import")
    def import_(
        self,
        address: Annotated[str, Doc("Image's address from its registry.")],
    ) -> dagger.Container:
        """Import a Doker image"""
        if not address:
            return self.containers[0]
        return dag.container().from_(address=address)

    @function
    async def apko(
        self,
        context: Annotated[dagger.Directory, Doc("Directory context used by apko.")],
        config: Annotated[str, Doc("apko config file.")] = "apko.yaml",
        arch: Annotated[str, Doc("Architectures to build.")] | None = None,
        image: Annotated[str, Doc("apko Docker image.")] | None = "chainguard/apko:latest",
    ) -> Self:
        """Build a container using apko"""
        containers: list[dagger.Container] = []
        apko = dag.container().from_(image)
        builder = (
            dag.container()
            .from_("chainguard/bash:latest")
            .with_user("nonroot")
            .with_mounted_directory(path="/apko", source=context, owner="nonroot")
            .with_workdir("/apko")
            .with_file(path="/bin/apko", source=apko.file(path="/usr/bin/apko"))
            .with_entrypoint(["/bin/apko"])
        )

        async def apko_(arch: str = "host"):
            container: dagger.Container
            output_tar = "/home/nonroot/image.tar"
            cmd = ["build", "--arch", arch, config, "image:latest", output_tar]
            tarball = await builder.with_exec(cmd).file(path=output_tar)
            if arch == "host":
                container = dag.container()
            else:
                platform = dagger.Platform(f"linux/{arch}")
                container = dag.container(platform=platform)
            containers.append(container.import_(source=tarball))

        if arch:
            async with asyncio.TaskGroup() as tg:
                for arch_ in arch.split(","):
                    tg.create_task(apko_(arch=arch_))
        else:
            await apko_()

        self.containers = tuple(containers)
        return self

    @function
    async def build(
        self,
        context: Annotated[dagger.Directory, Doc("Directory context used by the Dockerfile.")],
        dockerfile: Annotated[str, Doc("Path to the Dockerfile to use.")] = "Dockerfile",
        platform: Annotated[str, Doc("Platforms to initialize the container with.")] | None = None,
        target: Annotated[str, Doc("Target build stage to build.")] = "",
    ) -> Self:
        """Build a container using Dockerfile"""
        containers: list[dagger.Container] = []

        async def build_(
            container: dagger.Container,
            context: dagger.Directory,
            dockerfile: str,
            target: str,
        ):
            container = await container.build(
                context=context,
                dockerfile=dockerfile,
                target=target,
            )
            containers.append(container)

        if platform:
            platforms = [dagger.Platform(platform) for platform in platform.split(",")]
            async with asyncio.TaskGroup() as tg:
                for platform in platforms:
                    tg.create_task(
                        build_(
                            container=dag.container(platform=platform),
                            context=context,
                            dockerfile=dockerfile,
                            target=target,
                        )
                    )
        else:
            containers.append(
                dag.container().build(
                    context=context,
                    dockerfile=dockerfile,
                    target=target,
                )
            )
        self.containers = tuple(containers)
        return self

    @function
    async def scan_report(
        self,
        container: Annotated[dagger.Container, Doc("Container to scan.")] | None = None,
        fail_on: (
            Annotated[
                str,
                Doc(
                    "Set the return code to 1 if a vulnerability is found with a severity >= the given severity"
                ),
            ]
            | None
        ) = None,
        output_format: Annotated[str, Doc("Report output formatter.")] | None = "table",
        image: Annotated[str, Doc("Grype Docker image.")] | None = "chainguard/grype:latest",
    ) -> str:
        """Scan a container using Grype and return the formatted report"""
        user = "nonroot"
        cache_dir: str = "/home/nonroot/.grype/cache"
        image_tar = "/home/nonroot/image.tar"

        cmd = [image_tar, "--output", output_format]
        if fail_on:
            cmd.extend(["--fail-on", fail_on])

        if not container:
            container = self.containers[0]

        return await (
            dag.container()
            .from_(image)
            .with_user(user)
            .with_env_variable("GRYPE_DB_CACHE_DIR", cache_dir)
            .with_mounted_cache(cache_dir, dag.cache_volume("grype"), owner=user)
            .with_file(path=image_tar, source=container.as_tarball(), owner=user)
            .with_exec(cmd)
            .stdout()
        )

    @function
    async def scan(
        self,
        container: Annotated[dagger.Container, Doc("Container to scan.")] | None = None,
        fail_on: (
            Annotated[
                str,
                Doc(
                    "Set the return code to 1 if a vulnerability is found with a severity >= the given severity"
                ),
            ]
            | None
        ) = "critical",
        image: Annotated[str, Doc("Grype Docker image.")] | None = "chainguard/grype:latest",
    ) -> Self:
        """Scan a container using Grype"""
        await self.scan_report(container=container, fail_on=fail_on, image=image)
        return self

    @function
    async def export(
        self,
        platform_variants: tuple[dagger.Container, ...] | None = None,
        compress: bool | None = False,
    ) -> dagger.File:
        """Export container"""
        if not platform_variants:
            platform_variants = self.containers
        forced_compression = dagger.ImageLayerCompression("Uncompressed")
        if compress:
            forced_compression = dagger.ImageLayerCompression("Gzip")
        return dag.container().as_tarball(
            forced_compression=forced_compression, platform_variants=platform_variants
        )

    @function
    async def publish(
        self,
        addresses: Annotated[tuple[str, ...], Arg(name="address")],
        platform_variants: tuple[dagger.Container, ...] | None = None,
        username: str | None = None,
        password: dagger.Secret | None = None,
    ) -> str:
        """Publish container"""
        digest: str = ""

        if not platform_variants:
            platform_variants = self.containers

        for address in addresses:
            container = dag.container()
            if username and password:
                container = container.with_registry_auth(
                    address=address, username=username, secret=password
                )
            digest_ = await container.publish(address=address, platform_variants=platform_variants)
            if not digest:
                digest = digest_
                self.digest = digest
        return digest

    @function
    async def sign(
        self,
        private_key: Annotated[dagger.Secret, Doc("Cosign private key.")],
        password: Annotated[dagger.Secret, Doc("Cosign password.")],
        digest: Annotated[str, Doc("Docker image digest.")] | None = None,
        registry_username: Annotated[str, Doc("Registry username.")] | None = None,
        registry_password: Annotated[dagger.Secret, Doc("Registry password.")] | None = None,
        docker_config: Annotated[dagger.File, Doc("Docker config.")] | None = None,
        image: Annotated[str, Doc("Cosign Docker image.")] | None = "chainguard/cosign:latest",
    ) -> str:
        """Sign container"""
        user = "nonroot"

        if not digest:
            digest = self.digest

        cmd = ["sign", digest, "--key", "env://COSIGN_PRIVATE_KEY"]

        if registry_username and registry_password:
            cmd.extend(
                [
                    "--registry-username",
                    registry_username,
                    "--registry-password",
                    await registry_password.plaintext(),
                ]
            )

        container = (
            dag.container()
            .from_(image)
            .with_user(user)
            .with_env_variable("COSIGN_YES", "true")
            .with_secret_variable("COSIGN_PASSWORD", password)
            .with_secret_variable("COSIGN_PRIVATE_KEY", private_key)
            .with_exec(cmd)
        )

        if docker_config:
            container = container.with_mounted_file(
                "/home/nonroot/.docker/config.json", docker_config, owner=user
            )

        return await container.stdout()
