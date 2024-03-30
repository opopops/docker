#!/usr/bin/env bash

#set -x
set -ueo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

dagger call release \
    --src=${SCRIPT_DIR}/../opopops \
    --registry="docker.io/opopops" \
    --docker-config="${HOME}/.docker/config.json" \
    --username="opopops" \
    --password=env:O5S_REGISTRY_TOKEN \
    --platforms="linux/amd64,linux/arm64" \
    --sign \
    --cosign-password=env:O5S_COSIGN_PASSWORD \
    --cosign-private-key=env:O5S_COSIGN_PRIVATE_KEY $@
