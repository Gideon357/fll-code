from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveDifferential, SpeedPercent, MoveTank, SpeedNativeUnits, Motor, SpeedValue
from ev3dev2.wheel import EV3Tire
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.sound import Sound
from .button import Button
from ev3dev2.console import Console
from time import sleep

# Config setting for Griffy
LEFT_MEDIUM_MOTOR_PORT = OUTPUT_A
LEFT_LARGE_MOTOR_PORT = OUTPUT_B
RIGHT_LARGE_MOTOR_PORT = OUTPUT_C
RIGHT_MEDIUM_MOTOR_PORT = OUTPUT_D
STUD_MM = 7
WHEEL_CLASS = EV3Tire
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
    Maybe Missions
    """

    def __init__(self):
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
        self.wheel_circumference = 17.9 # Need to add constant value
        # Put a sound at the end to show when it is done.
        self.start_tone()

    def start_tone(self):
        player = Sound()
        player.play_tone(500, 0.5, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

    def sleep_in_loop(self, sleep_time=0.01):
        sleep(sleep_time)

    def in_to_mm(self, inches):
        return inches * 25.4

    def line_square(self, speed, black_light_intensity=BLACK_LIGHT_INTENSITY, white_light_intensity=WHITE_LIGHT_INTENSITY):
        """
        Squares the robot to the line using the 
        selected speed 'speed' and the constant intensities
        """
        self.left_color_sensor.MODE_COL_REFLECT
        self.right_color_sensor.MODE_COL_REFLECT
        while self.right_color_sensor.reflected_light_intensity <= white_light_intensity:
            self.on(SpeedPercent(0), SpeedPercent(speed))
            self.sleep_in_loop
        self.off()
        while self.right_color_sensor.reflected_light_intensity >= black_light_intensity:
            self.on(SpeedPercent(0), SpeedPercent(speed))
            self.sleep_in_loop
        self.off()
        while self.right_color_sensor.reflected_light_intensity <= white_light_intensity:
            self.on(SpeedPercent(0), SpeedPercent(-speed))
            self.sleep_in_loop
        self.off()
        while self.right_color_sensor.reflected_light_intensity >= black_light_intensity:
            self.on(SpeedPercent(0), SpeedPercent(speed))
            self.sleep_in_loop
        self.off()
        while self.left_color_sensor.reflected_light_intensity <= white_light_intensity:
            self.on(SpeedPercent(-speed), SpeedPercent(0))
            self.sleep_in_loop
        self.off()
        while self.left_color_sensor.reflected_light_intensity >= black_light_intensity:
            self.on(SpeedPercent(speed), SpeedPercent(0))
            self.sleep_in_loop
        self.off()
        while self.left_color_sensor.reflected_light_intensity <= white_light_intensity:
            self.on(SpeedPercent(-speed), SpeedPercent(0))
            self.sleep_in_loop
        self.off()
        while self.left_color_sensor.reflected_light_intensity >= black_light_intensity:
            self.on(SpeedPercent(speed), SpeedPercent(0))
            self.sleep_in_loop
        self.off()
        
    def pid_line_follow(self, speed, black_light_intensity, white_light_intensity):
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
    
    def gyro_turn(self, degrees, speed):
        pass

    def on_for_distance(self, speed, distance_in, brake=True, block=True, use_gyro=True, kp=0.1, ki=0.1, kd=0.1, target=0):
        """
        Drives for a certain distance
        and has a toglable gyro feature
        TODO: Define Parameters so people know what they are for
        TODO: Explain gyro algorithm
        """
        distance_mm = self.in_to_mm(distance_in)
        if use_gyro:
            gyro = self.left_gyro_sensor
            gyro.reset()
            integral = 0.0
            last_error = 0.0
            derivative = 0.0
            # rotations = distance_mm / self.wheel_circumference
            # degrees = 360 * rotations
            self.reset(self.right_large_motor)
            self.reset(self.left_large_motor)
            speed_native_units = speed.to_native_units(self.left_large_motor)
            while True:
                error = target - gyro.angle
                integral = integral + error
                derivative = error - last_error
                last_error = error
                turn_native_units = (kp * error) + (ki * integral) + (kd * derivative)
                left_speed = speed_native_units(SpeedNativeUnits - turn_native_units)
                right_speed = speed_native_units(SpeedNativeUnits + turn_native_units)
                self.sleep_in_loop()
                self.on(left_speed, right_speed)
        else:
            super().on_for_distance(speed, distance_mm, brake, block)

    # def move(ki=0, kp=0, kd=0, target=0, drive_with_gyro=True):
    #     """ Moves the robot a specified amount of inches. Uses PID algorithim and the Gyro Sensor to correct drift"""
    #     if drive_with_gyro == True:
    #                 error = target - gyro.mode
    #                 integral = integral + error
    #                 derivative = error - last_error
    #                 last error = error
    #                 turn_native_units = (kp * error) + (ki * integral) + (kd * derivative)
    #                 if motor.position => m:
    #                     return False #If the motor has moved the correct amount, it ends the loop
    #                 else:
    #                     return True
    #         except: # If tacho motor does not initialize, it runs without gyro
    #             tank.on_for_rotations(LeftSpeed,RightSpeed,r)
    #             try:
    #                 console.text_at('An Exception Occured, Ran Without Gyro. Check Motor and Drivers', column=1, row=5, reset_console=True, inverse=True)
    #             except:
    #                 pass
    #         else:
    #             tank.on_for_rotations(LeftSpeed,RightSpeed,r)

    def first_run(self):
        """A Test Run"""
        self.on_for_distance(35, 390)
        self.on_for_distance(-75, 125)
        self.off
        self.on_arc_left(-80, self.in_to_mm(4), self.in_to_mm(15))
        self.off
        sleep(8)
        # make this an arc so we dont have to aim it
        self.on_for_distance(60, self.in_to_mm(37.5))
        self.off
        self.on_for_distance(60, self.in_to_mm(-8))
