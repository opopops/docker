#!/usr/bin/env sh

exec -- openvpn --config ${OPENVPN_CONFIG_PATH} "$@"

