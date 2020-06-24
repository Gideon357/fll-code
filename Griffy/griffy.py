from sys import stderr
from time import sleep

from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.led import Leds
from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor,
                           MediumMotor, Motor, MoveDifferential, MoveSteering,
                           MoveTank, SpeedNativeUnits, SpeedPercent,
                           follow_for_ms)
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.sound import Sound
from ev3dev2.wheel import EV3Tire

from .settings import Settings

# Config setting for Griffy
LEFT_MEDIUM_MOTOR_PORT = OUTPUT_A
LEFT_LARGE_MOTOR_PORT = OUTPUT_B
RIGHT_LARGE_MOTOR_PORT = OUTPUT_C
RIGHT_MEDIUM_MOTOR_PORT = OUTPUT_D
STUD_MM = 7
WHEEL_CLASS = EV3Tire
WHEEL_CIRCUMFERENCE = 176
WHEEL_DISTANCE = STUD_MM * 11  # Center of wheels are 11 studs apart
LEFT_GYRO_SENSOR_INPUT = INPUT_1
LEFT_COLOR_SENSOR_INPUT = INPUT_2
RIGHT_COLOR_SENSOR_INPUT = INPUT_3
RIGHT_GYRO_SENSOR_INPUT = INPUT_4
WHITE_LIGHT_INTENSITY = 44
BLACK_LIGHT_INTENSITY = 8
LINE_LIGHT_INTENSITY = 26
INCHES_TO_MILIMETERS = 25.4
USE_GYRO = True  # Global constant to turn on and off gyro driving
SETTINGSFILE = "/home/robot/griffy-dev2/settings.json"


class Griffy(MoveDifferential):
    """
    Created a Griffy Class based on MoveDifferential
    Adds:
    Move with Gyro
    Recreated PID Line Follower
    Drive until color
    Missions
    """

    def __init__(self, debug_on=True, settings_file=SETTINGSFILE):
        """
        Initalize a griffy class which is based
        on move differential. Also set up the medium motors
        and all sensors.
        """
        super().__init__(
            LEFT_LARGE_MOTOR_PORT, RIGHT_LARGE_MOTOR_PORT, WHEEL_CLASS, WHEEL_DISTANCE
        )
        self.settings = Settings(settings_file)
        self.debug_on = self.settings.get("debug_on", debug_on)
        self.debug("Griffy started!")
        error = self.set_up_sensors_motors()
        if not error is None:
            # wait until user exits program!!
            self.debug(error)
            self.error_tone()
            while True:
                self.sleep_in_loop()
        self.calibrate_gyro(which_gyro_sensor="right")

        self.wheel_circumference = WHEEL_CIRCUMFERENCE
        self.attachment_tank = MoveTank(OUTPUT_A, OUTPUT_D, motor_class=MediumMotor)
        self.move_tank = MoveTank(OUTPUT_B, OUTPUT_C)
        self.read_light_from_settings()  # read light from settings files via Settings class
        self.use_gyro = self.settings.get("use_gyro", USE_GYRO)

        self.start_tone()  # A sound at the end to show when it is done.
        # Set black and white in the init

    def debug(self, str):
        """Print to stderr the debug message ``str`` if self.debug is True."""
        if self.debug_on:
            print(str, file=stderr)

    def start_tone(self):
        player = Sound()
        player.play_tone(
            500, 0.5, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE
        )

    def error_tone(self):
        player = Sound()
        player.play_tone(
            750, 0.2, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE
        )
        player.play_tone(
            250, 0.3, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE
        )
        player.play_tone(
            750, 0.5, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE
        )
        player.play_tone(
            250, 0.7, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE
        )

    def sleep_in_loop(self, sleep_time=0.1):
        sleep(sleep_time)

    def in_to_mm(self, inches):
        return inches * 25.4

    def set_led(self, color="GREEN"):
        self.leds.set_color("LEFT", color)
        self.leds.set_color("RIGHT", color)

    def line_square(self, speed, which_algo="rough"):
        """
        Two options for line squaring:
        option 1: Squares the robot with a line using the provided `black_light_intensity`
                  and `white_light_intesity`.
        option 2: Squares using alternative line squaring algorithm
        """
        if which_algo == "loop":
            while True:
                self.left_large_motor.on(speed=SpeedPercent(speed))
                self.right_large_motor.on(speed)
                if self.right_color_sensor.reflected_light_intensity == 1:
                    self.right_large_motor.off()
                elif self.left_color_sensor.reflected_light_intensity == 1:
                    self.left_large_motor.off()
                elif self.right_color_sensor.reflected_light_intensity == 6:
                    self.right_large_motor.on(speed=SpeedPercent(5))
                elif self.right_color_sensor.reflected_light_intensity == 6:
                    self.left_large_motor.on(speed=SpeedPercent(5))
                elif (
                    self.right_color_sensor.reflected_light_intensity == 1
                    and self.left_color_sensor.reflected_light_intensity == 1
                ):
                    break
        elif which_algo == "fine":
            # square using fine adjustments
            # generally to be used after a rought adjustments
            # TODO: turn LED to TK so we know we're fine adjusting
            # TODO: only loop for max_seconds
            while True:
                # first the left sensor and motor
                if (
                    self.left_color_sensor.reflected_light_intensity
                    < self.line_square_intensity
                ):
                    # Griffy too far forward, move backwards
                    self.left_large_motor.on(-speed)
                elif (
                    self.left_color_sensor.reflected_light_intensity
                    > self.line_square_intensity
                ):
                    # Griffy too gar back, move forward
                    self.left_large_motor.on(speed)
                else:
                    # we are there, turn off left motor and idle
                    self.left_large_motor.off()
                    break
            while True:
                # next the right sendors and motor
                if (
                    self.right_color_sensor.reflected_light_intensity
                    < self.line_square_intensity
                ):
                    # Griffy too far forward, move backwards
                    self.right_large_motor.on(-speed)
                elif (
                    self.right_color_sensor.reflected_light_intensity
                    > self.line_square_intensity
                ):
                    # Griffy too far back, move forward
                    self.right_large_motor.on(speed)
                else:
                    # we are there, turn off left motor and idle
                    self.right_large_motor.off()
                    break
        elif which_algo == "rough":
            self.on(speed, speed)
            while (
                self.right_color_sensor.reflected_light_intensity
                > self.black_light_intensity
                and self.left_color_sensor.reflected_light_intensity
                > self.black_light_intensity
            ):
                self.debug(
                    "left light intensity: {}, right light intensity: {}".format(
                        self.left_color_sensor.reflected_light_intensity,
                        self.right_color_sensor.reflected_light_intensity,
                    )
                )
            if (
                self.right_color_sensor.reflected_light_intensity
                <= self.black_light_intensity
            ):
                self.right_large_motor.off()
                self.debug("shutting right motor")
                while (
                    self.left_color_sensor.reflected_light_intensity
                    > self.black_light_intensity
                ):
                    self.debug(
                        "left light intensity: {}, right light intensity: {}".format(
                            self.left_color_sensor.reflected_light_intensity,
                            self.right_color_sensor.reflected_light_intensity,
                        )
                    )
                self.left_large_motor.off()
                self.debug("shutting left motor")
            else:
                self.left_large_motor.off()
                self.debug("shutting left motor")
                while (
                    self.right_color_sensor.reflected_light_intensity
                    > self.black_light_intensity
                ):
                    self.debug(
                        "left light intensity: {}, right light intensity: {}".format(
                            self.left_color_sensor.reflected_light_intensity,
                            self.right_color_sensor.reflected_light_intensity,
                        )
                    )
                self.right_large_motor.off()
                self.debug("shutting right motor")

    def display_color_sensor(self, which_color_sensor):
        """Display reflected light intensity of said sensor"""
        cs = self.choose_color_sensor(which_color_sensor)
        cs.MODE_COL_REFLECT = "COL-REFLECT"
        btn = Button()
        light = cs.reflected_light_intensity
        while True:
            self.write_to_console(
                str(light),
                column=5,
                row=2,
                reset_console=True,
                inverse=True,
                alignment="C",
                font_size="L",
            )
            light = cs.reflected_light_intensity
            self.sleep_in_loop()
            if btn.any():
                break

    def display_gyro_sensor(self, which_gyro_sensor):
        """Display reflected light intensity of said sensor"""
        gyro = self.choose_gyro_sensor(which_gyro_sensor)
        gyro.mode = gyro.MODE_GYRO_ANG
        btn = Button()
        angle = gyro.angle
        while True:
            self.write_to_console(
                str(angle),
                column=5,
                row=2,
                reset_console=True,
                inverse=True,
                alignment="C",
                font_size="L",
            )
            angle = gyro.angle
            self.sleep_in_loop()
            if btn.any():
                break

    def choose_color_sensor(self, which_color_sensor="right"):
        """
        Returns the color sensor based on argument
        """
        if which_color_sensor == "right":
            return self.right_color_sensor
        else:
            return self.left_color_sensor

    def choose_gyro_sensor(self, which_gyro_sensor="right"):
        """
        Returns the gyro sensor based on argument
        """
        if which_gyro_sensor == "right":
            return self.right_gyro_sensor
        else:
            return self.left_gyro_sensor

    def write_to_console(
        self,
        msg: str,
        column: int,
        row: int,
        reset_console=True,
        inverse=False,
        alignment="L",
        font_size="M",
    ):
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
        if font_size == "S":
            console.set_font("Lat15-TerminusBoldVGA16.psf.gz", True)
        elif font_size == "M":
            console.set_font("Lat15-Terminus20x10.psf.gz", True)
        else:
            console.set_font("Lat15-Terminus32x16.psf.gz", True)
        console.text_at(
            msg,
            column,
            row,
            reset_console=reset_console,
            inverse=inverse,
            alignment=alignment,
        )

    def read_from_color_sensor(self, which_color_sensor="right", read_white=True):
        """
        Will show the value of the color sensor on the screen
        and return when any button is pressed
        TODO: Fix console display of light value which is changing size and location
        """
        cs = self.choose_color_sensor(which_color_sensor)
        cs.MODE_COL_REFLECT = "COL-REFLECT"
        btn = Button()
        light = cs.reflected_light_intensity
        while True:
            self.write_to_console(
                str(light),
                column=5,
                row=2,
                reset_console=True,
                inverse=(not read_white),
                alignment="C",
                font_size="L",
            )
            light = cs.reflected_light_intensity
            self.sleep_in_loop()
            if btn.any():
                break
        return light

    def write_light_to_settings(self):
        """
        Writes white and black light values to settings file via Settings class
        """
        white = self.read_from_color_sensor(read_white=True)
        self.start_tone()
        self.debug("White: {}".format(white))
        black = self.read_from_color_sensor(read_white=False)
        self.start_tone()
        self.debug("Black: {}".format(black))
        line = self.read_from_color_sensor(read_white=True)
        self.start_tone()
        self.debug("Line: {}".format(line))
        light_values = {"white": white, "black": black, "line": line}

        self.settings.settings["light_values"] = light_values
        self.settings.write()  # save to file

    def read_light_from_settings(self):
        """
        Reads from light.txt and returns the white
        and black and line values as a tuple
        If error, catch exception, debug.print it, and return None
        """
        try:
            light_values = self.settings.get("light_values")
            white = light_values.get("white", WHITE_LIGHT_INTENSITY)
            black = light_values.get("black", BLACK_LIGHT_INTENSITY)
            line = light_values.get("line", LINE_LIGHT_INTENSITY)
            self.debug(
                "Returning white and black and line values: ({}, {}, {})".format(
                    white, black, line
                )
            )
            self.white_light_intensity = int(white)
            self.black_light_intensity = int(black)  # Stores values as integers
            self.line_square_intensity = int(line)
            return (white, black, line)
        except Exception as e:
            self.debug("Error reading light: {}".format(e))
            return None

    def flip_boolean_setting(self, setting):
        """Flip a boolean true/false setting named `settings`"""
        btn = Button()
        self.wait_for_button_press(btn)
        # flip the gyro setting
        self.settings.settings[setting] = not self.settings.get(setting)
        self.settings.write()
        return self.settings.get(setting)

    def flip_gyro_sensor_setting(self):
        """
        Will show the value of the color sensor on the screen
        and return when any button is pressed
        """
        return self.flip_boolean_setting("use_gyro")

    def flip_debug_setting(self):
        return self.flip_boolean_setting("debug")

    def set_up_sensors_motors(self):
        """
        Creates all sensors and motors or returns None or the error
        """
        try:
            self.leds = Leds()
            self.left_color_sensor = ColorSensor(LEFT_COLOR_SENSOR_INPUT)
            self.cs = self.left_color_sensor
            self.left_gyro_sensor = GyroSensor(LEFT_GYRO_SENSOR_INPUT)
            self.right_gyro_sensor = GyroSensor(RIGHT_GYRO_SENSOR_INPUT)
            self.gyro = self.right_gyro_sensor
            self.right_color_sensor = ColorSensor(RIGHT_COLOR_SENSOR_INPUT)
            self.left_medium_motor = MediumMotor(LEFT_MEDIUM_MOTOR_PORT)
            self.right_medium_motor = MediumMotor(RIGHT_MEDIUM_MOTOR_PORT)
            self.left_large_motor = LargeMotor(LEFT_LARGE_MOTOR_PORT)
            self.right_large_motor = LargeMotor(RIGHT_LARGE_MOTOR_PORT)
        except Exception as e:
            self.write_to_console(
                str(e),
                column=1,
                row=3,
                reset_console=True,
                inverse=True,
                alignment="L",
                font_size="M",
            )
            return e
        else:
            return None

    def drive_until_color(self, speed: int, color: int, which_color_sensor="right"):
        """
        drives at `SpeedPercent(speed)` until the specified color `stop_color`
        with chosen color sensor `which_color_sensor`
        TODO: add gyro support
        """
        cs = self.choose_color_sensor(which_color_sensor)
        cs.MODE_COL_COLOR = "COL-COLOR"
        self.on(SpeedPercent(speed), SpeedPercent(speed))
        while not color == cs.color_name:
            self.sleep_in_loop()
        self.off()

    def drive_until_white_black(self, speed: int, which_color_sensor="left"):
        """
        drives at `SpeedPercent(speed)` until white `white_light_intensity`
        then black 'black_light_intensity' 
        with chosen color sensor `which_color_sensor`
        TODO: Fix drive_until_white_black
        """
        cs = self.choose_color_sensor(which_color_sensor)
        cs.MODE_COL_REFLECT = "COL-REFLECT"
        self.on(SpeedPercent(speed), SpeedPercent(speed))
        while cs.reflected_light_intensity < self.white_light_intensity:
            self.debug(
                "reflected light intensity: {}".format(cs.reflected_light_intensity)
            )
            self.sleep_in_loop()
        while cs.reflected_light_intensity >= self.black_light_intensity:
            self.sleep_in_loop()
        self.move_tank.off()

    def attachment_raise_lower(self, speed: int, rotations: int):
        """
        Raises and lowers the medium motors as a tank
        """
        self.attachment_tank.on_for_rotations(speed, -speed, rotations)

    def calibrate_gyro(self, which_gyro_sensor="right"):
        """
        Calibrates the gyro sensor.
        NOTE: This takes 1sec to run
        """
        # assert self._gyro, "GyroSensor must be defined"
        gyro = self.choose_gyro_sensor(which_gyro_sensor)
        for _ in range(2):
            gyro.mode = "GYRO-RATE"
            gyro.mode = "GYRO-ANG"
            sleep(0.5)

    def on_for_distance(
        self,
        speed: int,
        distance_in: int,
        brake=True,
        block=True,
        use_gyro=False,
        target=0,
        which_gyro_sensor="right",
    ):
        """
        Drives for a certain distance
        and has a toglable gyro feature
        ``speed`` can be a percentage or a :class:`ev3dev2.motor.SpeedValue`
        object, enabling use of other units.
        """
        # self.reset()

        # values from ev3dev2 source
        # kp = 11.3
        # ki = 0.05
        # kd = 3.2

        kp = 11.3
        ki = 2
        kd = 3.2

        distance_mm = self.in_to_mm(distance_in)
        if use_gyro:
            self.set_led("AMBER")
            gyro = self.choose_gyro_sensor(which_gyro_sensor)
            gyro.mode = gyro.MODE_GYRO_ANG
            # there is currently a bug in gyro.reset() method so instead we just read the current
            # angle and then compare to that
            gyro.reset()
            # reset_angle = gyro.angle
            self.debug("GYRO ANGLE BEFORE LOOP: {}".format(gyro.angle))

            # convert speed to a SpeedValue if not already
            speed_native_units = self.left_motor._speed_native_units(speed)
            integral = 0.0  # integral is the sum of all errors
            last_error = 0.0  # last_error stores the last error through the while loop
            derivative = 0.0  # derivative is the rate at which the error is changing
            while self.follow_for_distance(distance_in, speed):
                # error = gyro.angle - reset_angle # OLD CODE BEFORE GYRO.RESET FIXED
                error = gyro.angle - target
                integral = integral + error
                derivative = error - last_error
                last_error = error
                turn_native_units = (kp * error) + (ki * integral) + (kd * derivative)
                left_speed = SpeedNativeUnits(speed_native_units - turn_native_units)
                right_speed = SpeedNativeUnits(speed_native_units + turn_native_units)
                self.debug(
                    "error: {}, integral: {}, derivative: {}, last_error: {},\
                turn_native_units: {}, left_speed: {}, right_speed: {}".format(
                        error,
                        integral,
                        derivative,
                        last_error,
                        turn_native_units,
                        left_speed,
                        right_speed,
                    )
                )
                self.on(left_speed, right_speed)
                self.sleep_in_loop(0.01)
        else:
            super().on_for_distance(speed, distance_mm, brake, block)

        self.set_led()

    def line_follow(
        self,
        speed: int,
        distance_in,
        which_color_sensor="right",
        brake=True,
        block=True,
    ):
        cs = self.choose_color_sensor(which_color_sensor)
        integral = 0.0
        last_error = 0.0
        derivative = 0.0

        kp = 0.5
        ki = 0.1
        kd = 0.1

        target_light_intensity = self.line_square_intensity
        speed_native_units = self.left_motor._speed_native_units(speed)
        while self.follow_for_distance(distance_in, speed):
            reflected_light_intensity = cs.reflected_light_intensity
            error = target_light_intensity - reflected_light_intensity
            integral = integral + error
            derivative = error - last_error
            last_error = error
            turn_native_units = (kp * error) + (ki * integral) + (kd * derivative)
            left_speed = SpeedNativeUnits(speed_native_units - turn_native_units)
            right_speed = SpeedNativeUnits(speed_native_units + turn_native_units)

            self.debug(
                "target_light_intensity: {}, error: {}, integral: {}, derivative: {}, last_error: {}, turn_native_units: {}, left_speed: {}, right_speed: {}".format(
                    target_light_intensity,
                    error,
                    integral,
                    derivative,
                    last_error,
                    turn_native_units,
                    left_speed,
                    right_speed,
                )
            )

            self.on(left_speed, right_speed)

    def follow_for_distance(self, distance_in, speed):
        """
       Measures the current position of the left large motor and
       Compares it to the desired position
       If less, returns False
       If equal or more, returns True
        """
        # if this is the first time during this follow_for_distance run that we are calling this function
        # store the total distance that the robot will run in self.follow_distance_degrees
        if not hasattr(
            self, "target_degrees"
        ):  # pylint: disable=access-member-before-definition
            rotations = self.in_to_mm(distance_in) / self.wheel_circumference
            # target degrees is current position + additional rotations * 360
            self.target_degrees = self.left_large_motor.position + (360 * rotations)

        left_current = self.left_large_motor.position
        left_rotations = left_current / self.left_motor.count_per_rot
        left_degrees = left_rotations * 360
        self.debug(
            "Current Degrees: {} vs Desired Degrees: {}".format(
                left_degrees, self.target_degrees
            )
        )

        if left_degrees < self.target_degrees:
            return True
        else:
            # reset follow_for_distance method by removing target_degrees attribute
            delattr(self, "target_degrees")
            return False

    def wait_for_button_press(self, button):
        """
        Wait for a button to be pressed and released.
        Parameter:
        - `button` (Button): an instance of the EV3 Button() class
        return the Button name that was pressed.
        """
        pressed = None
        while True:
            allpressed = button.buttons_pressed
            if bool(allpressed):
                pressed = allpressed[0]  # just get the first one
                while not button.wait_for_released(pressed):
                    pass
                break
        return pressed
