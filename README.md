# Opopops Docker library

A set of applications provided by opopops

## Dagger

This repository provides a Docker dagger module and allows you to execute the following functions:

- Run a container in a terminal (Just For fun):

```shell
dagger -m github.com/opopops/daggerverse/docker@main \
  call import --address=chainguard/wolfi-base terminal
```

- Build a container using [apko](https://github.com/chainguard-dev/apko) and export it as tarball on the host filesystem:

```shell
dagger -m github.com/opopops/daggerverse/docker@main \
  call apko --context="." --config="apko.yml" \
    export --output=<path>
```

- Build a multi-platform container unsing [apko](https://github.com/chainguard-dev/apko) and publish it:

```shell
dagger -m github.com/opopops/daggerverse/docker@main \
  call apko --arch="x86_64,arm64" --context="." --config="apko.yml" \
    publish --address=<image>
```

- Build a container and export it as tarball on the host filesystem:

```shell
dagger -m github.com/opopops/daggerverse/docker@main \
  call build --context="." --dockerfile="Dockerfile" \
    export --output=<path>
```

- Build a multi-platform container and publish it:

```shell
dagger -m github.com/opopops/daggerverse/docker@main \
  call build --platform="linux/amd64,linux/arm64" --context="." --dockerfile="Dockerfile" \
    publish --address=<image>
```

- Build a multi-platform container, publish and sign it:

```shell
dagger -m github.com/opopops/daggerverse/docker@main \
  call build --platform="linux/amd64,linux/arm64" --context="." --dockerfile="Dockerfile" \
    publish --address=<image> \
    sign --private-key=env:COSIGN_PRIVATE_KEY --password=env:COSIGN_PASSWORD --registry-username=<username> --registry-password=env:REGISTRY_PASSWORD
```

- Build a container and scan it using `grype`:

```shell
dagger -m github.com/opopops/daggerverse/docker@main call \
  build \
    --context="." \
    --file="Dockerfile" \
    --platform="linux/amd64,linux/arm64" \
  scan \
    --fail-on=high

# Generate a JSON report
dagger -m github.com/opopops/daggerverse/docker@main call \
  build \
    --context="." \
    --file="Dockerfile" \
    --platform="linux/amd64,linux/arm64" \
  scan \
    --output-format=json

# Generate a JSON report and write it to /tmp/grype.json
dagger -m github.com/opopops/daggerverse/docker@main call \
  build \
    --context="." \
    --file="Dockerfile" \
    --platform="linux/amd64,linux/arm64" \
  scan \
    --output-format=json \
    --output=/tmp/grype.json
```

- Import a container and scan it using `grype`:

```shell
dagger -m github.com/opopops/daggerverse/docker@main call \
  --container=alpine:latest scan
```
