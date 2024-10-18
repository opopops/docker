# syntax=docker/dockerfile:1

ARG WOLFI_VERSION="latest"
ARG CODE_SERVER_VERSION="latest"

FROM chainguard/wolfi-base:${WOLFI_VERSION} AS base

ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

RUN apk add --no-cache \
    curl \
    gzip \
    unzip

FROM base AS kubectl

# --- Install kubectl CLI
ARG KUBECTL_VERSION="v1.29.5"
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
ARG HELMFILE_VERSION="0.169.0"
ENV HELMFILE_VERSION $HELMFILE_VERSION
RUN curl -fsSL https://github.com/helmfile/helmfile/releases/download/v${HELMFILE_VERSION}/helmfile_${HELMFILE_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | \
    tar xvzf - -C /usr/bin helmfile && \
    chmod 755 /usr/bin/helmfile

USER 65532

FROM chainguard/wolfi-base:${WOLFI_VERSION}

LABEL org.opencontainers.image.authors="opopops"

USER root

RUN apk add --no-cache \
    bash \
    bind-tools \
    curl \
    jq \
    nano \
    tzdata \
    unzip \
    vim \
    yq

# --- Install binaries
COPY --link --from=helm /usr/bin/helm /usr/bin/helm
COPY --link --from=helmfile /usr/bin/helmfile /usr/bin/helmfile
COPY --link --from=k9s /usr/bin/k9s /usr/bin/k9s
COPY --link --from=kubectl /usr/bin/kubectl /usr/bin/kubectl

USER 65532
