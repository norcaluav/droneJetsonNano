#!/usr/bin/env python3

"""
Caveat when attempting to run the examples in non-gps environments:

`drone.offboard.stop()` will return a `COMMAND_DENIED` result because it
requires a mode switch to HOLD, something that is currently not supported in a
non-gps environment.
"""

import asyncio
import time

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
from mavsdk.telemetry import (PositionNed, PositionVelocityNed)




def PositionNed_to_PositionNedYaw(PositionNed):
    return PositionNedYaw(PositionNed.north_m, PositionNed.east_m, PositionNed.down_m, 0.0)

def PositionNedYaw_to_PositionNed(PositionNedYaw):
    return PositionNed(PositionNedYaw.north_m, PositionNedYaw.east_m, PositionNedYaw.down_m)

async def is_converge(position_goal, drone):
    """
    This function checks if we have arrived at the set location, within some epsilon difference
    """

    async for position in drone.telemetry.position_velocity_ned():
        position_actual = position.position


        print(position_actual)

        difference_n = abs(position_goal.north_m - position_actual.north_m)
        difference_e = abs(position_goal.east_m - position_actual.east_m)
        difference_d = abs(position_goal.down_m - position_actual.down_m) 

        epsilon = 0.1

        if (difference_n < epsilon and difference_e < epsilon and difference_d < epsilon):
            return True
        else:
            return False
            


async def coop_is_converged(position_goal, drone):
    """
    Checks if drone has converged on position goal - includes an asyncio.sleep to allow for other tasks to run.
    This makes this function cooperative and non-blocking. 
    """

    while True:
        if await is_converge(position_goal, drone):
            print("-- Position Arrived")
            return
        else:
            print("-- Position Not Arrived")
            await asyncio.sleep(1)
    
    
        
        










async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("-- Arming")
    #await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result .result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    test_position = 50.0
    # Set the goal in PositionNedYaw form
    position_goal_yaw = PositionNedYaw(test_position, test_position, -50.0, 0.0)
    # Convert to PositionNed
    position_goal = PositionNedYaw_to_PositionNed(position_goal_yaw)
    

    print("-- Go 50m North, 50m East, -50m Down within local coordinate system")
    await drone.offboard.set_position_ned(position_goal_yaw)

    print("-- Creating Task: Checking if complete")
    asyncio.create_task(coop_is_converged(position_goal, drone)) 
    

    

    for i in range(1,60):
        await asyncio.sleep(0.5)
        print(f"-- Working on Fake task {i}")


    #
    # Test 2: what is set_position_ned in reference to? 
    #

    test_position = 0

    # Set the goal in PositionNedYaw form
    position_goal_yaw = PositionNedYaw(test_position, test_position, -50.0, 0.0)
    # Convert to PositionNed
    position_goal = PositionNedYaw_to_PositionNed(position_goal_yaw)


    print("-- Go 0m North, 0m East, -0m Down within local coordinate system")
    await drone.offboard.set_position_ned(position_goal_yaw)





    #print("-- Landing Drone")
    #await drone.action.return_to_launch()
    await asyncio.sleep(30)

#    print("-- Stopping offboard")
#    try: 
#        await drone.offboard.stop()
#    except OffboardError as error:
#        print(f"Stopping offboard mode failed with error code: {error._result.result}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
