"""
This will convert in/cm to rotations, be sure to use either metric or imperial for all params.
TODO:
add a default size once decided
Please see the bottom of the code for a call example.
"""
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
import math
#math allows for PI in equations, import all the other things for all EV3dev programs


Class moveBlock():
	# creates a class called "moveBlock"
	def __init__(self,size,distance, speed = 75):
		#initializes every object with params size,distance, speed
		self.c = size        
		self.distance = dist
		self.speed = speed
	def move(self):
		r = d/c
		tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), r)
	def turn(self):
	 #https://va-dcfll.org/distance-to-rotation-formula/ for formula for turning.
	 
"""
How to call this object:
1) initalize from this code:
RIPGerhard = moveBlock(size of wheel, distance, desired speed (automatically at 75)
RIPGerard.move()
2) initialize from another code (change user/root to your home directory):
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
import griffy-dev2/moveInches.py as program
from program import moveBlock
ParallelLinesHaveSoMuchInCommonItsAShameTheyNeverMeet = moveBlock(size of wheel, distance, desired speed (automatically at 75)
ParallelLinesHaveSoMuchInCommonItsAShameTheyNeverMeet.move()
"""