from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveDifferential
from ev3dev2.wheel import EV3Tire
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.sound import Sound
from button import Button
from time import sleep

# Config setting for Griffy
LEFT_MEDIUM_MOTOR_PORT = OUTPUT_A
LEFT_LARGE_MOTOR_PORT = OUTPUT_B
RIGHT_LARGE_MOTOR_PORT = OUTPUT_C
RIGHT_MEDIUM_MOTOR_PORT = OUTPUT_D
STUD_MM = 7
WHEEL_CLASS = EV3Tire
WHEEL_DISTANCE = STUD_MM * 11 # Center of wheels are 11 studs apart
LEFT_COLOR_SENSOR_INPUT = INPUT_1
LEFT_GYRO_SENSOR_INPUT = INPUT_2
RIGHT_GYRO_SENSOR_INPUT = INPUT_3
RIGHT_COLOR_SENSOR_INPUT = INPUT_4

class Griffy(MoveDifferential):
    """
    Created a Griffy Class based on MoveDifferential
    Adds:
    Move with Gyro
    Recreated PID Line Follower
    Drive until color
    Maybe Missions
    """

    def __init__(self):
        """
        Initalize a griffy class which is based
        on move differential. Also set up the medium motors
        and all sensors.
        """
        super().__init__(LEFT_LARGE_MOTOR_PORT, RIGHT_LARGE_MOTOR_PORT, WHEEL_CLASS, WHEEL_DISTANCE)
        self.left_color_sensor = LEFT_COLOR_SENSOR_INPUT
        self.left_gyro_sensor = LEFT_GYRO_SENSOR_INPUT
        self.right_gyro_sensor = RIGHT_GYRO_SENSOR_INPUT
        self.right_color_sensor = RIGHT_COLOR_SENSOR_INPUT
        self.left_medium_motor = LEFT_MEDIUM_MOTOR_PORT
        self.right_medium_motor = RIGHT_MEDIUM_MOTOR_PORT

    def on_for_distance(self, speed, distance):
        pass

    def line_square(self, black_light_intensity, white_light_intensity):
        pass

    def pid_line_follow(self, black_light_intensity, white_light_intensity, speed):
        pass

    def dive_until_color(self, speed):
        pass

    def gyro_turn(self, degrees, speed):
        pass