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
        self.on_for_distance(SpeedPercent(-60), 15.5) # Go backward at 100 power all of the way to the wall
        self.on_for_distance(SpeedPercent(50), .35) # Move a small amount off of the wall
        self.move_tank.on_for_rotations(100, -100, .63) # Turn to the right 90 degrees
        self.on_for_distance(50, 20) # Go to the Traffic Jam
        self.move_tank.on_for_rotations(100, -100, .15) # Turn to the right and hit it up
        sleep(0.25)
        self.on_for_distance(-100, 31) # Go back home at 100 power
        self.move_tank.on_for_rotations(100, -100, .62) # Turn to the right

    def third_run(self):
        """Traffic Jam Extra"""
        self.on_for_distance(70, 19) # Go to the Traffic Jam
        self.move_tank.on_for_rotations(100, -100, .15) # Turn to the right and hit it up
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
        self.on_for_distance(100, 10.5)
        self.on_for_distance(-100, 11)
        self.move_tank.on_for_rotations(100, -100, .27)
        self.on_for_distance(-100, 20)
    
    def sixth_run(self):
        """Broken building elevator and swing: Jig"""
        
        self.left_medium_motor.on_for_rotations(100, .0001)
        self.on_for_distance(30, 26)
        self.left_medium_motor.on_for_rotations(25, .35)
        sleep(1)
        self.on_for_distance(30, 15)
        self.move_tank.on_for_rotations(20, -20, .035)
        self.on_for_distance(30, 5.5)
        self.move_tank.on_for_rotations(-20, 20, .14)
        self.move_tank.on_for_rotations(20, -20, .14)
        self.on_for_distance(-30, 6)

        # 90 degrees is `self.in_to_mm(1.8), self.in_to_mm(3.5)`
        # self.left_medium_motor.on_for_rotations(-80, .2) # Turn attachment
        # sleep(.5)
        # self.move_tank.on_for_rotations(SpeedPercent(-25), 25, .109) # Turn to the left
        # self.on_for_distance(SpeedPercent(50), 38) # Go to the beige circle
        # self.left_medium_motor.on_for_seconds(10, 0.57) # Turn attachment
        # self.on_for_distance(SpeedPercent(-20), 5.5) # Backup from the houses we put
        # self.move_tank.on_for_rotations(25, -25, .18) # Turn past the houses
        # self.left_medium_motor.on_for_seconds(-50, 0.9) # Turn attachment
        # sleep(1)
        # self.on_for_distance(SpeedPercent(60), 13.5) # Go forward 13.5 inches
        # sleep(1)
        # self.on_for_distance(SpeedPercent(30), 3) # Go forward 3 inches
        # self.move_tank.on_for_rotations(15, -15, .14) # Turn to the right
        # self.move_tank.on_for_rotations(-15, 15, .14) # Turn to the left
        # self.on_for_distance(SpeedPercent(-20), 4) # Back up
        # self.left_medium_motor.on_for_rotations(75, .32) # Turn attachment
        # self.move_tank.on_for_rotations(25, -25, .349) # Turn to the right
        # self.on_for_distance(SpeedPercent(30), 8.5) # Go forward to swing
        # self.move_tank.on_for_rotations(-25, 25, .2) # Turn to the left
        # self.on_for_distance(SpeedPercent(-30), 7) # Go backward from swing
        # self.move_tank.on_for_rotations(-25, 25, .29) # Turn to the left
        # self.on_for_distance(-80, 60) # Go 60 inches backwards, arriving home
        
    def seventh_run(self):
        """Ramp: Jig """
        self.move_tank.on_for_rotations(-15, 15, .13) # Turn to the left
        self.on_for_distance(-50, 34.8) # Go forward 34.8 inches to align with the bridge
        self.move_tank.on_for_rotations(-15, 15, .58) # Turn to the right
        self.on_for_distance(-60, 21.2) # Go backward 21.2 inches, getting up the bridge
