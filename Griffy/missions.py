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
        self.on_for_distance(SpeedPercent(30), 10)
        self.move_tank.on_for_rotations(-20,20, .19)
        self.on_for_distance(SpeedPercent(-30), 13)
        self.on_for_distance(SpeedPercent(25), 24.5)
        sleep(1)
        self.on_for_distance(SpeedPercent(-30), 2)
        self.on_arc_left(SpeedPercent(-50), self.in_to_mm(6), self.in_to_mm(25))

    def second_run(self):
        """Buildings, Innovation: 2"""
        self.on_for_distance(SpeedPercent(30), 15.4)
        self.on_for_distance(SpeedPercent(-75), 6)
        self.on_arc_left(-80, self.in_to_mm(4), self.in_to_mm(15))
    
    def third_run(self):
        """Treehouse: Aim"""
        self.on_for_distance(SpeedPercent(30), 21)
        self.on_for_distance(SpeedPercent(10), 4.5)
        self.on_for_distance(SpeedPercent(-10), 1.5)
        self.on_for_distance(SpeedPercent(-65), 21.5)
        self.move_tank.on_for_rotations(25, -25, .25) # Turn to the right
        self.on_for_distance(SpeedPercent(-75), 12)

    def fourth_run(self):
        """Traffic Jam: 2"""
        self.on_for_distance(50, 22)
        self.move_tank.on_for_rotations(15, -15, .1)
        self.move_tank.on_for_rotations(-15, 15, .1)
        self.on_for_distance(-100, 36)
        # add turn and lower back

    def fifth_run(self):
        """Broken building elevator and swing: Jig"""
        # 90 degrees is `self.in_to_mm(1.8), self.in_to_mm(3.5)`
        self.left_medium_motor.on_for_rotations(-80, .1) # Turn attachment
        sleep(.5)
        self.move_tank.on_for_rotations(SpeedPercent(-25), 25, .1125)
        self.on_for_distance(SpeedPercent(50), 38) # Go to the beige circle
        self.left_medium_motor.on_for_seconds(10, 0.6) # Turn attachment
        self.on_for_distance(SpeedPercent(-20), 5.5) # Backup from the houses we put
        self.move_tank.on_for_rotations(25, -25, .16) # Turn past the houses
        self.left_medium_motor.on_for_seconds(-50, 0.9) # Turn attachment
        sleep(1)
        self.on_for_distance(SpeedPercent(60), 13.3) # Go forward 13 inches
        sleep(1)
        self.on_for_distance(SpeedPercent(30), 4.25) # Go forward 7 inches
        self.move_tank.on_for_rotations(15, -15, .1) # Turn to the right
        self.move_tank.on_for_rotations(-15, 15, .1) # Turn to the left
        self.on_for_distance(SpeedPercent(-20), 4) # Back up
        self.left_medium_motor.on_for_rotations(75, .15) # Turn attachment
        self.move_tank.on_for_rotations(25, -25, .36) # Turn to the right
        self.on_for_distance(SpeedPercent(30), 7)
        self.move_tank.on_for_rotations(-25, 25, .2) # Turn to the left
        self.on_for_distance(SpeedPercent(-30), 9)
        self.on_for_distance(SpeedPercent(30), 3)
        self.move_tank.on_for_rotations(-25, 25, .28) # Turn to the right
        self.on_for_distance(-80, 60)
    
    def sixth_run(self):
        self.move_tank.on_for_rotations(-15, 15, .13)
        self.on_for_distance(-50, 34.8)
        self.move_tank.on_for_rotations(-15, 15, .55)
        self.on_for_distance(-60, 21.2)

    def drone_run(self):
        self.on_for_distance(50, 30)
        self.left_medium_motor.on_for_rotations(50, 1)
        self.on_for_distance(-50, 30)