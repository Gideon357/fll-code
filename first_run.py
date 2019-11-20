#!/usr/bin/env micropython

from Griffy.griffy import Griffy
from Griffy.missions import Missions
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.motor import SpeedPercent
griffy = Griffy()
.on_arc_right(SpeedPercent(30), griffy.in_to_mm(1.8), griffy.in_to_mm(2.45))