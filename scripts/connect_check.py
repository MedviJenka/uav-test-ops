"""
Read-only connection check against the PX4 SITL container.

Listens for MAVLink on UDP 14540 (PX4 sends there), finds the autopilot,
and prints a few telemetry values. It never arms or moves the vehicle.

Run from the project root:  uv run python -m scripts.connect_check
"""

import asyncio
from src.ops.logger import log
from typing import Any, Optional
from mavsdk.asyncio.plugins.telemetry import TelemetryAsync
from mavsdk.asyncio import ComponentType, Configuration, Mavsdk


CONNECTION_URL = "udpin://0.0.0.0:14540"  # listen on all interfaces, port 14540

DISCOVERY_TIMEOUT_S = 30.0


async def first(stream) -> Optional[Any]:
    """Return the first value from a telemetry subscription."""
    async for value in stream:
        return value
    return None


async def main() -> None:
    """Configuration"""
    config = Configuration.create_with_component_type(ComponentType.GROUND_STATION)
    async with Mavsdk(config) as mavsdk:
        await mavsdk.add_any_connection(CONNECTION_URL)
        log.fire(
            "Listening on {url}, waiting up to {timeout_s:.0f}s for PX4...",
            url=CONNECTION_URL,
            timeout_s=DISCOVERY_TIMEOUT_S,
        )

        system = await mavsdk.first_autopilot(timeout_s=DISCOVERY_TIMEOUT_S)

        if system is None:
            raise SystemExit(
                "No autopilot found. Is the container running (docker ps)? "
                "Did Windows Firewall block python.exe?"
            )
        log.fire("Connected: system id {system_id}", system_id=await system.get_system_id())

        telemetry = TelemetryAsync(system)
        log.fire("Flight mode: {flight_mode}", flight_mode=await first(telemetry.subscribe_flight_mode()))
        log.fire("Armed:       {armed}", armed=await first(telemetry.subscribe_armed()))
        battery = await first(telemetry.subscribe_battery())
        log.fire("Battery:     {voltage_v:.2f} V", voltage_v=battery.voltage_v)

        log.fire("Waiting for health checks to pass (EKF/GPS can take ~10-30s)...")
        async for ok in telemetry.subscribe_health_all_ok():
            if ok:
                log.fire("Health: all OK, vehicle is ready to arm.")
                break

        position = await first(telemetry.subscribe_position())
        log.fire(
            "Position:    {lat:.6f}, {lon:.6f}  alt AMSL {alt_amsl_m:.1f} m / AGL {alt_agl_m:.1f} m",
            lat=position.latitude_deg,
            lon=position.longitude_deg,
            alt_amsl_m=position.absolute_altitude_m,
            alt_agl_m=position.relative_altitude_m,
        )


if __name__ == "__main__":
    asyncio.run(main())
