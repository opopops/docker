#!/usr/bin/env bash

#set -x
set -ueo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BUILDX_ARGS=""
BUILDX_PRUNE="false"
BUILDX_BUILDER_NAME="${BUILDX_BUILDER_NAME:-opopops}"
BUILDX_PRUNE_FILTER="${BUILDX_PRUNE_FILTER:-until=72h}"
BUILDX_PRUNE_KEEP_STORAGE="${BUILDX_PRUNE_KEEP_STORAGE:-5gb}"


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

    --build-arg <key=value>
        Set build args

    --platform <string>
        Set target platform for build (format: "linux/amd64,linux/arm64")

    --tag
        Set image tag

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
  --build-arg | --platform | --tag)
    BUILDX_ARGS+=" $1=$2"
    shift 2
    ;;
  --load | --push)
    BUILDX_ARGS+=" $1"
    shift
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

if [[ -z "$BUILDX_CONTEXT" ]]; then
  echo "ERROR: you must specify a context"
  exit 1
fi

set +e
docker buildx create \
  --name="$BUILDX_BUILDER_NAME" 2>/dev/null
set -e

trap _exit EXIT

docker buildx build \
  --builder=$BUILDX_BUILDER_NAME \
  $BUILDX_ARGS $BUILDX_CONTEXT
