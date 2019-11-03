from ev3dev2.console import Console
from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveDifferential, SpeedPercent, MoveTank, SpeedNativeUnits, Motor, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.wheel import EV3Tire
from sys import stderr
from time import sleep
from .button import Button


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
WHITE_LIGHT_INTENSITY = 44
BLACK_LIGHT_INTENSITY = 8
INCHES_TO_MILIMETERS = 25.4
LIGHTFILE = "/home/robot/light.txt"


class Griffy(MoveDifferential):
    """
    Created a Griffy Class based on MoveDifferential
    Adds:
    Move with Gyro
    Recreated PID Line Follower
    Drive until color
    Missions
    """

    def __init__(self, debug_on=True, light_from_file=False):
        """
        Initalize a griffy class which is based
        on move differential. Also set up the medium motors
        and all sensors.
        """
        super().__init__(LEFT_LARGE_MOTOR_PORT, RIGHT_LARGE_MOTOR_PORT, WHEEL_CLASS, WHEEL_DISTANCE)
        self.debug_on = debug_on
        error = self.set_up_sensors_motors()
        if not error is None:
            # wait until user exits program!!
            self.debug(error)
            self.error_tone()
            while True:
                self.sleep_in_loop()
        
        self.wheel_circumference = WHEEL_CIRCUMFERENCE
        self.attachment_tank = MoveTank(OUTPUT_A, OUTPUT_D, motor_class=MediumMotor)
        self.move_tank = MoveTank(OUTPUT_B, OUTPUT_C)
        self.white_light_intensity = WHITE_LIGHT_INTENSITY
        self.black_light_intensity = BLACK_LIGHT_INTENSITY
        if light_from_file:
            self.read_light_from_file()
        self.start_tone() # A sound at the end to show when it is done.
        # Set black and white in the init

    def debug(self, str):
        """Print to stderr the debug message ``str`` if self.debug is True."""
        if self.debug_on:
            print(str, file=stderr)

    def start_tone(self):
        player = Sound()
        player.play_tone(500, 0.5, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

    def error_tone(self):
        player = Sound()
        player.play_tone(750, 0.2, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        player.play_tone(250, 0.3, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        player.play_tone(750, 0.5, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        player.play_tone(250, 0.7, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

    def sleep_in_loop(self, sleep_time=0.1):
        sleep(sleep_time)

    def in_to_mm(self, inches):
        return inches * 25.4

    def line_square(self, speed, black_light_intensity=BLACK_LIGHT_INTENSITY, white_light_intensity=WHITE_LIGHT_INTENSITY):
        """
        Squares the robot to the line using the 
        selected speed 'speed' and the constant intensities
        """
        # Need to think of a way to involve all cases
        pass

    def choose_color_sensor(self, which_color_sensor='right'):
        """
        Returns the color sensor based on argument
        """
        if which_color_sensor == 'right':
            return self.right_color_sensor
        else:
            return self.left_color_sensor

    def write_to_console(self, msg, column, row, reset_console=True, inverse=False, alignment='L', font_size='M'):
        """Write msg to console at column, and row
        reset_console clears console first
        inverse reverses out text
        alignment: 'L', 'C', or 'R'
        font_size: 'S', 'M', 'L'
        Small: 8 rows, 22 columns
        Medium: 6 rows, 17 columns
        Large: 4 rows, 12 columns
        """
        console = Console()
        if font_size == 'S':
            console.set_font('Lat15-TerminusBoldVGA16.psf.gz', True)
        elif font_size == 'M':
            console.set_font('Lat15-Terminus20x10.psf.gz', True)
        else:
            console.set_font('Lat15-Terminus32x16.psf.gz', True)
        console.text_at(msg, column, row, reset_console=reset_console, inverse=inverse, alignment=alignment)

    def read_from_color_sensor(self, which_color_sensor='right', read_white=True):
        """
        Will show the value of the color sensor on the screen
        and return when any button is pressed
        TODO: Fix console display of light value which is changing size and location
        """
        cs = self.choose_color_sensor(which_color_sensor)
        cs.MODE_COL_REFLECT = 'COL-REFLECT'
        btn = Button()
        light = cs.reflected_light_intensity
        while not btn.any():
            self.write_to_console(str(light), column=5, row=2, reset_console=True, inverse=(not read_white), alignment='C', font_size='L')
            light = cs.reflected_light_intensity
            self.sleep_in_loop()
        return light

    def write_light_to_file(self, filename=LIGHTFILE):
        """
        Writes white and black light values to file system
        """
        self.debug(filename)
        white = self.read_from_color_sensor(read_white=True)
        black = self.read_from_color_sensor(read_white=False)
        with open(filename, 'w') as f:
            print("{} {}".format(white, black), file=f)

    def read_light_from_file(self, filename=LIGHTFILE):
        """
        Reads from light.txt and returns the white
        and black values as a tuple
        If error, catch exception, debug.print it, and return None
        """
        try:
            with open(filename, 'r') as f:
                line1 = f.readlines()[0]
            values = line1.split(" ")
            white = values[0].strip() # Removes \n if it exists
            black = values[1].strip() # Removes \n if it exists
            self.debug("Returning white and black values: ({}, {})".format(white, black))
            self.white_light_intensity = white
            self.black_light_intensity = black
            return (white, black)
        except Exception as e:
            self.debug("Error reading light: {}".format(e))
            return None

    def set_up_sensors_motors(self):
        """
        Creates all sensors and motors or returns None or the error
        """
        try:
            self.left_color_sensor = ColorSensor(LEFT_COLOR_SENSOR_INPUT)
            self.cs = self.left_color_sensor
            self.left_gyro_sensor = GyroSensor(LEFT_GYRO_SENSOR_INPUT)
            self.right_gyro_sensor = GyroSensor(RIGHT_GYRO_SENSOR_INPUT)
            self.right_color_sensor = ColorSensor(RIGHT_COLOR_SENSOR_INPUT)
            self.left_medium_motor = MediumMotor(LEFT_MEDIUM_MOTOR_PORT)
            self.right_medium_motor = MediumMotor(RIGHT_MEDIUM_MOTOR_PORT)
            self.left_large_motor = LargeMotor(LEFT_LARGE_MOTOR_PORT)
            self.right_large_motor = LargeMotor(RIGHT_LARGE_MOTOR_PORT)
        except Exception as e:
            self.write_to_console(str(e), column=1, row=3, reset_console=True, inverse=True, alignment='L', font_size='M')
            return e
        else:
            return None
        
    def drive_until_color(self, speed, color, which_color_sensor='right'):
        """
        drives at `SpeedPercent(speed)` until the specified color `stop_color`
        with chosen color sensor `which_color_sensor`
        TODO: add gyro support
        """
        cs = self.choose_color_sensor(which_color_sensor)
        cs.MODE_COL_COLOR = 'COL-COLOR'
        self.on(SpeedPercent(speed), SpeedPercent(speed))
        while not color == cs.color_name:
            self.sleep_in_loop()
        self.off()

    def drive_until_white_black(self, speed, which_color_sensor='left'):
        """
        drives at `SpeedPercent(speed)` until white `white_light_intensity`
        then black 'black_light_intensity' 
        with chosen color sensor `which_color_sensor`
        TODO: add gyro support
        """
        cs = self.choose_color_sensor(which_color_sensor)
        cs.MODE_COL_REFLECT = 'COL-REFLECT'
        self.on(SpeedPercent(speed), SpeedPercent(speed))
        while cs.reflected_light_intensity <= self.white_light_intensity:
            self.sleep_in_loop()
        while cs.reflected_light_intensity >= self.black_light_intensity:
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
        self.on_for_distance(SpeedPercent(30), 390, use_gyro=False)
        self.on_for_distance(SpeedPercent(-75), 125, use_gyro=False)
        self.on_arc_left(-80, self.in_to_mm(4), self.in_to_mm(15))
        sleep(8)
        # make this an arc so we dont have to aim it
        self.on_for_distance(SpeedPercent(60), 37.5, use_gyro=False)
        self.on_for_distance(SpeedPercent(-60), 8, use_gyro=False)

    def second_run(self):
        """Second robot run"""
        self.on_for_distance(SpeedPercent(30), 24.5, use_gyro=False)
        self.attachment_raise_lower(10, 1)
        self.on_for_distance(SpeedPercent(30), 3, use_gyro=False)
        self.on_for_distance(SpeedPercent(-75), 21, use_gyro=False)

    def third_run(self):
        """Crane: 4"""
        self.on_for_distance(SpeedPercent(30), 10, use_gyro=False)
        self.move_tank.on_for_rotations(-20,20, .145)
        self.on_for_distance(SpeedPercent(-30), 13, use_gyro=False)
        self.on_for_distance(SpeedPercent(25), 24.5, use_gyro=False)
        sleep(1)
        self.on_for_distance(SpeedPercent(-30), 2, use_gyro=False)
        self.on_arc_left(SpeedPercent(-50), self.in_to_mm(6), self.in_to_mm(24))

    def fourth_run(self):
        """Broken building elevator and swing: 7"""
        # 90 degrees is `self.in_to_mm(1.8), self.in_to_mm(3.5)`
        self.on_for_distance(SpeedPercent(30), 1.1, use_gyro=False) # Go 1.1 inches forward
        self.move_tank.on_for_rotations(15, -15, .395) # Turn to the right
        self.on_for_distance(SpeedPercent(50), 35.4, use_gyro=False) # Go to the beige circle
        self.on_for_distance(SpeedPercent(-20), 5, use_gyro=False) # Backup from the houses we put
        self.move_tank.on_for_rotations(15, -15, .15) # Turn past the houses
        self.left_medium_motor.on_for_rotations(100, .28) # Turn attachment
        self.move_tank.on_for_rotations(15, -15, .02) # Turn to the right
        self.on_for_distance(SpeedPercent(30), 8.5, use_gyro=False) # Go forward 8.5 inches
        self.left_medium_motor.on_for_rotations(75, .125) # Turn attachment
        self.move_tank.on_for_rotations(-15, 15, .085) # Tiny turn to adjust
        self.on_for_distance(SpeedPercent(30), 7, use_gyro=False) # Go forward 7 inches
        # self.on_arc_right(SpeedPercent(50), self.in_to_mm(1.8), self.in_to_mm(1.2))
        # self.on_arc_left(SpeedPercent(30), self.in_to_mm(1.8), self.in_to_mm(.5))
        # self.on_for_distance(SpeedPercent(-20), 5, use_gyro=False)
        # self.on_arc_right(SpeedPercent(30), self.in_to_mm(1.8), self.in_to_mm(2.65))
        # self.on_for_distance(SpeedPercent(30), 7, use_gyro=False)
        # self.on_for_distance(SpeedPercent(-30), 5, use_gyro=False)
        # self.on_arc_right(SpeedPercent(-30), self.in_to_mm(1.8), self.in_to_mm(2.8))
        # self.on_for_distance(-80, 55, use_gyro=False)