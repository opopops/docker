# syntax=docker/dockerfile:1

ARG KEYCLOAK_VERSION="latest"

FROM bitnami/keycloak:${KEYCLOAK_VERSION}

ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

# --- Install SCIM SDK plugin
COPY --chown=1001:0 --chmod=660 files/scim-for-keycloak-kc-24-2.1.0-free.jar /opt/bitnami/keycloak/providers/
