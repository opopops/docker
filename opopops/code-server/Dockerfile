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

FROM base as jq

# --- Install jq CLI
ARG JQ_VERSION="1.7.1"
ENV JQ_VERSION $JQ_VERSION
RUN curl -fsL --output /bin/jq \
    https://github.com/jqlang/jq/releases/download/jq-${JQ_VERSION}/jq-${TARGETOS}-${TARGETARCH} && \
    chmod 755 /bin/jq

USER nonroot

FROM base as yq

# --- Install yq CLI
ARG YQ_VERSION="v4.43.1"
ENV YQ_VERSION $YQ_VERSION
RUN curl -fsL --output /bin/yq \
    https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_${TARGETOS}_${TARGETARCH} && \
    chmod 755 /bin/yq

USER nonroot

FROM base as kubectl

# --- Install kubectl CLI
ARG KUBECTL_VERSION="v1.28.8"
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
ARG HELM_VERSION="v3.14.3"
ENV HELM_VERSION $HELM_VERSION
RUN curl -fsSL https://get.helm.sh/helm-${HELM_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz | \
    tar xvzf - --strip-components=1 -C /bin ${TARGETOS}-${TARGETARCH}/helm && \
    chmod 755 /bin/helm

USER nonroot

FROM base as terraform

# --- Install terraform CLI
ARG TERRAFORM_VERSION="1.7.5"
ENV TERRAFORM_VERSION $TERRAFORM_VERSION
RUN curl -fsSL https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_${TARGETOS}_${TARGETARCH}.zip | \
    gunzip -c - > /bin/terraform && \
    chmod 755 /bin/terraform

USER nonroot

FROM base as tofu

# --- Install tofu CLI
ARG TOFU_VERSION="1.7.0-alpha1"
ENV TOFU_VERSION $TOFU_VERSION
RUN curl -fsSL https://github.com/opentofu/opentofu/releases/download/v${TOFU_VERSION}/tofu_${TOFU_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /bin tofu && \
    chmod 755 /bin/tofu

USER nonroot

FROM base as vault

# --- Install vault CLI
ARG VAULT_VERSION="1.15.6"
ENV VAULT_VERSION $VAULT_VERSION
RUN curl -fsSL https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_${TARGETOS}_${TARGETARCH}.zip | \
    gunzip -c - > /bin/vault && \
    chmod 755 /bin/vault

USER nonroot

FROM lscr.io/linuxserver/code-server:${CODE_SERVER_VERSION}

ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

LABEL org.opencontainers.image.authors="opopops"

ENV DEBIAN_FRONTEND="noninteractive"
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,id=apt-cache-${TARGETARCH}${TARGETVARIANT},target=/var/cache/apt,sharing=locked \
    --mount=type=cache,id=apt-${TARGETARCH}${TARGETVARIANT},target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install --yes --no-install-recommends \
    apache2-utils \
    bash \
    ca-certificates \
    curl \
    git \
    gnupg \
    jq \
    lsb-release \
    openssh-client \
    pigz \
    python3-pip \
    python3-venv \
    rsync \
    unzip

# --- Install docker
ARG DOCKER_VERSION="25.0.6"
ENV DOCKER_VERSION $DOCKER_VERSION
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Pin docker version
# https://docs.docker.com/engine/release-notes/23.0/
RUN cat <<EOF > /etc/apt/preferences.d/docker
Package: /docker-ce/
Pin: version 5:${DOCKER_VERSION}*
Pin-Priority: 1000
EOF

RUN --mount=type=cache,id=apt-cache-${TARGETARCH}${TARGETVARIANT},target=/var/cache/apt,sharing=locked \
    --mount=type=cache,id=apt-${TARGETARCH}${TARGETVARIANT},target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install --yes --no-install-recommends \
    docker-buildx-plugin \
    docker-compose-plugin \
    docker-ce-cli

RUN groupadd -g 996 docker && \
    usermod -a -G docker abc

# --- Install binaries
COPY --from=jq --link /bin/jq /usr/local/bin/jq
COPY --from=yq --link /bin/yq /usr/local/bin/yq
COPY --from=kubectl --link /bin/kubectl /usr/local/bin/kubectl
COPY --from=k9s --link /bin/k9s /usr/local/bin/k9s
COPY --from=helm --link /bin/helm /usr/local/bin/helm
COPY --from=terraform --link /bin/terraform /usr/local/bin/terraform
COPY --from=tofu --link /bin/tofu /usr/local/bin/tofu
COPY --from=vault --link /bin/vault /usr/local/bin/vault

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
    pipx install ansible-lint && \
    pipx install black && \
    pipx install pylint && \
    pipx install pytest
