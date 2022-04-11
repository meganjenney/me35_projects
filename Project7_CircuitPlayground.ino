// Created by Megan Jenney
// Last Edited 30 March 2022
//
// Intro to Robotics and Mechatronics
// Tufts University Spring 2022
// Department of Mechanical Engineering
//
// Project 7: Random Processor/Sensor/Actuator Exploration
//

#include <Adafruit_CircuitPlayground.h>

#define BLUE 0x0000FF
#define GREEN 0x00FF00
#define OFF 0x000000

// keep track of button states
bool leftButton_prev_on = false;
bool rightButton_prev_on = false;
// keep track of pixel states
bool left_lights_on = false;
bool right_lights_on = false;
bool all_lights_on = false;

void setup() {
  // initialize Circuit Playgorund
  CircuitPlayground.begin();
  // clear any previous formatting
  CircuitPlayground.clearPixels();
  // start serial monitor
  Serial.begin(9600);
}

void loop() {
  // left button pressed
  if (digitalRead(CPLAY_LEFTBUTTON) and !leftButton_prev_on) {
    if (not left_lights_on) {
      if (not right_lights_on) {
        // no lights on, turn only left lights on
        turnLeftOn();
        left_lights_on = true;
      } else {
        // only right lights on, turn all lights green
        turnAllOn();
        left_lights_on = true;
        all_lights_on = true;
      }
      
    } else {
      if (all_lights_on) {
        // all lights on, turn only left lights off
        turnLeftOff();
        turnRightOn();
        all_lights_on = false;
        left_lights_on = false;
      } else {
        // only left lights on, turn off
        turnLeftOff();
        left_lights_on = false;
      }
    }

  // right button pressed
  } else if (digitalRead(CPLAY_RIGHTBUTTON) and not rightButton_prev_on) {
    if (not right_lights_on) {
      if (not left_lights_on) {
        // no lights on, turn only right lights on
        turnRightOn();
        right_lights_on = true;
      } else {
        // only left lights on, turn all lights green
        turnAllOn();
        right_lights_on = true;
        all_lights_on = true;
      }
    } else {
      if (all_lights_on) {
        // all lights on, turn only right lights off
        turnRightOff();
        turnLeftOn();
        all_lights_on = false;
        right_lights_on = false;
      } else {
        // only right lights on, turn off
        turnRightOff();
        right_lights_on = false;
      }
    }
  }

  // wait to try again
  delay(200);
}

// turn on left set of pixels
void turnLeftOn() {
  for (int pixel = 0; pixel < 5; pixel++) {
    CircuitPlayground.setPixelColor(pixel, BLUE);
  }
}

// turn on left set of pixels
void turnLeftOff() {
  for (int pixel = 0; pixel < 5; pixel++) {
    CircuitPlayground.setPixelColor(pixel, OFF);
  }
}

// turn on left set of pixels
void turnRightOn() {
  for (int pixel = 5; pixel < 10; pixel++) {
    CircuitPlayground.setPixelColor(pixel, BLUE);
  }
}

// turn off right set of pixels
void turnRightOff() {
  for (int pixel = 5; pixel < 10; pixel++) {
    CircuitPlayground.setPixelColor(pixel, OFF);
  }
}

void turnAllOn() {
  for (int pixel = 0; pixel < 10; pixel++) {
    CircuitPlayground.setPixelColor(pixel, GREEN);
  }
}
