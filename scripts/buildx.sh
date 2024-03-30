#!/usr/bin/env bash

#set -x
set -ueo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

REGISTRY="docker.io/opopops"

BUILDX_ARGS=""
BUILDX_BUILDER_NAME="opopops"
BUILDX_BUILDER_PLATFORM="linux/amd64,linux/arm64"

function _exit() {
  docker buildx prune \
    --force \
    --builder="$BUILDX_BUILDER_NAME" \
    --filter="until=48h" \
    --keep-storage="2gb"
}

function usage() {
  cat <<USAGE

Usage:
    $(basename $0) [OPTIONS] <context>

Description:
    Build Docker image using BuildX

OPTIONS:
    --platform <string>
        Set target platform for build (format: "linux/amd64,linux/arm64")

    --load
        Load image

    --push
        Push image to the registry

    --tag <string>
        Name and optionally a tag

    -h | --help
        Display this help message
USAGE
}

while (("$#")); do
  case "$1" in
  --load | --push)
    BUILDX_ARGS+=" $1"
    shift
    ;;
  --platform | --tag)
    BUILDX_ARGS+=" $1=\"$2\""
    shift 2
    ;;
  -h | --help)
    usage
    exit 0
    ;;
  *) # positional argument
    BUILDX_CONTEXT=$1
    shift
    break
    ;;
  esac
done

set +e
docker buildx use $BUILDX_BUILDER_NAME 2>/dev/null
if [[ $? -ne 0 ]];then
  set -e
  docker buildx create \
    --use \
    --platform="$BUILDX_BUILDER_PLATFORM" \
    --name="$BUILDX_BUILDER_NAME"
fi

trap _exit EXIT

docker buildx build \
  $BUILDX_ARGS $BUILDX_CONTEXT
