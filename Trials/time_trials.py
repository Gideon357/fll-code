#!/usr/bin/env micropython

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveTank, SpeedPercent 
from ev3dev2.sound import Sound
from time import sleep

tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

tank_drive.on_for_seconds(SpeedPercent(50), SpeedPercent(50), 2.5)
tank_drive.on_for_seconds(SpeedPercent(-70), SpeedPercent(-70), 2.5)