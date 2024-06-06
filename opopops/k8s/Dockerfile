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
RUN mkdir -p /usr/local/bin
COPY --link --from=helm /bin/helm /usr/local/bin/helm
COPY --link --from=helmfile /bin/helmfile /usr/local/bin/helmfile
COPY --link --from=k9s /bin/k9s /usr/local/bin/k9s
COPY --link --from=kubectl /bin/kubectl /usr/local/bin/kubectl

USER nonroot
