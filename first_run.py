#!/usr/bin/env micropython

from Griffy.griffy import Griffy
from Griffy.missions import Missions
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.motor import SpeedPercent
griffy = Griffy()
missions = Missions()

missions.fifth_run()
