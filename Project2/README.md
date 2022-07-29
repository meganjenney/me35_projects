# Project 2: Line Follower #

A car developed with the SPIKE Prime kit and follows a black line on a white background.

## Contents of Project 2 Line Follower.llsp ##
``` python3
### Created by Megan Jenney
### Last Edited 9 February 2022
### A collaboration between Megan Jenney and Grant Smith
### 
### Intro to Robotics and Mechatronics
### Tufts University Spring 2022
### 
### Project 2: Line Follower
### This script creates a car which is able to follow a black line on a white background,
###     turn onto red lines, and stop for 10 seconds at yellow lines.
### 

from spike import PrimeHub, ColorSensor, ForceSensor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
from time import sleep

## initialize motion control
# hub
hub = PrimeHub()

# inputs
color_sens_port = 'C'
color_sensor = ColorSensor(color_sens_port)

button_port = 'D'
button = ForceSensor(button_port)

# movement outputs
motor1_port = 'A'
motor2_port = 'B'
wheels = MotorPair(motor1_port, motor2_port)
wheels.set_default_speed(-10)

## initialize data instances
# asking for baseline values
white = 0
black_edge = 0
black = 0
red_edge = 0
red = 0
yellow_edge = 0
yellow = 0

print("hit the button for the WHITE READING")
while True:
    if button.is_pressed():
        white = color_sensor.get_reflected_light()
        button.wait_until_released()
        print("WHITE reading is ", white)
        break

print("hit the button for the BLACK READING")
while True:
    if button.is_pressed():
        black = color_sensor.get_reflected_light()
        button.wait_until_released()
        print("BLACK reading is ", black)
        break

print("calculating the BLACK EDGE value...")
black_edge = (white + black) / 2

print("hit the button for the RED READING")
while True:
   if button.is_pressed():
       red = color_sensor.get_reflected_light()
       button.wait_until_released()
       print("RED reading is ", red)
       break

print("calculating the RED EDGE value....")
red_edge = (white + red) / 2

print("BLACK reading is ", black, "   WHITE reading is ", white, "    RED reading is ", red)
print("BLACK EDGE reading is ", black_edge, "      RED EDGE reading is ", red_edge)

# integral and derivative preset values
# sum of all past errors for I
all_errors = 0
# most recent error for D
last_error = 0
# last color
last_color = 'purple'

# wait to start following until 1.5 seconds after button is pressed
print("Hit the button when you're ready to follow!")
while button.is_pressed() == False:
    continue
sleep(1.5)

## control
while True:
    # take a reading
    ref_light = color_sensor.get_reflected_light()

    error = ref_light - black_edge

    # if line has been found after veering off for a while, reset
    if all_errors < -50 and ref_light == black_edge:
        all_errors = 0

    # take a color reading
    color = color_sensor.get_color()
    print("color ", color)

    # stop at yellow line
    if color == 'yellow' and last_color != 'yellow':
        print("STOPPING, WAIT")
        wheels.stop()
        sleep(10)
    elif color == 'red' and black_edge != red_edge:
        print("RED LINE DETECTED, TURNING")
        # turn 90 degrees
        wheels.move_tank(5, 'cm', -10, 10)
        # re-reference with respect to red line
        black_edge = red_edge
        black = red
        # reset errors
        error = 0
        all_errors = 0
        last_error = 0

    last_color = color

    # proportional control
    Kp = 1.2
    P = error * Kp

    # integral control
    all_errors = all_errors + error
    Ki = 0.1
    I = all_errors * Ki

    # derivative control
    error_difference = error - last_error
    Kd = 1
    D = error_difference * Kd
    last_error = error

    # total correction
    correction = P + I + D
    rcorrection = round(-1 * correction)

    # if correction within tolerance, continue on current path
    if (correction < 1) and (correction > -1):
        wheels.start(steering = 0)
    # if correction either extremely positive or negative, align more or less with path edge
    else:
        wheels.start(steering = int(rcorrection))
    
    print("correction ", rcorrection)

    sleep(0.25)


# safety first
wheels.stop()
```
