#!/usr/bin/env micropython

from .griffy import Griffy
from .button import Button
from time import sleep
from sys import stderr
from os import listdir
from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.led import Leds
from ev3dev2.sensor import list_sensors, INPUT_1, INPUT_2, INPUT_3, INPUT_4

Griffy = Griffy()

class Missions:
    def __init__(self):
        Griffy = Griffy()
                
    def traffic_jam():
        Griffy.attachment_tank.on_for_rotations(100,1000, 4)

    
