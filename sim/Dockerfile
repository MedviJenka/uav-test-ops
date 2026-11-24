# PX4 SITL + Gazebo Harmonic, headless.
# The official px4io/px4-dev image is built with --no-sim-tools (no Gazebo),
# so this image runs PX4's own setup script with simulation tools included.
FROM ubuntu:22.04

ARG PX4_VERSION=v1.17.0

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    TZ=UTC \
    RUNS_IN_DOCKER=true

RUN apt-get update \
    && apt-get install -y --no-install-recommends git sudo ca-certificates lsb-release \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch ${PX4_VERSION} --recursive \
  https://github.com/PX4/PX4-Autopilot.git /px4 \
  && git config --global --add safe.directory '*'

WORKDIR /px4

# Toolchain, Python deps and Gazebo Harmonic.
RUN bash ./Tools/setup/ubuntu.sh \
 && rm -rf /var/lib/apt/lists/*

# Inside a container "localhost" is the container itself. Let every MAVLink
# link take a partner IP (set by the entrypoint to the Docker host) so
# QGroundControl (14550) and API/offboard code (14540) on the host receive
# telemetry exactly as with a native install.
RUN sed -i '/mavlink start/ s/[[:space:]]*$/ ${PX4_PARTNER_IP:+-t $PX4_PARTNER_IP}/' \
        ROMFS/px4fmu_common/init.d-posix/px4-rc.mavlink \
 && grep -n 'mavlink start' ROMFS/px4fmu_common/init.d-posix/px4-rc.mavlink \
 && test "$(grep -c 'PX4_PARTNER_IP' ROMFS/px4fmu_common/init.d-posix/px4-rc.mavlink)" -ge 4

# Pre-build so container start is fast. No run target here: `make px4_sitl gz_x500`
# would launch the simulator inside the build and never exit (DONT_RUN is ignored).
RUN make px4_sitl

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh && chmod +x /usr/local/bin/entrypoint.sh


# MAVLink: GCS / offboard local ports (for clients that connect in)
EXPOSE 18570/udp 14580/udp

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
