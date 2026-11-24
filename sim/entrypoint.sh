#!/usr/bin/env bash
set -euo pipefail

# Send MAVLink to the Docker host unless PX4_PARTNER_IP is set explicitly.
if [ -z "${PX4_PARTNER_IP:-}" ]; then
    PX4_PARTNER_IP="$(getent ahostsv4 "${PX4_PARTNER_HOST:-host.docker.internal}" | awk 'NR==1{print $1}')" || true
fi
export PX4_PARTNER_IP
echo "[entrypoint] MAVLink partner IP: ${PX4_PARTNER_IP:-localhost}"
echo "[entrypoint] vehicle: ${PX4_TARGET:-gz_x500}  world: ${PX4_GZ_WORLD:-default}  headless: ${HEADLESS:-1}"

export HEADLESS="${HEADLESS:-1}"
cd /px4
exec make px4_sitl "${PX4_TARGET:-gz_x500}"
