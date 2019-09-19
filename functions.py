"""
This will convert in/cm to rotations, be sure to use either metric or imperial for all params.
The formula is wheel circumfrence/distance. r is the number of rotations.
TODO:
add a default size once decided
add turning (see link in the turn function)
"""
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

def move(size, distance_inches, speed):
	rotations = distance/size
	tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), rotations)
def turn():
	pass