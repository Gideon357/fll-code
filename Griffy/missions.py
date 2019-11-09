#!/usr/bin/env micropython

from .griffy import Griffy
from .button import Button
from ev3dev2.motor import SpeedPercent
from time import sleep
from sys import stderr
from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.led import Leds
from ev3dev2.sensor import list_sensors, INPUT_1, INPUT_2, INPUT_3, INPUT_4


class Missions(Griffy):
    """
    Missions has all of the missions we run and is based of of griffy
    """

    def first_run(self):
        """Crane: 4"""
        self.on_for_distance(SpeedPercent(30), 10, use_gyro=False)
        self.move_tank.on_for_rotations(-20,20, .145)
        self.on_for_distance(SpeedPercent(-30), 13, use_gyro=False)
        self.on_for_distance(SpeedPercent(25), 24.5, use_gyro=False)
        sleep(1)
        self.on_for_distance(SpeedPercent(-30), 2, use_gyro=False)
        self.on_arc_left(SpeedPercent(-50), self.in_to_mm(6), self.in_to_mm(24))

    def second_run(self):
        """Buildings, Innovation: ???"""
        self.on_for_distance(SpeedPercent(30), 390, use_gyro=False)
        self.on_for_distance(SpeedPercent(-75), 125, use_gyro=False)
        self.on_arc_left(-80, self.in_to_mm(4), self.in_to_mm(15))
        sleep(8)
        # make this an arc so we dont have to aim it
        self.on_for_distance(SpeedPercent(60), 37.5, use_gyro=False)
        self.on_for_distance(SpeedPercent(-60), 8, use_gyro=False)
    
    def third_run(self):
        """Treehouse: """
        self.on_for_distance(SpeedPercent(30), 24.5, use_gyro=False)
        self.attachment_raise_lower(10, 1)
        self.on_for_distance(SpeedPercent(30), 3, use_gyro=False)
        self.on_for_distance(SpeedPercent(-75), 21, use_gyro=False)

    def fourth_run(self):
        """Traffic Jam: wall"""
        self.on_for_distance(50, 22, use_gyro=False)
        self.move_tank.on_for_rotations(15, -15, .1)
        self.move_tank.on_for_rotations(-15, 15, .1)
        self.on_for_distance(-100, 36, use_gyro=False)
        self.move_tank.on_for_rotations(-15, 15, .25)

    def fifth_run(self):
        """Broken building elevator and swing: 7"""
        # 90 degrees is `self.in_to_mm(1.8), self.in_to_mm(3.5)`
        self.left_medium_motor.on_for_rotations(-100, .1) # Turn attachment
        self.on_for_distance(SpeedPercent(50), 38, use_gyro=False) # Go to the beige circle
        self.left_medium_motor.on_for_rotations(100, .1) # Turn attachment
        self.on_for_distance(SpeedPercent(-20), 5, use_gyro=False) # Backup from the houses we put
        self.move_tank.on_for_rotations(15, -15, .15) # Turn past the houses
        self.left_medium_motor.on_for_rotations(-100, .45) # Turn attachment
        self.move_tank.on_for_rotations(15, -15, .03) # Turn to the right
        self.on_for_distance(SpeedPercent(40), 11, use_gyro=False) # Go forward 8.5 inches
        self.left_medium_motor.on_for_rotations(75, .125) # Turn attachment
        self.on_for_distance(SpeedPercent(30), 7, use_gyro=False) # Go forward 7 inches
        self.move_tank.on_for_rotations(15, -15, .1) # Turn to the right
        self.move_tank.on_for_rotations(-15, 15, .1) # Turn to the left
        self.on_for_distance(SpeedPercent(-20), 4, use_gyro=False)
        self.on_arc_right(SpeedPercent(30), self.in_to_mm(1.8), self.in_to_mm(2.45))
        self.on_for_distance(SpeedPercent(30), 7, use_gyro=False)
        self.on_arc_left(SpeedPercent(30), self.in_to_mm(1.8), self.in_to_mm(1))
        self.on_for_distance(SpeedPercent(-30), 6, use_gyro=False)
        self.on_arc_right(SpeedPercent(-30), self.in_to_mm(1.8), self.in_to_mm(2.4))
        self.on_for_distance(-80, 60, use_gyro=False)
