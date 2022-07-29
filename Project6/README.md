# Project 6: Toothpaste Dispenser #
A toothpaste dispenser which detects loaded toothbrush, originally created for the Raspberry Pi BuildHAT and modelled with Onshape. Ultimately executed with SPIKE Prime kit.

## Contents of Project 6: Toothpaste Dispenser.llsp ##
``` python3
### Created by Megan Jenney
### Last Edited 3 May 2022
###
### Intro to Robotics and Mechanics
### Tufts University Spring 2022
### Department of Mechanical Engineering
###
### Projects 5+6: Automated Toothpaste Dispenser
### This script controls an automated tooth dispenser which senses when
###    a toothbrush is loaded, dispenses toothpaste onto the toothbrush,
###    and takes a picture of the loaded toothbrush. This also predicts the
###    approximate number of toothpaste applications left before the current
###    tube of toothpaste will have to be replaced.
### A toothbrush is consider 'loaded' when the head is underneath the
###    toothpaste tube (determined with a distance sensor) for 5 seconds
###    followed by a button press.
### The image is saved to the file "Recent_Dispense.jpg" in this directory.
### The device is using Onshape to aid in the predictions of remaining
###    toothpaste amounts.
###
### Originally this script was part of a Python script which ran on a
###     Raspberry Pi 4B fitted with a Build HAT. It still runs in
###     conjunction with a script for the PiCamera, taken after the
###     toothpaste is dispensed onto the toothbrush.
### Block comments are from the original script using the Build HAT.

## Import
'''
from picamera import PiCamera
from buildhat import DistanceSensor, ForceSensor, Hat, Motor, MotorPair
'''
from spike import DistanceSensor, ForceSensor, Motor, MotorPair, PrimeHub
from time import time, sleep
'''from sys import stderr'''


## Functions
'''
def checkDevicesConnected(device_info):
    conn_devices = []

    for port in device_info:
        conn_devices.append(device_info[port]['name'])

    if not 'DistanceSensor' in conn_devices:
        print("Error: no distance sensor connected to the Build HAT.",file=stderr)
        exit()
    elif not 'ForceSensor' in conn_devices:
        print("Error: no force sensor connected to the Build HAT.",file=stderr)
        exit()
    elif not 'Motor' in conn_devices:
        print("Error: no motors connected to the Build HAT.",file=stderr)
        exit()

    print("All devices connected.")
'''

def checkLoadedDistance(read_dist, dist_target=4, dist_tol=1):
    # get tolerance range
    min_dist_tol = dist_target - dist_tol
    max_dist_tol = dist_target + dist_tol

    if read_dist > max_dist_tol:
        return False
    elif read_dist < min_dist_tol:
        return False
    else:
        return True

def toleranceForTime(target_time=5):
    # stay within tolerance for 5 seconds
    start_time = time()
    curr_time = time()
    elapsed_time = curr_time - start_time

    while elapsed_time < target_time:
        # reset if dist outside of range
        '''read_dist = dist.get_distance()'''
        read_dist = dist.get_distance_cm(short_range=True)
        if not checkLoadedDistance(read_dist):
            print("Out of range.")
            return False
        sleep(0.05)
        # recalculate elapsed time
        curr_time = time()
        elapsed_time = curr_time - start_time

    return True

def distToDegrees(dist=1):
    deg_to_turn = dist * 30
    print(deg_to_turn)
    return deg_to_turn


'''
## Verify All Parts Connected
hat = Hat()
print("Hat has been initialized.")
#print(hat.get())

# find if each device connected
device_info = hat.get()
checkDevicesConnected(device_info)
'''


## Initialize All Devices
dist_port = 'C'
dist = DistanceSensor(dist_port)

button_port = 'D'
button = ForceSensor(button_port)

'''
tube_motor_port = 'C'
tube_motor = Motor(tube_motor_port)
'''
lft_tube_mtr_port = 'A'
rgt_tube_mtr_port = 'B'
tube_motors = MotorPair(lft_tube_mtr_port, rgt_tube_mtr_port)

'''camera = PiCamera()'''

print("All devices initialized.")


## Part 1: Detection

# wait for dist to get in tolerance of target
while True:
    '''read_dist = dist.get_distance()'''
    read_dist = dist.get_distance_cm(short_range=True)
    print("Checking distance...")

    # if read distance in tolerance range for duration
    if checkLoadedDistance(read_dist):
        print("Object detected in range.")
        print("Checking for remainder of time...")

        if toleranceForTime():
            break

    print("Object out of range. Trying again...")
    # try again if not in tolerance for duration
    sleep(0.05)

print("In range for duration. Waiting for button press...")
# wait for button press
while True:
    if button.is_pressed():
        break
    sleep(0.05)

print("Part 1 (Detection) Complete.")
print("Proceeding to Part 2...")


## Part 2: Toothpaste Application

# turn motor for toothpaste disposal
deg_to_turn = distToDegrees(6)
print("Dispensing toothpaste...")
'''tube_motor.run_for_degrees(deg_to_turn, speed=50)'''
#tube_motor.run_for_degrees(deg_to_turn, speed=50)
tube_motors.set_motor_rotation(1, unit='in')
tube_motors.move(-0.5, unit='in', speed=10)
# stop motor in case
#tube_motor.stop()
tube_motors.stop()

print("Complete.")
```
