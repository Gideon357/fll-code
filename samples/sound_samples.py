#!/usr/bin/env micropython

from ev3dev2.sound import Sound

player = Sound()
player.play_song(
    (
        ("D4", "e3"),  # intro anacrouse
        ("D4", "e3"),
        ("D4", "e3"),
        ("G4", "h"),  # meas 1
        ("D5", "h"),
        ("C5", "e3"),  # meas 2
        ("B4", "e3"),
        ("A4", "e3"),
        ("G5", "h"),
        ("D5", "q"),
        ("C5", "e3"),  # meas 3
        ("B4", "e3"),
        ("A4", "e3"),
        ("G5", "h"),
        ("D5", "q"),
        ("C5", "e3"),  # meas 4
        ("B4", "e3"),
        ("C5", "e3"),
        ("A4", "h."),
    )
)
