import asyncio
from mavsdk.asyncio import Mavsdk, Configuration, ComponentType
from mavsdk.plugins.action import ActionError


async def main():
    config = Configuration.create_with_component_type(ComponentType.GROUND_STATION)
    async with Mavsdk(config) as mavsdk:
        await mavsdk.add_any_connection("udp://:14540")
        system = await mavsdk.first_autopilot(timeout_s=10.0)
        # then use system's action plugin for arm(), takeoff(), land(), ...


if __name__ == '__main__':
    asyncio.run(main())
