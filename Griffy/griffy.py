from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveDifferential, SpeedPercent, MoveTank, Motor, MoveSteering
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
        self.WHEEL_DISTANCE = WheelDistance
        self.LEFT_LARGE_MOTOR = LeftLargeMotor
        self.RIGHT_LARGE_MOTOR = RightLargeMotor
        # Put a sound at the end to show when it is done.
        self.start_tone()

    def start_tone(self):
        player = Sound()
        player.play_tone(500, 0.5, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

    def line_square(self, black_light_intensity, white_light_intensity):
        """Needs a method description and usage."""
        pass

    def pid_line_follow(self, black_light_intensity, white_light_intensity, speed):
        """Needs a method description and usage."""
        pass

    def dive_until_color(self, speed):
        """Needs a method description and usage."""
        pass

  def move(ki=0,kp=0,kd=0,target=0,wheel=self.WheelDistance,LeftSpeed=100,RightSpeed=100,distance, drive_with_gyro=True)
     """ Moves the robot a specified amount of inches. Uses PID algorithim and the Gyro Sensor to correct drift"""
    r = distance/wheel
    console = Console()
    if drive_with_gyro == True:
        try:
            subprocesses.call("echo reset > $MC/command")  # Resets Tacho Counts, I use these to count the robots movment so that it can correct using the PID algorithim and move simultaneously.
            counts = motor.count_per_rot # Finds Tacho Counts per rotation.
            m = r*counts
            steer = MoveSteering(self.LeftLargeMotor, self.RightLargeMotor) # Initializes MoveSteering 
            while True:
                error = target - gyro.mode
                integral = integral + error
                error - last_error = derivative
                integralResult = integral*ki
                porportionResult = kp*error
                derivResult = kd*derivative
                result = integralResult+derivResult+porportionResult
                steer.on(result,speed)
                error = lastError
                if motor.position => m:
                    return False #If the motor has moved the correct amount, it ends the loop
                else:
                    subprocesses.call("echo reset > $MC/command")
                    return True
        except: # If tacho motor does not initialize, it runs without gyro
            tank.on_for_rotations(LeftSpeed,RightSpeed,r)
            try:
                console.text_at('An Exception Occured, Ran Without Gyro. Check Motor and Drivers', column=1, row=5, reset_console=True, inverse=True)
            except:
                pass
        else:
            tank.on_for_rotations(LeftSpeed,RightSpeed,r)

    def first_run(self):
        """A Test Run"""
        self.on_for_distance(30, 520)
        self.on_for_distance(-100, 520)
