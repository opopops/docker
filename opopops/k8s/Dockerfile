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

FROM base as helm

# --- Install helm CLI
ARG HELM_VERSION="v3.14.3"
ENV HELM_VERSION $HELM_VERSION
RUN curl -fsSL https://get.helm.sh/helm-${HELM_VERSION}-${TARGETOS}-${TARGETARCH}.tar.gz | \
    tar xvzf - --strip-components=1 -C /bin ${TARGETOS}-${TARGETARCH}/helm && \
    chmod 755 /bin/helm

USER nonroot

FROM chainguard/bash:${WOLFI_VERSION}

LABEL org.opencontainers.image.authors="opopops"

USER root

# --- Install binaries
RUN mkdir -p /usr/local/bin
COPY --link --from=jq /bin/jq /usr/local/bin/jq
COPY --link --from=yq /bin/yq /usr/local/bin/yq
COPY --link --from=kubectl /bin/kubectl /usr/local/bin/kubectl
COPY --link --from=helm /bin/helm /usr/local/bin/helm

USER nonroot
