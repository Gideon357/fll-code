#!/usr/bin/env micropython

from Griffy.griffy import Griffy
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

griffy = Griffy()