#!usr/bin/env python3
### Created by Megan Jenney
### Last Edited 25 March 2022
###
### Intro to Robotics and Mechanics
### Tufts University Spring 2022
### Department of Mechanical Engineering
### 
### Projects 5+6: Automated Toothpaste Dispenser
### This script controls an automated tooth dispenser which senses when
###     a toothbrush is loaded, dispenses toothpaste onto the toothbrush,
###     and takes a picture of the loaded toothbrush. This also predicts the
###     approximate number of toothpaste applications left before the current
###     tube of toothpaste will have to be replaced. 
### A toothbrush is consider 'loaded' when the head is underneath the
###     toothpaste tube (determined with a distance sensor) for 5 seconds
###     followed by a button press.
### The image is saved to the file "Recent_Dispense.jpg" in this directory.
### The device is using Onshape to aid in the predictions of remaining
###     toothpaste amounts.
###
### Before running this script for the first time, be sure to run
###     chmod u+x toothpaste_dispenser.py

from picamera import PiCamera
from buildhat import DistanceSensor, ForceSensor, Hat, Motor, MotorPair
from time import time, sleep
from sys import stderr

## Functions
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


def checkLoadedDistance(read_dist, dist_target=2, dist_tol = 1):
    # get tolerance range
    min_dist_tol = dist_target - dist_tol
    max_dist_tol = dist_target + dist_tol
    
    if read_dist > max_dist_tol:
        return false
    elif read_dist < min_dist_tol:
        return false
    else:
        return true

def toleranceForTime(target_time=5):
    # stay within tolerance for 5 seconds
    start_time = time()
    curr_time = time()
    elapsed_time = curr_time - start_time
    
    while elapsed_time < target_time:
        # reset if dist outside of range
        if not checkLoadedDistance():
            return False
        sleep(0.01)
        # recalculate elapsed time
        curr_time = time()
        elapsed_time = curr_time - start_time
    
    return True

def distToDegrees(dist=1):
    deg_to_turn = dist
    return deg_to_turn


## Verify All Parts Connected
hat = Hat()
print("Hat has been initialized.")
#print(hat.get())

# find if each device connected
device_info = hat.get()
checkDevicesConnected(device_info)


## Initialize All Devices
dist_port = 'A'
dist = DistanceSensor(dist_port)

button_port = 'B'
button = ForceSensor(button_port)

tube_motor_port = 'C'
tube_motor = Motor(tube_motor_port)

camera = PiCamera()

print("All devices initialized.")


## Part 1: Detection

# wait for dist to get in tolerance of target
while True:
    read_dist = dist.get_distance()
    
    # if read distance in tolerance range for duration
    if checkLoadedDistance(read_dist):
        print("Object detected in range.")
        print("Checking for remainder of time...")
        
        if toleranceForTime():
            break
        
        print("Object out of range. Trying again...")
    
    # try again if not in tolerance for duration
    sleep(0.05)

# wait for button press
while True:
    if button.is_pressed():
        break
    sleep(0.05)

print("Part 1 (Detection) Complete.")
print("Proceeding to Part 2...")


## Part 2: Toothpaste Application

# turn motor for 1 cm of paste disposal
deg_to_turn = distToDegrees()
print("Dispensing toothpaste...")
tube_motor.run_for_degrees(deg_to_turn)
# stop motor in case
tube_motor.stop()

# DECIDE: cut off from tube


## Part 3: Photograph

# sleep for sensing light levels
sleep(3)

# save in this directory
camera.capture('/home/pi/Documents/me35_projects/Project6/Recent_Dispense.jpg')


## Part 4: Replacement Prediction

# how do I do this !!!
