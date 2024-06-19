"""Build, publish, scan and sign Docker images."""

import asyncio
import logging
import os
from typing import Annotated, Self

import dagger
from dagger import Arg, Doc, dag, field, function, object_type
from dagger.log import configure_logging

configure_logging(logging.INFO)


@object_type
class Docker:
    """Docker module"""

    container: Annotated[list[dagger.Container], Doc("Image address.")] = field(default=list)
    digest: Annotated[str, Doc("Image digest.")] = field(default="")

    @function(name="import")
    def import_(
        self,
        address: Annotated[str, Doc("Image's address from its registry.")],
    ) -> dagger.Container:
        """Import a Doker image"""
        return dag.container().from_(address=address)

    @function
    async def apko(
        self,
        context: Annotated[dagger.Directory, Doc("Context directory.")],
        config: Annotated[str, Doc("Config file.")] = "apko.yaml",
        arch: Annotated[str, Doc("Architectures to build.")] | None = None,
        image: Annotated[str, Doc("apko Docker image.")] = "chainguard/apko:latest",
    ) -> Self:
        """Build multi-platform image using Chainguard apko tool (apk-based OCI image builder)."""
        platform_variants: list[dagger.Container] = []
        apko = dag.container().from_(image)
        builder = (
            dag.container()
            .from_("chainguard/bash:latest")
            .with_user("nonroot")
            .with_mounted_directory(path="/work", source=context, owner="nonroot")
            .with_workdir(f"/work/{os.path.dirname(config)}")
            .with_file(path="/bin/apko", source=apko.file(path="/usr/bin/apko"))
            .with_entrypoint(["/bin/apko"])
        )

        async def apko_(arch: str = "host"):
            container: dagger.Container
            output_tar = "/home/nonroot/image.tar"
            cmd = ["build", "--arch", arch, os.path.basename(config), "image:latest", output_tar]
            tarball = await builder.with_exec(cmd).file(path=output_tar)
            if arch == "host":
                container = dag.container()
            else:
                platform = dagger.Platform(f"linux/{arch}")
                container = dag.container(platform=platform)
            platform_variants.append(container.import_(source=tarball))

        if arch:
            async with asyncio.TaskGroup() as tg:
                for arch_ in arch.split(","):
                    tg.create_task(apko_(arch=arch_))
        else:
            await apko_()

        self.container = platform_variants
        return self

    @function
    async def build(
        self,
        context: Annotated[dagger.Directory, Doc("Directory context used by the Dockerfile.")],
        dockerfile: Annotated[str, Doc("Path to the Dockerfile to use.")] = "Dockerfile",
        platform: Annotated[str, Doc("Platforms to initialize the container with.")] | None = None,
        target: Annotated[str, Doc("Target build stage to build.")] = "",
    ) -> Self:
        """Build multi-platform image using Dockerfile."""
        platform_variants: list[dagger.Container] = []

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
            platform_variants.append(container)

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
            platform_variants.append(
                dag.container().build(
                    context=context,
                    dockerfile=dockerfile,
                    target=target,
                )
            )
        self.container = platform_variants
        return self

    @function
    async def scan(
        self,
        container: Annotated[dagger.Container, Doc("Image to scan.")] | None = None,
        fail_on: (
            Annotated[
                str,
                Doc("Set the return code to 1 if a vulnerability is found with a severity >= the given severity"),
            ]
            | None
        ) = None,
        output_format: Annotated[str, Doc("Report output formatter.")] = "table",
        image: Annotated[str, Doc("Grype Docker image.")] = "chainguard/grype:latest",
    ) -> str:
        """Scan image with Grype and return the formatted report"""
        user = "nonroot"
        cache_dir: str = "/home/nonroot/.grype/cache"
        image_tar = "/home/nonroot/image.tar"

        cmd = [image_tar, "--output", output_format]
        if fail_on:
            cmd.extend(["--fail-on", fail_on])

        if not container:
            container = self.container[0]

        return await (
            dag.container()
            .from_(image)
            .with_user(user)
            .with_env_variable("GRYPE_DB_CACHE_DIR", cache_dir)
            .with_mounted_cache(
                cache_dir,
                dag.cache_volume("GRYPE_DB_CACHE"),
                sharing=dagger.CacheSharingMode("LOCKED"),
                owner=user,
            )
            .with_file(path=image_tar, source=container.as_tarball(), owner=user)
            .with_exec(cmd)
            .stdout()
        )

    @function
    async def export(
        self,
        platform_variants: (
            Annotated[list[dagger.Container], Doc("Identifiers for other platform specific containers.")] | None
        ) = None,
        compress: Annotated[bool, Doc("Enable compression.")] | None = False,
    ) -> dagger.File:
        """Export image as tarball."""
        if not platform_variants:
            platform_variants = self.container
        forced_compression = dagger.ImageLayerCompression("Uncompressed")
        if compress:
            forced_compression = dagger.ImageLayerCompression("Gzip")
        return dag.container().as_tarball(forced_compression=forced_compression, platform_variants=platform_variants)

    @function
    async def publish(
        self,
        addresses: Annotated[tuple[str, ...], Arg(name="address")],
        platform_variants: (
            Annotated[list[dagger.Container], Doc("Identifiers for other platform specific containers.")] | None
        ) = None,
        username: Annotated[str, Doc("Registry username.")] | None = None,
        password: Annotated[dagger.Secret, Doc("Registry password.")] | None = None,
    ) -> str:
        """Publish multi-platform image."""
        digest: str = ""

        if not platform_variants:
            platform_variants = self.container

        for address in addresses:
            container = dag.container()
            if username and password:
                container = container.with_registry_auth(address=address, username=username, secret=password)
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
        image: Annotated[str, Doc("Cosign Docker image.")] = "chainguard/cosign:latest",
    ) -> str:
        """Sign multi-platform image with Cosign."""
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
            container = container.with_mounted_file("/home/nonroot/.docker/config.json", docker_config, owner=user)

        return await container.stdout()
