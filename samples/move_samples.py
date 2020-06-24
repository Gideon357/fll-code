#!/usr/bin/env micropython

from ev3dev2.led import Leds
from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor,
                           MoveTank, SpeedPercent)
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor

tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

# drive in a turn for 5 rotations of the outer motor
# the first two parameters can be unit classes or percentages.
tank_drive.on_for_seconds(SpeedPercent(30), SpeedPercent(30), 2)
