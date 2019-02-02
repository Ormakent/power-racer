import subprocess
import pyautogui
import time
import logging
import config

log = logging.getLogger('launcher')


def launch_game():
    process_options = ["mame", "amspdwy", "-resolution", config.GAME['resolution'], "-window", "-sound", "none"]
    subprocess.Popen(process_options, cwd=config.GAME['path'])

    # wait for game to start up
    time.sleep(3)

    # skip machine info window
    for i in range(5):
        pyautogui.press("w")
        time.sleep(0.1)

    # wait for screen transition
    time.sleep(3)

    '''
    # insert coin
    pyautogui.press("5")
    # wait for race to start
    time.sleep(8)
    # drive forward
    pyautogui.keyDown("UP")
    time.sleep(20)
    pyautogui.keyUp("UP")
    '''


if __name__ == "__main__":
    launch_game()
