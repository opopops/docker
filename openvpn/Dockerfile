FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk update && \
    apk add --no-cache \
    openvpn

ENV OPENVPN_CONFIG_PATH=/etc/openvpn/client.conf

COPY --chmod=755 files/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD []
