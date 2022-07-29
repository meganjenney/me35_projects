# Project 3: Dog Feeder #
A feeder which automatically dispenses dog food, created and controlled with the SPIKE Prime kit.

## Contents of Project 3 Dog Feeder Final.llsp ##
``` python3
### Created by Megan Jenney
### Last Edited 16 February 2022
### A Collaboration with Katie Castor and Trevar Hall
###
### Intro to Robotics and Mechanics
### Tufts University Spring 2022
###
### Project 3: Dog Food Dispenser
### This script controlls a food dispenser for your pet, and allows for them to be more paced
###     while eating, and putting you in control of the amount of food they have each meal.
### To change the amount of food your pet will eat each meal, based on sections of an internal
###     wheel dispensing structure, edit 'meal_portions' on line 37 (unit: WHEEL SECTIONS)
### To change the amount of time your pet should wait between meal portions, edit
###     'time_between_portions' on line 38 (unit: SECONDS)

## import statements
from spike import PrimeHub, ForceSensor, Motor, App
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

print("Hello!")
print("Starting up your feeder...")

## initialize
hub = PrimeHub()

# bone shaped chew toy button
button_port = 'E'
button = ForceSensor(button_port)

# wheel dispense mechanism
dispenser_port = 'A'
dispenser = Motor(dispenser_port)
dispenser.set_default_speed(20)

number_sections = 5
degrees_to_turn = int(360 / number_sections)

## functionality
meal_portions = 2
time_between_portions = 30
portions_fed = 0
time_between_iterations = 0.05

print("starting to feed!")
# while not all portions of meal have been fully dispensed
while portions_fed < 4:
    if button.get_force_newton() > 3:
        print("Feeding another portion! This will be portion %s of %s this meal." % (portions_fed+1, meal_portions))
        # feed
        dispenser.run_for_degrees(degrees_to_turn)
        #increment times fed
        portions_fed += 1
        # wait
        wait_for_seconds(time_between_portions - time_between_iterations)
        print("You can have another portion!")
    wait_for_seconds(time_between_iterations)

# done feeding
print("Your pet has completed thier meal.\n Have a good day!")
# show completion image
hub.light_matrix.show_image('HAPPY')

wait_for_seconds(120)
```
