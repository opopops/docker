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

FROM base AS kubectl

# --- Install kubectl CLI
ARG KUBECTL_VERSION="v1.30.5"
ENV KUBECTL_VERSION $KUBECTL_VERSION
RUN curl -fsSL https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/${TARGETOS}/${TARGETARCH}/kubectl \
    -o /usr/bin/kubectl && \
    chmod 755 /usr/bin/kubectl

USER 65532

FROM base AS k9s

# --- Install k9s CLI
ARG K9S_VERSION="v0.32.5"
ENV K9S_VERSION $K9S_VERSION
RUN curl -fsSL https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/bin k9s && \
    chmod 755 /usr/bin/k9s

USER 65532

FROM base AS helm

# --- Install helm CLI
ARG HELM_VERSION="v3.16.2"
ENV HELM_VERSION $HELM_VERSION
RUN curl -fsSL https://get.helm.sh/helm-${HELM_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz | \
    tar xvzf - --strip-components=1 -C /usr/bin ${TARGETOS}-${TARGETARCH}/helm && \
    chmod 755 /usr/bin/helm

USER 65532

FROM base AS helmfile

# --- Install helmfile CLI
ARG HELMFILE_VERSION="0.169.1"
ENV HELMFILE_VERSION $HELMFILE_VERSION
RUN curl -fsSL https://github.com/helmfile/helmfile/releases/download/v${HELMFILE_VERSION}/helmfile_${HELMFILE_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/bin helmfile && \
    chmod 755 /usr/bin/helmfile

USER 65532

FROM base AS terraform

# --- Install terraform CLI
ARG TERRAFORM_VERSION="1.9.8"
ENV TERRAFORM_VERSION $TERRAFORM_VERSION
RUN TEMP_DIR=$(mktemp -d) && \
    curl -fsSL https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_${TARGETOS}_${TARGETARCH}.zip \
        -o ${TEMP_DIR}/terraform.zip && \
    unzip -d $TEMP_DIR ${TEMP_DIR}/terraform.zip  && \
    mv ${TEMP_DIR}/terraform /usr/bin/terraform && \
    chmod 755 /usr/bin/terraform && \
    rm -rf ${TEMP_DIR}

USER 65532

FROM base AS tofu

# --- Install tofu CLI
ARG TOFU_VERSION="1.8.4"
ENV TOFU_VERSION $TOFU_VERSION
RUN curl -fsSL https://github.com/opentofu/opentofu/releases/download/v${TOFU_VERSION}/tofu_${TOFU_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/bin tofu && \
    chmod 755 /usr/bin/tofu

USER 65532

FROM base AS terragrunt

# --- Install terragrunt CLI
ARG TERRAGRUNT_VERSION="0.68.4"
ENV TERRAGRUNT_VERSION $TERRAGRUNT_VERSION
RUN curl -fsSL https://github.com/gruntwork-io/terragrunt/releases/download/v${TERRAGRUNT_VERSION}/terragrunt_${TARGETOS}_${TARGETARCH} \
    -o /usr/bin/terragrunt && \
    chmod 755 /usr/bin/terragrunt

USER 65532

FROM base AS vault

# --- Install vault CLI
ARG VAULT_VERSION="1.18.0"
ENV VAULT_VERSION $VAULT_VERSION
RUN TEMP_DIR=$(mktemp -d) && \
    curl -fsSL https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_${TARGETOS}_${TARGETARCH}.zip \
    -o ${TEMP_DIR}/vault.zip && \
    unzip -d $TEMP_DIR ${TEMP_DIR}/vault.zip  && \
    mv ${TEMP_DIR}/vault /usr/bin/vault && \
    chmod 755 /usr/bin/vault && \
    rm -rf ${TEMP_DIR}

USER 65532

FROM base AS doctl

# --- Install doctl CLI
ARG DOCTL_VERSION="1.117.0"
ENV DOCTL_VERSION $DOCTL_VERSION
RUN curl -fsSL https://github.com/digitalocean/doctl/releases/download/v${DOCTL_VERSION}/doctl-${DOCTL_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/bin doctl && \
    chmod 755 /usr/bin/doctl

USER 65532

FROM base AS dagger

# --- Install dagger CLI
ARG DAGGER_VERSION="0.13.6"
ENV DAGGER_VERSION $DAGGER_VERSION
RUN curl -fsSL https://github.com/dagger/dagger/releases/download/v${DAGGER_VERSION}/dagger_v${DAGGER_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/bin dagger && \
    chmod 755 /usr/bin/dagger

FROM cgr.dev/chainguard/wolfi-base:${WOLFI_VERSION}

LABEL org.opencontainers.image.authors="opopops"

USER root

RUN apk add --no-cache \
    aws-cli-v2 \
    bash \
    bind-tools \
    cosign \
    curl \
    grype \
    jq \
    nano \
    python-3.12 \
    py3.12-pip \
    tzdata \
    vim \
    yq

# --- Install binaries
COPY --link --from=dagger /usr/bin/dagger /usr/bin/dagger
COPY --link --from=doctl /usr/bin/doctl /usr/bin/doctl
COPY --link --from=helm /usr/bin/helm /usr/bin/helm
COPY --link --from=helmfile /usr/bin/helmfile /usr/bin/helmfile
COPY --link --from=k9s /usr/bin/k9s /usr/bin/k9s
COPY --link --from=kubectl /usr/bin/kubectl /usr/bin/kubectl
COPY --link --from=terraform /usr/bin/terraform /usr/bin/terraform
COPY --link --from=terragrunt /usr/bin/terragrunt /usr/bin/terragrunt
COPY --link --from=tofu /usr/bin/tofu /usr/bin/tofu
COPY --link --from=vault /usr/bin/vault /usr/bin/vault

# --- Install pipx
RUN mkdir -p /usr/local/bin
ARG PIPX_BIN_DIR=/usr/local/bin
ARG PIPX_HOME=/usr/local/pipx
ENV PIPX_BIN_DIR $PIPX_BIN_DIR
ENV PIPX_HOME $PIPX_HOME
RUN --mount=type=cache,target=/config/.cache/pip \
    mkdir -p \
    ${PIPX_BIN_DIR} \
    ${PIPX_HOME} && \
    python3 -m pip install pipx

# --- Install python packages
RUN --mount=type=cache,target=/config/.cache/pip \
    pipx install --include-deps ansible && \
    pipx install ansible-lint

USER 65532
