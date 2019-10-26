from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveDifferential, SpeedPercent, MoveTank, SpeedNativeUnits, Motor
from ev3dev2.wheel import EV3Tire
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.sound import Sound
from .button import Button
from sys import stderr
from time import sleep


# Config setting for Griffy
LEFT_MEDIUM_MOTOR_PORT = OUTPUT_A
LEFT_LARGE_MOTOR_PORT = OUTPUT_B
RIGHT_LARGE_MOTOR_PORT = OUTPUT_C
RIGHT_MEDIUM_MOTOR_PORT = OUTPUT_D
STUD_MM = 7
WHEEL_CLASS = EV3Tire
WHEEL_CIRCUMFERENCE = 17.9
WHEEL_DISTANCE = STUD_MM * 11 # Center of wheels are 11 studs apart
LEFT_GYRO_SENSOR_INPUT = INPUT_1
LEFT_COLOR_SENSOR_INPUT = INPUT_2
RIGHT_COLOR_SENSOR_INPUT = INPUT_3
RIGHT_GYRO_SENSOR_INPUT = INPUT_4
WHITE_LIGHT_INTENSITY = 46
BLACK_LIGHT_INTENSITY = 8
INCHES_TO_MILIMETERS = 25.4


class Griffy(MoveDifferential):
    """
    Created a Griffy Class based on MoveDifferential
    Adds:
    Move with Gyro
    Recreated PID Line Follower
    Drive until color
    Missions
    """

    def __init__(self, debug_on=True):
        """
        Initalize a griffy class which is based
        on move differential. Also set up the medium motors
        and all sensors.
        """
        super().__init__(LEFT_LARGE_MOTOR_PORT, RIGHT_LARGE_MOTOR_PORT, WHEEL_CLASS, WHEEL_DISTANCE)
        self.left_color_sensor = ColorSensor(LEFT_COLOR_SENSOR_INPUT)
        self.cs = self.left_color_sensor
        self.left_gyro_sensor = GyroSensor(LEFT_GYRO_SENSOR_INPUT)
        self.right_gyro_sensor = GyroSensor(RIGHT_GYRO_SENSOR_INPUT)
        self.right_color_sensor = ColorSensor(RIGHT_COLOR_SENSOR_INPUT)
        self.left_medium_motor = MediumMotor(LEFT_MEDIUM_MOTOR_PORT)
        self.right_medium_motor = MediumMotor(RIGHT_MEDIUM_MOTOR_PORT)
        self.left_large_motor = LargeMotor(LEFT_LARGE_MOTOR_PORT)
        self.right_large_motor = LargeMotor(RIGHT_LARGE_MOTOR_PORT)
        self.wheel_circumference = WHEEL_CIRCUMFERENCE
        self.attachment_tank = MoveTank(OUTPUT_A, OUTPUT_D, motor_class=MediumMotor)
        self.debug_on = debug_on
        self.start_tone() # A sound at the end to show when it is done.

    def debug(self, str):
        """Print to stderr the debug message ``str`` if self.debug is True."""
        if self.debug_on:
            print(str, file=stderr)

    def start_tone(self):
        player = Sound()
        player.play_tone(500, 0.5, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

    def sleep_in_loop(self, sleep_time=0.1):
        sleep(sleep_time)

    def in_to_mm(self, inches):
        return inches * 25.4

    def line_square(self, speed, black_light_intensity=BLACK_LIGHT_INTENSITY, white_light_intensity=WHITE_LIGHT_INTENSITY):
        """
        Squares the robot to the line using the 
        selected speed 'speed' and the constant intensities
        """
        # Need to think o a way to involve all cases
        pass

    def drive_until_color(self, speed, color, which_color_sensor='right'):
        """
        drives at `SpeedPercent(speed)` until the specified color `stop_color`
        with chosen color sensor `which_color_sensor`
        TODO: add gyro support
        """
        if which_color_sensor == 'right':
            cs = self.right_color_sensor
        else:
            cs = self.left_color_sensor
        cs.MODE_COL_COLOR = 'COL-COLOR'
        self.on(SpeedPercent(speed), SpeedPercent(speed))
        while not color == cs.color_name:
            self.sleep_in_loop()
        self.off()

    def drive_until_white_black(self, speed, black_light_intensity=BLACK_LIGHT_INTENSITY, white_light_intensity=WHITE_LIGHT_INTENSITY, which_color_sensor='left'):
        """
        drives at `SpeedPercent(speed)` until white `white_light_intensity`
        then black 'black_light_intensity' 
        with chosen color sensor `which_color_sensor`
        TODO: add gyro support
        """
        if which_color_sensor == 'right':
            cs = self.right_color_sensor
        else:
            cs = self.left_color_sensor
        cs.MODE_COL_REFLECT = 'COL-REFLECT'
        self.on(SpeedPercent(speed), SpeedPercent(speed))
        while cs.reflected_light_intensity <= white_light_intensity:
            self.sleep_in_loop()
        while cs.reflected_light_intensity >= black_light_intensity:
            self.sleep_in_loop()
        self.off()
    
    def attachment_raise_lower(self, speed, rotations):
        """
        Raises and lowers the medium motors as a tank
        """
        self.attachment_tank.on_for_rotations(speed, -speed, rotations)

    def on_for_distance(self, speed, distance_in, brake=True, block=True, use_gyro=True, kp=0.6, ki=0.5, kd=0.6, target=0):
        """
        Drives for a certain distance
        and has a toglable gyro feature
        HIGHLY SUGGESTED TO NOT CHANGE K VALUES
        TODO: Define Parameters so people know what they are for
        TODO: Explain gyro algorithm
        TODO: Add comments throughout

        ``speed`` can be a percentage or a :class:`ev3dev2.motor.SpeedValue`
        object, enabling use of other units.
        """
        # self.reset()
        distance_mm = self.in_to_mm(distance_in)
        if use_gyro:
            gyro = self.right_gyro_sensor
            gyro.mode = gyro.MODE_GYRO_ANG
            # there is currently a bug in gyro.reset() method so instead we just read the current
            # angle and then compare to that
            # gyro.reset()
            reset_angle = gyro.angle
            self.debug("GYRO ANGLE BEFORE LOOP: {}".format(gyro.angle))
            
            # convert speed to a SpeedValue if not already
            speed_native_units = self.left_motor._speed_native_units(speed)
            integral = 0.0 # integral is the sum of all errors
            last_error = 0.0 # last_error stores the last error through the while loop
            derivative = 0.0  # derivative is the rate at which the error is changing
            # rotations = distance_mm / self.wheel_circumference
            # degrees = 360 * rotations
            # self.left_large_motor.reset()
            # self.right_large_motor.reset()        
            while True:
                #error = target - gyro.angle - reset_angle
                error = gyro.angle - reset_angle
                integral = integral + error
                derivative = error - last_error
                last_error = error
                turn_native_units = (kp * error) + (ki * integral) + (kd * derivative)
                left_speed = SpeedNativeUnits(speed_native_units - turn_native_units)
                right_speed = SpeedNativeUnits(speed_native_units + turn_native_units)
                self.debug("error: {}, integral: {}, derivative: {}, last_error: {}, turn_native_units: {}, left_speed: {}, right_speed: {}".format(error, integral, derivative, last_error, turn_native_units, left_speed, right_speed))
                self.on(left_speed, right_speed)
                self.sleep_in_loop(0.01)
        else:
            super().on_for_distance(speed, distance_mm, brake, block)

    def first_run(self):
        """First robot run"""
        self.on_for_distance(SpeedPercent(30), self.in_to_mm(390), use_gyro=False)
        self.on_for_distance(SpeedPercent(-75), self.in_to_mm(125), use_gyro=False)
        self.on_arc_left(-80, self.in_to_mm(4), self.in_to_mm(15))
        sleep(8)
        # make this an arc so we dont have to aim it
        self.on_for_distance(SpeedPercent(60), self.in_to_mm(37.5), use_gyro=False)
        self.on_for_distance(SpeedPercent(60), self.in_to_mm(-8), use_gyro=False)

    def second_run(self):
        """Second robot run"""
        self.on_for_distance(SpeedPercent(30), self.in_to_mm(24.5), use_gyro=False)
        self.attachment_raise_lower(10, 1)
        self.on_for_distance(SpeedPercent(30), self.in_to_mm(3), use_gyro=False)
        self.on_for_distance(SpeedPercent(-75), self.in_to_mm(21), use_gyro=False)

    def third_run(self):
        """Third robot run"""
        self.on_for_distance(SpeedPercent(30), self.in_to_mm(24.5), use_gyro=False)
        self.on_for_distance(SpeedPercent(-30), self.in_to_mm(10), use_gyro=False)

    def fourth_run(self):
        """Fourth robot run"""
        self.on_for_distance(SpeedPercent(30), self.in_to_mm(24.5), use_gyro=False)
        sleep(1)
        self.on_for_distance(SpeedPercent(-30), self.in_to_mm(10), use_gyro=False)

    def fifth_run(self):
        """Fifth robot run"""
        self.on_for_distance(SpeedPercent(30), self.in_to_mm(24.5), use_gyro=False)
        self.on_arc_left(SpeedPercent(40), self.in_to_mm(1), self.in_to_mm(15))
        self.on_for_distance(SpeedPercent(-30), self.in_to_mm(10), use_gyro=False)