# syntax=docker/dockerfile:1

ARG WOLFI_VERSION="latest"

FROM chainguard/bash:${WOLFI_VERSION}

LABEL org.opencontainers.image.authors="opopops"

USER root

RUN apk add --no-cache \
    bash \
    bind-tools \
    curl \
    jq \
    nano \
    tree \
    tzdata \
    unzip \
    vim \
    yq

USER nonroot
