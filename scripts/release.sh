#!/usr/bin/env bash

#set -x
set -ueo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

dagger call release \
    --src=${SCRIPT_DIR}/../opopops \
    --registry="index.docker.io/opopops" \
    --docker-config="${HOME}/.docker/config.json" \
    --registry-username="opopops" \
    --registry-password=env:O5S_REGISTRY_TOKEN \
    --sign \
    --cosign-password=env:O5S_COSIGN_PASSWORD \
    --cosign-private-key=env:O5S_COSIGN_PRIVATE_KEY $@
