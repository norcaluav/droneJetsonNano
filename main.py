#!/usr/bin/env python3

"""
Caveat when attempting to run the examples in non-gps environments:

`drone.offboard.stop()` will return a `COMMAND_DENIED` result because it
requires a mode switch to HOLD, something that is currently not supported in a
non-gps environment.
"""

import asyncio


from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
from mavsdk.telemetry import (PositionNed, PositionVelocityNed)

class PositionConvert:
    """
    Class created as a container for these two functions    
    """

    def PositionNed_to_PositionNedYaw(PositionNed):
        return PositionNedYaw(PositionNed.north_m, PositionNed.east_m, PositionNed.down_m, 0.0)

    def PositionNedYaw_to_PositionNed(PositionNedYaw):
        return PositionNed(PositionNedYaw.north_m, PositionNedYaw.east_m, PositionNedYaw.down_m)

def is_converge(PositionVelocityNed, PositionNed):
    difference_n = abs(PositionVelocityNed.north_m - PositionNed.north_m)
    difference_e = abs(PositionVelocityNed.east_m - PositionNed.east.m)
    difference_d = abs(PositionVelocityNed.down_m - PositionNed.down_m) 
    epsilon = 0.01
    if (difference_n < epsilon and difference_e < epsilon and difference_d < epsilon):
        return True
    else 
        return False





async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    # Set the goal in PositionNedYaw form
    position_goal_yaw = PositionNedYaw(50.0, 50.0, -50.0, 0.0)
    # Convert to PositionNed
    position_goal = PositionConvert.PositionNedYaw_to_PositionNed(position_goal_yaw)
    

    print("-- Go 0m North, 0m East, -50m Down within local coordinate system")
    await drone.offboard.set_position_ned(position_goal_yaw)
    await asyncio.sleep(30)

    print("-- Checking if complete")
    async for position_velocity_ned in drone.telemetry.position_velocity_ned():
     #  if 
  



    print("-- Landing Drone")
    await drone.action.return_to_launch()
    await asyncio.sleep(30)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
