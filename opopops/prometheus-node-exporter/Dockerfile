# syntax=docker/dockerfile:1

ARG WOLFI_VERSION="latest"

FROM cgr.dev/chainguard/wolfi-base:${WOLFI_VERSION}

LABEL org.opencontainers.image.authors="opopops"
LABEL org.opencontainers.image.source="https://github.com/opopops/docker"
LABEL org.opencontainers.image.description="Prometheus node-exporter image based on Wolfi OS"

USER root

RUN apk add --no-cache \
    prometheus-node-exporter

USER 65532
