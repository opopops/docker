# syntax=docker/dockerfile:1

ARG WOLFI_VERSION="latest"
ARG CODE_SERVER_VERSION="latest"

FROM lscr.io/linuxserver/code-server:${CODE_SERVER_VERSION} AS prod

ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

LABEL org.opencontainers.image.authors="opopops"
LABEL org.opencontainers.image.title="code-server"
LABEL org.opencontainers.image.source="https://github.com/opopops/docker/tree/main/images/code-server"
LABEL org.opencontainers.image.description="Code-Server image"

ENV DEBIAN_FRONTEND="noninteractive"
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
    rsync \
    unzip \
    vim

# --- Install mise
ARG MISE_VERSION="2025.12.12"
ENV MISE_DATA_DIR="/mise" \
    MISE_CONFIG_DIR="/mise" \
    MISE_CACHE_DIR="/mise/cache" \
    MISE_INSTALL_PATH="/usr/local/bin/mise" \
    MISE_VERSION="${MISE_VERSION}"
RUN mkdir -m 777 -p $MISE_CACHE_DIR \
COPY ./mise.toml ${MISE_CONFIG_DIR}/mise.toml
RUN --mount=type=cache,id=mise-cache,target=${MISE_CACHE_DIR} \
    --mount=type=secret,id=github_token,env=GITHUB_TOKEN \
    curl https://mise.run | sh && \
    mise upgrade

ENV EDITOR=vi

# --- Update bashrc
RUN cat <<EOF >> /config/.bashrc
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

alias d="docker"
alias dri="docker run -it --rm --entrypoint=''"
alias dprune="docker system prune -a -f"
alias dshell="docker run -it --rm --pull always ghcr.io/opopops/wolfi/shell:latest-dev bash"
alias dwolfi="docker run -it --rm --pull always cgr.dev/chainguard/wolfi-base:latest sh"
alias dc="docker compose"
alias k="kubectl"
alias kshell="kubectl run shell --rm -i --tty --image-pull-policy='Always' --image ghcr.io/opopops/wolfi/shell:latest -- bash"
alias kwolfi="kubectl run shell --rm -i --tty --image-pull-policy='Always' --image cgr.dev/chainguard/wolfi-base:latest -- bash"
alias terraform='tofu'
alias tf='tofu'
alias g='git'

# MISE
eval "\$(mise activate bash)"

# POWERLINE-GO
function _update_ps1() {
    PS1="\$(${MISE_DATA_DIR}/installs/powerline-go/1.25/powerline-go -mode flat -hostname-only-if-ssh -cwd-max-depth 3 -modules cwd,git,terraform-workspace,kube -error \$? -jobs \$(jobs -p | wc -l))"
}
PROMPT_COMMAND="_update_ps1; \$PROMPT_COMMAND"
EOF
