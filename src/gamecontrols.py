"""A module for keyboard presses emulation.

As MAME does not always register single presses with pyautogui certain functions perform multiple presses to
circumvent that.

WARNING: MAME does not accept keyboard emulators on Windows as of more recent versions (MacOS works,
Linux not tested). To fix that, a custom version of MAME with DIRECT_INPUT enabled must be used.
"""

import pyautogui


def move_car_in_direction(direction):
    for key in possible_keys_for_move:
        if keys_for_direction[direction] and key in keys_for_direction[direction]:
            pyautogui.keyDown(key)
        else:
            pyautogui.keyUp(key)


def exit_game():
    pyautogui.press("esc", interval=0.1)
    pyautogui.press("esc", interval=0.1)


def restart_game():
    pyautogui.press("f3", interval=0.1)
    pyautogui.press("f3", interval=0.1)


def insert_coin():
    pyautogui.press("5", interval=0.1)
    pyautogui.press("5", interval=0.1)
    pyautogui.press("5", interval=0.1)


keys_for_direction = {
    'L': ['left'],
    'R': ['right'],
    'F': ['up'],
    'FR': ['up', 'right'],
    'FL': ['up', 'left'],
    'S': None
}

possible_keys_for_move = ['up', 'left', 'right']
