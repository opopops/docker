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

FROM base AS jq

# --- Install jq CLI
ARG JQ_VERSION="1.7.1"
ENV JQ_VERSION=$JQ_VERSION
RUN curl -fsL --output /usr/bin/jq \
    https://github.com/jqlang/jq/releases/download/jq-${JQ_VERSION}/jq-${TARGETOS}-${TARGETARCH} && \
    chmod 755 /usr/bin/jq

USER nonroot

FROM base AS yq

# --- Install yq CLI
ARG YQ_VERSION="v4.44.1"
ENV YQ_VERSION=$YQ_VERSION
RUN curl -fsL --output /usr/bin/yq \
    https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_${TARGETOS}_${TARGETARCH} && \
    chmod 755 /usr/bin/yq

USER nonroot

FROM base AS powerline-go

# --- Install yq CLI
ARG POWERLINEGO_VERSION="v1.24"
ENV POWERLINEGO_VERSION=$POWERLINEGO_VERSION
RUN curl -fsL --output /usr/bin/powerline-go \
    https://github.com/justjanne/powerline-go/releases/download/${POWERLINEGO_VERSION}/powerline-go-${TARGETOS}-${TARGETARCH} && \
    chmod 755 /usr/bin/powerline-go

USER nonroot

FROM base AS kubectl

# --- Install kubectl CLI
ARG KUBECTL_VERSION="v1.29.5"
ENV KUBECTL_VERSION=$KUBECTL_VERSION
RUN curl -fsSL https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/${TARGETOS}/${TARGETARCH}/kubectl \
    -o /usr/bin/kubectl && \
    chmod 755 /usr/bin/kubectl

USER nonroot

FROM base AS k9s

# --- Install k9s CLI
ARG K9S_VERSION="v0.50.6"
ENV K9S_VERSION=$K9S_VERSION
RUN curl -fsSL https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/bin k9s && \
    chmod 755 /usr/bin/k9s

USER nonroot

FROM base AS helm

# --- Install helm CLI
ARG HELM_VERSION="v3.18.1"
ENV HELM_VERSION=$HELM_VERSION
RUN curl -fsSL https://get.helm.sh/helm-${HELM_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz | \
    tar xvzf - --strip-components=1 -C /usr/bin ${TARGETOS}-${TARGETARCH}/helm && \
    chmod 755 /usr/bin/helm

USER nonroot

FROM base AS helmfile

# --- Install helmfile CLI
ARG HELMFILE_VERSION="1.1.1"
ENV HELMFILE_VERSION=$HELMFILE_VERSION
RUN curl -fsSL https://github.com/helmfile/helmfile/releases/download/v${HELMFILE_VERSION}/helmfile_${HELMFILE_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/bin helmfile && \
    chmod 755 /usr/bin/helmfile

USER nonroot

FROM base AS grype

# --- Install grype CLI
ARG GRYPE_VERSION="0.92.2"
ENV GRYPE_VERSION=$GRYPE_VERSION
RUN curl -fsSL https://github.com/anchore/grype/releases/download/v${GRYPE_VERSION}/grype_${GRYPE_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/bin grype && \
    chmod 755 /usr/bin/grype

USER nonroot

FROM base AS cosign

# --- Install cosign CLI
ARG COSIGN_VERSION="2.5.0"
ENV COSIGN_VERSION=$COSIGN_VERSION
RUN curl -fsSL https://github.com/sigstore/cosign/releases/download/v${COSIGN_VERSION}/cosign-${TARGETOS}-${TARGETARCH} \
    -o /usr/bin/cosign && \
    chmod 755 /usr/bin/cosign

USER nonroot

FROM base AS terraform

# --- Install terraform CLI
ARG TERRAFORM_VERSION="1.12.1"
ENV TERRAFORM_VERSION=$TERRAFORM_VERSION
RUN TEMP_DIR=$(mktemp -d) && \
    curl -fsSL https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_${TARGETOS}_${TARGETARCH}.zip \
    -o ${TEMP_DIR}/terraform.zip && \
    unzip -d $TEMP_DIR ${TEMP_DIR}/terraform.zip  && \
    mv ${TEMP_DIR}/terraform /usr/bin/terraform && \
    chmod 755 /usr/bin/terraform && \
    rm -rf ${TEMP_DIR}

USER nonroot

FROM base AS tofu

# --- Install tofu CLI
ARG TOFU_VERSION="1.9.1"
ENV TOFU_VERSION=$TOFU_VERSION
RUN curl -fsSL https://github.com/opentofu/opentofu/releases/download/v${TOFU_VERSION}/tofu_${TOFU_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/bin tofu && \
    chmod 755 /usr/bin/tofu

USER nonroot

FROM base AS terragrunt

# --- Install terragrunt CLI
ARG TERRAGRUNT_VERSION="0.80.4"
ENV TERRAGRUNT_VERSION=$TERRAGRUNT_VERSION
RUN curl -fsSL https://github.com/gruntwork-io/terragrunt/releases/download/v${TERRAGRUNT_VERSION}/terragrunt_${TARGETOS}_${TARGETARCH} \
    -o /usr/bin/terragrunt && \
    chmod 755 /usr/bin/terragrunt

USER nonroot

FROM base AS vault

# --- Install vault CLI
ARG VAULT_VERSION="1.19.5"
ENV VAULT_VERSION=$VAULT_VERSION
RUN TEMP_DIR=$(mktemp -d) && \
    curl -fsSL https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_${TARGETOS}_${TARGETARCH}.zip \
    -o ${TEMP_DIR}/vault.zip && \
    unzip -d $TEMP_DIR ${TEMP_DIR}/vault.zip  && \
    mv ${TEMP_DIR}/vault /usr/bin/vault && \
    chmod 755 /usr/bin/vault && \
    rm -rf ${TEMP_DIR}

USER nonroot

FROM base AS dagger

# --- Install dagger CLI
ARG DAGGER_VERSION="0.18.9"
ENV DAGGER_VERSION=$DAGGER_VERSION
RUN curl -fsSL https://github.com/dagger/dagger/releases/download/v${DAGGER_VERSION}/dagger_v${DAGGER_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/bin dagger && \
    chmod 755 /usr/bin/dagger

USER nonroot

FROM lscr.io/linuxserver/code-server:${CODE_SERVER_VERSION} AS prod

ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

LABEL org.opencontainers.image.authors="opopops"
LABEL org.opencontainers.image.title="Code-Server"
LABEL org.opencontainers.image.source="https://github.com/opopops/docker/tree/main/images/code-server"
LABEL org.opencontainers.image.description="Code-Server image"

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
    dnsutils \
    git \
    gnupg \
    lsb-release \
    nano \
    openssh-client \
    pigz \
    pipx \
    python3-pip \
    python3-venv \
    rsync \
    unzip \
    vim

ENV EDITOR=vi
ENV PATH="${PATH}:/config/.local/bin"

# --- Install docker
ARG DOCKER_VERSION="28.2.2"
ENV DOCKER_VERSION=$DOCKER_VERSION
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

# --- Install python packages
RUN --mount=type=cache,target=/config/.cache/pip \
    pipx install ansible-lint && \
    pipx install pylint && \
    pipx install pytest && \
    pipx install ruff && \
    pipx install uv

# --- Install binaries
COPY --link --from=cosign /usr/bin/cosign /usr/bin/cosign
COPY --link --from=dagger /usr/bin/dagger /usr/bin/dagger
COPY --link --from=grype /usr/bin/grype /usr/bin/grype
COPY --link --from=helm /usr/bin/helm /usr/bin/helm
COPY --link --from=helmfile /usr/bin/helmfile /usr/bin/helmfile
COPY --link --from=jq /usr/bin/jq /usr/bin/jq
COPY --link --from=k9s /usr/bin/k9s /usr/bin/k9s
COPY --link --from=kubectl /usr/bin/kubectl /usr/bin/kubectl
COPY --link --from=powerline-go /usr/bin/powerline-go /usr/bin/powerline-go
COPY --link --from=terraform /usr/bin/terraform /usr/bin/terraform
COPY --link --from=terragrunt /usr/bin/terragrunt /usr/bin/terragrunt
COPY --link --from=tofu /usr/bin/tofu /usr/bin/tofu
COPY --link --from=vault /usr/bin/vault /usr/bin/vault
COPY --link --from=yq /usr/bin/yq /usr/bin/yq

# --- Update bashrc
RUN cat <<EOF >> /config/.bashrc
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

function _update_ps1() {
    PS1="\$(/usr/bin/powerline-go -mode flat -hostname-only-if-ssh -cwd-max-depth 3 -modules cwd,git,terraform-workspace,kube -error \$? -jobs \$(jobs -p | wc -l))"
}

if [ "\$TERM" != "linux" ] && [ -f "/usr/bin/powerline-go" ]; then
    PROMPT_COMMAND="_update_ps1; \$PROMPT_COMMAND"
fi
EOF
