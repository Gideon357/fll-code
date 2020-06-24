#!/usr/bin/env micropython

from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import ColorSensor, GyroSensor

from Griffy.griffy import Griffy
from Griffy.missions import Missions

# griffy = Griffy()
missions = Missions()

missions.seventh_run()
