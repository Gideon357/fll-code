"""
This will convert in/cm to rotations, be sure to use either metric or imperial for all params.
TODO:
add a default size once decided
add turning (see link in the turn function)
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
	def move(size, distance, speed = 75):
		c = size        
		distance = dist
		speed = speed
		r = d/c
		tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), r)
	def turn():
	 #https://va-dcfll.org/distance-to-rotation-formula/ for formula for turning.
