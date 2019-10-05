#!/usr/bin/env micropython

from Griffy.griffy import Griffy
from ev3dev2.sensor.lego import ColorSensor

griffy = Griffy()

# griffy.first_run()
# griffy.drive_until_color(25, 'Red')
griffy.drive_until_white_black(25)
griffy.line_square(15)