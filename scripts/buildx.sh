#!/usr/bin/env bash

#set -x
set -ueo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BUILDX_ARGS=""
BUILDX_PRUNE="false"
BUILDX_BUILDER_NAME="${BUILDX_BUILDER_NAME:-opopops}"
BUILDX_BUILDER_PLATFORM="${BUILDX_BUILDER_PLATFORM:-linux/amd64,linux/arm64}"
BUILDX_PRUNE_FILTER="${BUILDX_PRUNE_FILTER:-until=72h}"
BUILDX_PRUNE_KEEP_STORAGE="${BUILDX_PRUNE_KEEP_STORAGE:-10gb}"

function _exit() {
  if [[ "$BUILDX_PRUNE" == "true" ]]; then
    docker buildx prune \
      --builder="$BUILDX_BUILDER_NAME" \
      --force \
      --filter="$BUILDX_PRUNE_FILTER" \
      --keep-storage="$BUILDX_PRUNE_KEEP_STORAGE"
  fi
}

function usage() {
  cat <<USAGE

Usage:
    $(basename $0) [OPTIONS] <context>

Description:
    Build Docker image using BuildX

OPTIONS:
    --builder <string>
        Override the configured builder instance (default "$BUILDX_BUILDER_NAME")

    --platform <string>
        Set target platform for build (format: "linux/amd64,linux/arm64")

    --load
        Load image

    --push
        Push image to the registry

    --prune
        Remove build cache

    --tag <string>
        Name and optionally a tag

    -h | --help
        Display this help message
USAGE
}

while (("$#")); do
  case "$1" in
  --builder)
    BUILDX_BUILDER_NAME="$2"
    shift 2
    ;;
  --load | --push)
    BUILDX_ARGS+=" $1"
    shift
    ;;
  --platform | --tag)
    BUILDX_ARGS+=" $1=$2"
    shift 2
    ;;
  --prune)
    BUILDX_PRUNE="true"
    shift
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
docker buildx create \
  --platform="$BUILDX_BUILDER_PLATFORM" \
  --name="$BUILDX_BUILDER_NAME" 2>/dev/null
set -e

trap _exit EXIT

docker buildx build \
  --builder=$BUILDX_BUILDER_NAME \
  $BUILDX_ARGS $BUILDX_CONTEXT
