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
ARG YQ_VERSION="v4.44.1"
ENV YQ_VERSION $YQ_VERSION
RUN curl -fsL --output /bin/yq \
    https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_${TARGETOS}_${TARGETARCH} && \
    chmod 755 /bin/yq

USER nonroot

FROM base as powerline-go

# --- Install yq CLI
ARG POWERLINEGO_VERSION="v1.24"
ENV POWERLINEGO_VERSION $POWERLINEGO_VERSION
RUN curl -fsL --output /bin/powerline-go \
    https://github.com/justjanne/powerline-go/releases/download/${POWERLINEGO_VERSION}/powerline-go-${TARGETOS}-${TARGETARCH} && \
    chmod 755 /bin/powerline-go

USER nonroot

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
ARG HELM_VERSION="v3.15.1"
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

FROM base as grype

# --- Install grype CLI
ARG GRYPE_VERSION="0.77.4"
ENV GRYPE_VERSION $GRYPE_VERSION
RUN curl -fsSL https://github.com/anchore/grype/releases/download/v${GRYPE_VERSION}/grype_${GRYPE_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /bin grype && \
    chmod 755 /bin/grype

USER nonroot

FROM base as cosign

# --- Install cosign CLI
ARG COSIGN_VERSION="2.2.4"
ENV COSIGN_VERSION $COSIGN_VERSION
RUN curl -fsSL https://github.com/sigstore/cosign/releases/download/v${COSIGN_VERSION}/cosign-${TARGETOS}-${TARGETARCH} \
    -o /bin/cosign && \
    chmod 755 /bin/cosign

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
ARG TERRAGRUNT_VERSION="0.59.2"
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

FROM base as dagger

# --- Install dagger CLI
ARG DAGGER_VERSION="0.11.7"
ENV DAGGER_VERSION $DAGGER_VERSION
RUN curl -fsSL https://github.com/dagger/dagger/releases/download/v${DAGGER_VERSION}/dagger_v${DAGGER_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /bin dagger && \
    chmod 755 /bin/dagger

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
    dnsutils \
    git \
    gnupg \
    lsb-release \
    nano \
    openssh-client \
    pigz \
    python3-pip \
    python3-venv \
    rsync \
    unzip \
    vim

ENV EDITOR=vi

# --- Install docker
ARG DOCKER_VERSION="26.1.3"
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
COPY --link --from=cosign /bin/cosign /usr/local/bin/cosign
COPY --link --from=dagger /bin/dagger /usr/local/bin/dagger
COPY --link --from=grype /bin/grype /usr/local/bin/grype
COPY --link --from=helm /bin/helm /usr/local/bin/helm
COPY --link --from=helmfile /bin/helmfile /usr/local/bin/helmfile
COPY --link --from=jq /bin/jq /usr/local/bin/jq
COPY --link --from=k9s /bin/k9s /usr/local/bin/k9s
COPY --link --from=kubectl /bin/kubectl /usr/local/bin/kubectl
COPY --link --from=powerline-go /bin/powerline-go /usr/local/bin/powerline-go
COPY --link --from=terraform /bin/terraform /usr/local/bin/terraform
COPY --link --from=terragrunt /bin/terragrunt /usr/local/bin/terragrunt
COPY --link --from=tofu /bin/tofu /usr/local/bin/tofu
COPY --link --from=vault /bin/vault /usr/local/bin/vault
COPY --link --from=yq /bin/yq /usr/local/bin/yq

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

# --- Update bashrc
RUN cat <<EOF >> /config/.bashrc
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

function _update_ps1() {
    PS1="\$(/usr/local/bin/powerline-go -mode flat -hostname-only-if-ssh -cwd-max-depth 3 -modules cwd,git,terraform-workspace,kube -error \$? -jobs \$(jobs -p | wc -l))"
}

if [ "\$TERM" != "linux" ] && [ -f "/usr/local/bin/powerline-go" ]; then
    PROMPT_COMMAND="_update_ps1; \$PROMPT_COMMAND"
fi
EOF
