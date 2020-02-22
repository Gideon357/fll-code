#!/usr/bin/env micropython

from .griffy import Griffy
from ev3dev2.motor import SpeedPercent
from sys import stderr
from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.led import Leds
from ev3dev2.sensor import list_sensors, INPUT_1, INPUT_2, INPUT_3, INPUT_4
from time import sleep

class Missions(Griffy):
    """
    Missions has all of the missions we run and is based of of griffy
    """

    def first_run(self):
        """Crane: 4"""
        self.on_for_distance(SpeedPercent(40), 24.5) # Go forward 24.5 inches to the crane
        sleep(1) # Wait for 1 second
        self.on_for_distance(SpeedPercent(-30), 4) # Slowly back out
        self.on_arc_left(SpeedPercent(-80), self.in_to_mm(4.8), self.in_to_mm(22)) # Arc back into base

    def second_run(self):
        """Buildings and Traffic Jam, Innovation: 2"""
        self.on_for_distance(SpeedPercent(25), 15) # Go forward 15 inches to drop off the houses
        sleep(0.5)
        self.on_for_distance(SpeedPercent(-60), 14) # Go backward at 100 power all of the way to the wall
        self.move_tank.on_for_rotations(100, -100, .63) # Turn to the right 90 degrees
        self.on_for_distance(50, 19) # Go to the Traffic Jam
        self.move_tank.on_for_rotations(100, -100, .3) # Turn to the right and hit it up
        sleep(0.25)
        self.move_tank.on_for_rotations(-50, 50, .05) # Turn to the right and hit it up
        self.on_for_distance(-100, 31) # Go back home at 100 power
        self.move_tank.on_for_rotations(-100, 100, .62) # Turn to the right

    def third_run(self):
        """Traffic Jam Extra"""
        self.on_for_distance(70, 19) # Go to the Traffic Jam
        self.move_tank.on_for_rotations(100, -100, .3) # Turn to the right and hit it up
        self.move_tank.on_for_rotations(-50, 50, .05) # Turn to the right and hit it up
        self.on_for_distance(-100, 31) # Go back home at 100 power
        self.move_tank.on_for_rotations(100, -100, .62) # Turn to the right
    
    def fourth_run(self):
        """Treehouse: Aim"""
        self.on_for_distance(SpeedPercent(30), 23) # Go forward 23 inches to the treehouse
        self.on_for_distance(SpeedPercent(15), 2) # Drop in the cubes moving forward slowly
        self.on_for_distance(SpeedPercent(-10), 2.5) # Slowly back away from tree
        self.on_for_distance(SpeedPercent(-100), 21.5) # Go backwards 21.5 inches forcing the attachment off
        self.move_tank.on_for_rotations(25, -25, .25) # Turn to the right
        self.on_for_distance(SpeedPercent(-75), 12) # Go backwards 12 inches into base

    def fifth_run(self):
        """Self Structure: Aim"""
        self.on_for_distance(100, 11) # Go forward to circle
        self.on_for_distance(-100, 11) # Back up from circle
        self.move_tank.on_for_rotations(100, -100, .27) # Turn right
        self.on_for_distance(-100, 20) # Back up to wall
    
    def sixth_run(self):
        """Broken building elevator and swing: Jig"""
        self.on_for_distance(50, 60, use_gyro=True) # Go forward 60 inches using the PID gyro algorthm
        self.move_tank.on_for_rotations(-8, 8, .2) # Turn left
        self.move_tank.on_for_rotations(8, -8, .2) # Turn right
        self.on_for_distance(-30, 12) # Back up
        self.on_for_distance(30, 12) # Go again to double check the swing
        self.on_for_distance(-30, 12) # Back up
        self.move_tank.on_for_rotations(-8, 8, .225) # Turn to elevator
        self.left_medium_motor.on_for_rotations(30, .56) # Turn attachment
        self.on_for_distance(50, 11.5) # Go and hit over evelator
        self.on_for_distance(-10, 10) # Slowly back up
        self.move_tank.on_for_rotations(8, -8, .22) # Turn right
        self.on_for_distance(-100, 50) # Go home
        self.left_medium_motor.on_for_rotations(-30, .45) # Turn attachment
        
    def seventh_run(self):
        """Ramp: Jig """
        self.on_for_distance(30, 43, use_gyro=True) # Go forward 43 inches to drop off cubes
        self.on_for_distance(-20, 8) # Back up
        self.line_square(20) # Line square roughly
        self.line_square(20, which_algo='fine') # Fine line square
        self.on_for_distance(20, 2) # Go forward 2 inches
        self.move_tank.on_for_rotations(-15, 15, .52) # Turn to the left
        self.on_for_distance(60, 24, use_gyro=True) # Go 24 inches, getting up the bridge