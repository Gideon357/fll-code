#!/usr/bin/env micropython

from Griffy.griffy import Griffy
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.motor import SpeedPercent
griffy = Griffy()

griffy.first_run()
