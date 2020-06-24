#!/usr/bin/env micropython
# TODO: add screen feedback listing motors (A, B, C, D)

from time import sleep

from ev3dev2.button import Button
from ev3dev2.led import Leds
from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor,
                           MediumMotor, Motor, SpeedPercent, list_motors)
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.sound import Sound

motor_a = MediumMotor(OUTPUT_A)
motor_b = LargeMotor(OUTPUT_B)
motor_c = LargeMotor(OUTPUT_C)
motor_d = MediumMotor(OUTPUT_D)
selected_motor = None


def main():
    intro_sound()
    stop_all_motors()
    choose_motor_loop()


def stop_all_motors():
    for motor in list_motors():
        motor.stop(stop_action="brake")


def get_selected_motor():
    global selected_motor
    print("Returning motor: {}".format(selected_motor))
    return selected_motor


def set_selected_motor(motor):
    global selected_motor
    print("Setting selected motor to: {}".format(motor))
    selected_motor = motor


def change_motor(changed_buttons):
    """
    Respond to button presses in choose_motor loop
    and based on pressed button choose the selected motor
    up=a, left=b, down=c, right=d
    """
    if ("up", True) in changed_buttons:
        set_selected_motor(motor_a)
    elif ("left", True) in changed_buttons:
        set_selected_motor(motor_b)
    elif ("down", True) in changed_buttons:
        set_selected_motor(motor_c)
    elif ("right", True) in changed_buttons:
        set_selected_motor(motor_d)
    else:
        print("Center button pressed.")
        return

    command_loop()
    sleep(1)


def choose_motor_loop():
    """
    while the back button is not pressed
    loop and set the active motor to control
    based on the button pressed.
    """
    btn = Button()
    btn.on_change = change_motor
    while True:
        btn.process()
        sleep(0.01)


def run_motor(direction=1):
    get_selected_motor().on(SpeedPercent(50) * direction)


def stop_motor():
    get_selected_motor().off()


def up_pressed(state):
    if (
        state
        and get_selected_motor() is not None
        and not get_selected_motor().is_running
    ):
        run_motor(1)
    else:
        stop_motor()


def down_pressed(state):
    if (
        state
        and get_selected_motor() is not None
        and not get_selected_motor().is_running
    ):
        run_motor(-1)
    else:
        stop_motor()


def command_loop():
    btn = Button()
    btn.on_up = up_pressed
    btn.on_down = down_pressed
    while not btn.enter:
        btn.process()
        sleep(0.01)


def intro_sound():
    player = Sound()
    player.play_tone(
        500, 0.5, delay=0.0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE
    )


if __name__ == "__main__":
    main()
