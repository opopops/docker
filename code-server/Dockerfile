# syntax=docker/dockerfile:1

FROM lscr.io/linuxserver/code-server:latest

ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

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
ARG DOCKER_VERSION="25.0.4"
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

# --- Install kubectl CLI
ARG KUBECTL_VERSION="v1.28.7"
ENV KUBECTL_VERSION $KUBECTL_VERSION
RUN curl -fsSL https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${TARGETARCH}/kubectl \
        -o /usr/local/bin/kubectl && \
    chmod 755 /usr/local/bin/kubectl

# --- Install k9s CLI
ARG K9S_VERSION="v0.32.3"
ENV K9S_VERSION $K9S_VERSION
RUN curl -fsSL https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/local/bin k9s && \
    chmod 755 /usr/local/bin/k9s

# --- Install helm CLI
ARG HELM_VERSION="v3.14.3"
ENV HELM_VERSION $HELM_VERSION
RUN curl -fsSL https://get.helm.sh/helm-${HELM_VERSION}-linux-${TARGETARCH}.tar.gz | \
    tar xvzf - --strip-components=1 -C /usr/local/bin linux-${TARGETARCH}/helm && \
    chmod 755 /usr/local/bin/helm

# --- Install terraform CLI
ARG TERRAFORM_VERSION="1.7.5"
ENV TERRAFORM_VERSION $TERRAFORM_VERSION
RUN curl -fsSL https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${TARGETARCH}.zip | \
        gunzip -c - > /usr/local/bin/terraform && \
    chmod 755 /usr/local/bin/terraform

# --- Install vault CLI
ARG VAULT_VERSION="1.15.6"
ENV VAULT_VERSION $VAULT_VERSION
RUN curl -fsSL https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_${TARGETARCH}.zip | \
    gunzip -c - > /usr/local/bin/vault && \
    chmod 755 /usr/local/bin/vault

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
