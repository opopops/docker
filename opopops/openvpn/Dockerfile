FROM cgr.dev/chainguard/wolfi-base:latest

LABEL org.opencontainers.image.authors="opopops"
LABEL org.opencontainers.image.source="https://github.com/opopops/docker"
LABEL org.opencontainers.image.description="OpenVPN image based on Wolfi OS"

RUN apk add --no-cache \
    openvpn

ENV OPENVPN_CONFIG_PATH=/etc/openvpn/client.conf

COPY --chmod=755 files/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD []
