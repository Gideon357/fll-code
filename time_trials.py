#!/usr/bin/env micropython

from time import sleep

from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import ColorSensor

from Griffy.griffy import Griffy

griffy = Griffy()
