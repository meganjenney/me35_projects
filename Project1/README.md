# Project 1: Top Spinner #
An automatic release top spinner, developed with the SPIKE Prime kit and designed for a custom 3D-printed top.

## Contents of Project 1 Top Spinner.llsp ##
``` python3
# Created by Megan Jenney
# Last Edited 31 January 2022
#
# Intro to Robotics & Mechatronics
# Spring 2022 Tufts University
#
# Project 1: Spinning Top
# This script will control a pair motor which start a top spinning. One motor controls
# a gear train to start the top spinning, while the other controls a platform which
# releases the top onto a flat surface.

from spike import PrimeHub, LightMatrix, Button, StatusLight, App, Motor
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
from time import sleep

# initialize
hub = PrimeHub()

gear_motor_port = 'A'
platform_motor_port = 'B'
gear_motor = Motor(gear_motor_port)
platform_motor = Motor(platform_motor_port)

print("Hub and motors initialized successfully.")

# start top spinning
#move platform in slightly to secure
platform_motor.run_to_position(32, 'shortest path', 100)

#gear motor spins continuously at max power
gear_motor.start_at_power(-100)
print("Started gear rotation")

# wait to add some speed to top
sleep(5)

# release top
#platform rotates away 90 degrees from top as fast as it can as to avoid any part
#of the top catching on the platform
platform_motor.run_for_degrees(90, 100)
print("Platform moved")

print("End of program, stopping motors")
gear_motor.stop()
platform_motor.stop()
```
