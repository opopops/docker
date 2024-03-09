#!/usr/bin/env bash

#set -x
set -ueo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

NAMESPACE="opopops"
BUILDX_BUILDER_NAME="$NAMESPACE"
BUILDX_PLATFORM="linux/amd64,linux/arm64"

function _exit() {
  docker buildx rm --force $BUILDX_BUILDER_NAME
}

docker buildx create \
  --use \
  --platform $BUILDX_PLATFORM \
  --name $BUILDX_BUILDER_NAME
trap _exit EXIT
docker buildx build \
  --push \
  --platform $BUILDX_PLATFORM \
  --tag ${NAMESPACE}/$1:latest \
  --file $1/Dockerfile $1
