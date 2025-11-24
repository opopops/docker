# syntax=docker/dockerfile:1

ARG WOLFI_VERSION="latest"
ARG CODE_SERVER_VERSION="latest"

FROM --platform=$BUILDPLATFORM cgr.dev/chainguard/wolfi-base:${WOLFI_VERSION} AS base

ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

RUN apk add --no-cache \
    curl \
    gzip \
    unzip

FROM base AS helmfile

# --- Install helmfile CLI
ARG HELMFILE_VERSION="1.2.1"
ENV HELMFILE_VERSION=$HELMFILE_VERSION
RUN curl -fsSL https://github.com/helmfile/helmfile/releases/download/v${HELMFILE_VERSION}/helmfile_${HELMFILE_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/bin helmfile && \
    chmod 755 /usr/bin/helmfile

USER 65532

FROM base AS terraform

# --- Install terraform CLI
ARG TERRAFORM_VERSION="1.14.0"
ENV TERRAFORM_VERSION=$TERRAFORM_VERSION
RUN TEMP_DIR=$(mktemp -d) && \
    curl -fsSL https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_${TARGETOS}_${TARGETARCH}.zip \
        -o ${TEMP_DIR}/terraform.zip && \
    unzip -d $TEMP_DIR ${TEMP_DIR}/terraform.zip  && \
    mv ${TEMP_DIR}/terraform /usr/bin/terraform && \
    chmod 755 /usr/bin/terraform && \
    rm -rf ${TEMP_DIR}

USER 65532

FROM base AS vault

# --- Install vault CLI
ARG VAULT_VERSION="1.21.1"
ENV VAULT_VERSION=$VAULT_VERSION
RUN TEMP_DIR=$(mktemp -d) && \
    curl -fsSL https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_${TARGETOS}_${TARGETARCH}.zip \
    -o ${TEMP_DIR}/vault.zip && \
    unzip -d $TEMP_DIR ${TEMP_DIR}/vault.zip  && \
    mv ${TEMP_DIR}/vault /usr/bin/vault && \
    chmod 755 /usr/bin/vault && \
    rm -rf ${TEMP_DIR}

USER 65532

FROM cgr.dev/chainguard/wolfi-base:${WOLFI_VERSION} AS prod

LABEL org.opencontainers.image.authors="opopops"
LABEL org.opencontainers.image.title="iac"
LABEL org.opencontainers.image.source="https://github.com/opopops/docker/tree/main/images/iac"
LABEL org.opencontainers.image.description="IaC image"

USER root

RUN apk add --no-cache \
    aws-cli-v2 \
    bash \
    bind-tools \
    busybox \
    cosign \
    crane \
    curl \
    grype \
    helm \
    jq \
    k9s \
    kubectl \
    openssl \
    opentofu \
    python-3.13 \
    py3.13-ansible-core \
    tzdata \
    vim \
    yq

# --- Install binaries
COPY --link --from=helmfile /usr/bin/helmfile /usr/bin/helmfile
COPY --link --from=terraform /usr/bin/terraform /usr/bin/terraform
COPY --link --from=vault /usr/bin/vault /usr/bin/vault

USER 65532
