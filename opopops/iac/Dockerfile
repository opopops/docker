# syntax=docker/dockerfile:1

ARG WOLFI_VERSION="latest"
ARG CODE_SERVER_VERSION="latest"

FROM chainguard/wolfi-base:${WOLFI_VERSION} as base

ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

RUN apk add --no-cache \
    curl \
    gzip \
    unzip

FROM base as kubectl

# --- Install kubectl CLI
ARG KUBECTL_VERSION="v1.29.5"
ENV KUBECTL_VERSION $KUBECTL_VERSION
RUN curl -fsSL https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/${TARGETOS}/${TARGETARCH}/kubectl \
    -o /bin/kubectl && \
    chmod 755 /bin/kubectl

USER nonroot

FROM base as k9s

# --- Install k9s CLI
ARG K9S_VERSION="v0.32.4"
ENV K9S_VERSION $K9S_VERSION
RUN curl -fsSL https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /bin k9s && \
    chmod 755 /bin/k9s

USER nonroot

FROM base as helm

# --- Install helm CLI
ARG HELM_VERSION="v3.15.2"
ENV HELM_VERSION $HELM_VERSION
RUN curl -fsSL https://get.helm.sh/helm-${HELM_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz | \
    tar xvzf - --strip-components=1 -C /bin ${TARGETOS}-${TARGETARCH}/helm && \
    chmod 755 /bin/helm

USER nonroot

FROM base as helmfile

# --- Install helmfile CLI
ARG HELMFILE_VERSION="0.164.0"
ENV HELMFILE_VERSION $HELMFILE_VERSION
RUN curl -fsSL https://github.com/helmfile/helmfile/releases/download/v${HELMFILE_VERSION}/helmfile_${HELMFILE_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /bin helmfile && \
    chmod 755 /bin/helmfile

USER nonroot

FROM base as terraform

# --- Install terraform CLI
ARG TERRAFORM_VERSION="1.8.5"
ENV TERRAFORM_VERSION $TERRAFORM_VERSION
RUN TEMP_DIR=$(mktemp -d) && \
    curl -fsSL https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_${TARGETOS}_${TARGETARCH}.zip \
        -o ${TEMP_DIR}/terraform.zip && \
    unzip -d $TEMP_DIR ${TEMP_DIR}/terraform.zip  && \
    mv ${TEMP_DIR}/terraform /bin/terraform && \
    chmod 755 /bin/terraform && \
    rm -rf ${TEMP_DIR}

USER nonroot

FROM base as tofu

# --- Install tofu CLI
ARG TOFU_VERSION="1.7.2"
ENV TOFU_VERSION $TOFU_VERSION
RUN curl -fsSL https://github.com/opentofu/opentofu/releases/download/v${TOFU_VERSION}/tofu_${TOFU_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /bin tofu && \
    chmod 755 /bin/tofu

USER nonroot

FROM base as terragrunt

# --- Install terragrunt CLI
ARG TERRAGRUNT_VERSION="0.58.13"
ENV TERRAGRUNT_VERSION $TERRAGRUNT_VERSION
RUN curl -fsSL https://github.com/gruntwork-io/terragrunt/releases/download/v${TERRAGRUNT_VERSION}/terragrunt_${TARGETOS}_${TARGETARCH} \
    -o /bin/terragrunt && \
    chmod 755 /bin/terragrunt

USER nonroot

FROM base as vault

# --- Install vault CLI
ARG VAULT_VERSION="1.16.2"
ENV VAULT_VERSION $VAULT_VERSION
RUN curl -fsSL https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_${TARGETOS}_${TARGETARCH}.zip | \
    gunzip -c - > /bin/vault && \
    chmod 755 /bin/vault

USER nonroot

FROM base as doctl

# --- Install doctl CLI
ARG DOCTL_VERSION="1.107.0"
ENV DOCTL_VERSION $DOCTL_VERSION
RUN curl -fsSL https://github.com/digitalocean/doctl/releases/download/v${DOCTL_VERSION}/doctl-${DOCTL_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz | \
    tar xvzf - -C /bin doctl && \
    chmod 755 /bin/doctl

USER nonroot

FROM base as dagger

# --- Install dagger CLI
ARG DAGGER_VERSION="0.11.7"
ENV DAGGER_VERSION $DAGGER_VERSION
RUN curl -fsSL https://github.com/dagger/dagger/releases/download/v${DAGGER_VERSION}/dagger_v${DAGGER_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /bin dagger && \
    chmod 755 /bin/dagger

FROM chainguard/wolfi-base:${WOLFI_VERSION}

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
RUN mkdir -p /usr/local/bin
COPY --link --from=dagger /bin/dagger /usr/local/bin/dagger
COPY --link --from=doctl /bin/doctl /usr/local/bin/doctl
COPY --link --from=helm /bin/helm /usr/local/bin/helm
COPY --link --from=helmfile /bin/helmfile /usr/local/bin/helmfile
COPY --link --from=k9s /bin/k9s /usr/local/bin/k9s
COPY --link --from=kubectl /bin/kubectl /usr/local/bin/kubectl
COPY --link --from=terraform /bin/terraform /usr/local/bin/terraform
COPY --link --from=terragrunt /bin/terragrunt /usr/local/bin/terragrunt
COPY --link --from=tofu /bin/tofu /usr/local/bin/tofu
COPY --link --from=vault /bin/vault /usr/local/bin/vault

# --- Install pipx
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

USER nonroot
