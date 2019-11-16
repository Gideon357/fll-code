#!/usr/bin/env micropython

from .griffy import Griffy
from .button import Button
from ev3dev2.motor import SpeedPercent
from sys import stderr
from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.led import Leds
from ev3dev2.sensor import list_sensors, INPUT_1, INPUT_2, INPUT_3, INPUT_4
from time import sleep
import time

class Missions(Griffy):
    """
    Missions has all of the missions we run and is based of of griffy
    """

    def first_run(self):
        """Crane: 4"""
        self.on_for_distance(SpeedPercent(30), 10, use_gyro=False)
        self.move_tank.on_for_rotations(-20,20, .19)
        self.on_for_distance(SpeedPercent(-30), 13, use_gyro=False)
        self.on_for_distance(SpeedPercent(25), 24.5, use_gyro=False)
        sleep(1)
        self.on_for_distance(SpeedPercent(-30), 2, use_gyro=False)
        self.on_arc_left(SpeedPercent(-50), self.in_to_mm(6), self.in_to_mm(25))

    def second_run(self):
        """Buildings, Innovation: 2"""
        self.on_for_distance(SpeedPercent(30), 15.4, use_gyro=False)
        self.on_for_distance(SpeedPercent(-75), 6, use_gyro=False)
        self.on_arc_left(-80, self.in_to_mm(4), self.in_to_mm(15))
    
    def third_run(self):
        """Treehouse: ???"""
        self.on_for_distance(SpeedPercent(30), 24.5, use_gyro=False)
        self.attachment_raise_lower(10, 1)
        self.on_for_distance(SpeedPercent(30), 3, use_gyro=False)
        self.on_for_distance(SpeedPercent(-75), 21, use_gyro=False)

    def fourth_run(self):
        """Traffic Jam: 2"""
        self.on_for_distance(50, 22, use_gyro=False)
        self.move_tank.on_for_rotations(15, -15, .1)
        self.move_tank.on_for_rotations(-15, 15, .1)
        self.on_for_distance(-100, 36, use_gyro=False)
        # add turn and lower back

    def fifth_run(self):
        """Broken building elevator and swing: Jig"""
        # 90 degrees is `self.in_to_mm(1.8), self.in_to_mm(3.5)`
        self.left_medium_motor.on_for_rotations(-100, .1) # Turn attachment
        self.on_for_distance(SpeedPercent(50), 38, use_gyro=False) # Go to the beige circle
        self.left_medium_motor.on_for_seconds(10, 0.6) # Turn attachment
        self.on_for_distance(SpeedPercent(-20), 5.5, use_gyro=False) # Backup from the houses we put
        self.move_tank.on_for_rotations(25, -25, .16) # Turn past the houses
        self.left_medium_motor.on_for_seconds(-50, 0.9) # Turn attachment
        sleep(1)
        self.on_for_distance(SpeedPercent(50), 13.3, use_gyro=False) # Go forward 13 inches
        self.on_for_distance(SpeedPercent(30), 4.25, use_gyro=False) # Go forward 7 inches
        self.move_tank.on_for_rotations(15, -15, .1) # Turn to the right
        self.move_tank.on_for_rotations(-15, 15, .1) # Turn to the left
        self.on_for_distance(SpeedPercent(-20), 4, use_gyro=False) # Back up
        self.left_medium_motor.on_for_rotations(75, .15) # Turn attachment
        self.move_tank.on_for_rotations(25, -25, .36) # Turn to the right
        self.on_for_distance(SpeedPercent(30), 7, use_gyro=False)
        self.move_tank.on_for_rotations(-25, 25, .2) # Turn to the left
        self.on_for_distance(SpeedPercent(-30), 9, use_gyro=False)
        self.on_for_distance(SpeedPercent(30), 3, use_gyro=False)
        self.move_tank.on_for_rotations(-25, 25, .31) # Turn to the right
        self.on_for_distance(-80, 60, use_gyro=False)
    
    def sixth_run(self):
        self.on_for_distance(50, 22)
        # self.line_square(20)
        self.move_tank.on_for_rotations(-15, 15, .571) 
        # self.line_square(20)
        self.on_for_distance(40, 15)
        self.move_tank.on_for_rotations(15, -15, .1) 
        self.on_for_distance(10, 15)