
import asyncio
from mavsdk import System
import datetime
import math
i=0

async def run():
    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14700")

    # Start the tasks
    now = datetime.datetime.utcnow()
    now_local = datetime.datetime.now()
    print(now_local)
    asyncio.ensure_future(print_heading_info(drone))

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


async def print_gs_info(drone):
    async for velocity in drone.telemetry.velocity_ned():
        speed = math.sqrt(velocity.east_m_s * velocity.east_m_s + velocity.north_m_s * velocity.north_m_s)
        print(f"GS info:"+ str(speed))
        global i
        await asyncio.sleep(1)
        i+=1
        print("bat " + str(i) + " seq")
        if i == 99:
            now = datetime.datetime.utcnow()
            now_local = datetime.datetime.now()
            print(now_local)

async def print_heading_info(drone):
    async for heading in drone.telemetry.raw_gps():
        gps_heading = heading.heading_uncertainty_deg
        print(f"heading {gps_heading}")
        global i
        await asyncio.sleep(1)
        i+=1
        print("heading " + str(i) + " seq")
        if i == 99:
            now = datetime.datetime.utcnow()
            now_local = datetime.datetime.now()
            print(now_local)


async def print_flightmode_info(drone):
    async for flight_mode in drone.telemetry.flight_mode():
        print("FlightMode:", flight_mode)
        global i
        await asyncio.sleep(1)
        i+=1
        print("bat " + str(i) + " seq")
        if i == 99:
            now = datetime.datetime.utcnow()
            now_local = datetime.datetime.now()
            print(now_local)


async def print_position(drone):
    async for position in drone.telemetry.position():
        print(position)
        global i
        await asyncio.sleep(1)
        i+=1
        print("bat " + str(i) + " seq")
        if i == 99:
            now = datetime.datetime.utcnow()
            now_local = datetime.datetime.now()
            print(now_local)


if __name__ == "__main__":
    # Start the main function
    asyncio.ensure_future(run())

    # Runs the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()



