
import asyncio
from mavsdk import System
import datetime
i=0

async def run():
    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14700")

    # Start the tasks
    now = datetime.datetime.utcnow()
    now_local = datetime.datetime.now()
    print(now_local)
    asyncio.ensure_future(print_battery(drone))

async def print_battery(drone):
    async for battery in drone.telemetry.battery():
        print(f"Battery: {battery.remaining_percent}")
        global i
        await asyncio.sleep(1)
        i+=1
        print("bat " + str(i) + " seq")
        if i == 99:
            now = datetime.datetime.utcnow()
            now_local = datetime.datetime.now()
            print(now_local)


async def print_gps_info(drone):
    async for gps_info in drone.telemetry.gps_info():
        print(f"GPS info: {gps_info}")


async def print_in_air(drone):
    async for in_air in drone.telemetry.in_air():
        print(f"In air: {in_air}")


async def print_position(drone):
    async for position in drone.telemetry.position():
        print(position)


if __name__ == "__main__":
    # Start the main function
    asyncio.ensure_future(run())

    # Runs the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()



