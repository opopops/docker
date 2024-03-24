"""Dagger module"""

from typing import Annotated, Self

import os
import logging

import dagger
from dagger import Doc, dag, function, object_type
from dagger.log import configure_logging

configure_logging(logging.INFO)


@object_type
class Docker:
    """Docker module"""

    platform_variants: tuple[dagger.Container, ...] = ()
    digest: str = ""

    @function
    def container(
        self,
        address: Annotated[str, Doc("Image's address from its registry.")],
    ) -> dagger.Container:
        """Return a container from registry"""
        return dag.container().from_(address=address)

    @function(name="import")
    def import_(
        self,
        address: Annotated[str, Doc("Image's address from its registry.")],
    ) -> Self:
        """Import a container from registry"""
        self.platform_variants = tuple([dag.container().from_(address=address)])
        return self

    @function
    async def build(
        self,
        context: Annotated[dagger.Directory, Doc("Directory context used by the Dockerfile.")],
        dockerfile: Annotated[str, Doc("Path to the Dockerfile to use.")] = "Dockerfile",
        platforms: Annotated[
            str, Doc("Platforms to initialize the container with.")
        ] = "linux/amd64,linux/arm64",
        target: Annotated[str, Doc("Target build stage to build.")] | None = "",
    ) -> Self:
        """Build multi-platform containers"""
        containers: list[dagger.Container] = []
        dagger_platforms = [dagger.Platform(platform) for platform in platforms.split(",")]
        for platform in dagger_platforms:
            container = dag.container(platform=platform).build(
                context=context, dockerfile=dockerfile, target=target
            )
            containers.append(container)
        self.platform_variants = tuple(containers)
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
    ) -> str:
        """Return Grype scan report"""
        user = "nonroot"
        cache_dir: str = "/home/nonroot/.grype/cache"
        image_tar = "/home/nonroot/image.tar"

        cmd = [image_tar, "--output", output_format]
        if fail_on:
            cmd.extend(["--fail-on", fail_on])

        if not container:
            container = self.platform_variants[0]

        return await (
            dag.container()
            .from_("chainguard/grype:latest")
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
    ) -> Self:
        """Scan container using Grype"""
        await self.scan_report(container=container, fail_on=fail_on)
        return self

    @function
    async def publish(
        self,
        address: str,
        platform_variants: tuple[dagger.Container, ...] | None = None,
        registry_username: str | None = None,
        registry_password: dagger.Secret | None = None,
    ) -> str:
        """Publish container"""
        if not platform_variants:
            platform_variants = self.platform_variants

        container = dag.container()
        if registry_username and registry_password:
            container = container.with_registry_auth(
                address=address, username=registry_username, secret=registry_password
            )
        digest = await container.publish(address=address, platform_variants=platform_variants)
        self.digest = digest
        return digest

    @function
    async def sign(
        self,
        private_key: dagger.Secret,
        password: dagger.Secret,
        digest: str | None = None,
        registry_username: str | None = None,
        registry_password: dagger.Secret | None = None,
        docker_config: dagger.File | None = None,
    ) -> str:
        """Sign Docker image"""
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
            .from_("chainguard/cosign:latest")
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

    @function
    async def release(
        self,
        src: dagger.Directory,
        registry: str,
        cosign_password: dagger.Secret | None,
        cosign_private_key: dagger.Secret | None,
        registry_username: str | None = None,
        registry_password: dagger.Secret | None = None,
        docker_config: dagger.File | None = None,
        sign: bool | None = False,
        scan: bool | None = False,
        fail_on: str | None = "critical",
    ) -> list[str]:
        """Release Docker images"""
        digests: list[str] = []
        dockerfiles = await src.glob("**/Dockerfile")
        for dockerfile in dockerfiles:
            repository = os.path.dirname(dockerfile)
            context = src.directory(repository)
            await self.build(context=context)
            if scan:
                await self.scan(fail_on=fail_on)
            digest = await self.publish(
                address=f"{registry}/{repository}:latest",
                registry_username=registry_username,
                registry_password=registry_password,
            )
            if sign:
                await self.sign(
                    digest=digest,
                    password=cosign_password,
                    private_key=cosign_private_key,
                    registry_username=registry_username,
                    registry_password=registry_password,
                    docker_config=docker_config,
                )
            digests.append(digest)
        return digests
