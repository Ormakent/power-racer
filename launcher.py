import os
import subprocess
import pyautogui
import time
import logging
import config
import PIL
from mss import mss

log = logging.getLogger('launcher')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

game_running = False


def launch_game():
    if game_running:
        restart_game()
    else:
        log.debug("Launching game")
        resolution = str(config.GAME['width']) + "x" + str(config.GAME['height'])
        process_options = [os.path.join(config.GAME['path'], config.GAME['executable']),
                           "amspdwy",
                           "-resolution", resolution,
                           "-window",
                           "-sound", "none"]
        subprocess.Popen(process_options, cwd=config.GAME['path'])

        # wait for game to start up
        log.debug("Waiting for game startup")
        time.sleep(4)

    # skip machine info window
    log.debug("Skipping info window")
    for i in range(5):
        pyautogui.press("w")
        time.sleep(0.1)

    # wait for screen transition
    log.debug("Waiting for screen transition")
    time.sleep(4)


def restart_game():
    pyautogui.press("f3")


def exit_game():
    pyautogui.press("esc")


def insert_coin():
    for i in range(3):
        pyautogui.press("5")
    log.debug("Coin was inserted")


def take_screenshot():
    start = time.time()
    monitor = {"width": 640,
               "height": 480,
               "left": (config.SYSTEM['width'] / 2 - config.GAME['width']) / 2,
               "top": (config.SYSTEM['height'] / 2 - config.GAME['height']) / 2}
    img_src = mss().grab(monitor)
    img = PIL.Image.frombytes("RGB", img_src.size, img_src.bgra, "raw", "BGRX")
    img.thumbnail((config.GAME['width'], config.GAME['height']), PIL.Image.ANTIALIAS)
    img.save("test.png")
    log.debug(f'it took {time.time() - start} seconds to process a screenshot')


def main():
    launch_game()
    insert_coin()
    time.sleep(8)
    take_screenshot()
    exit_game()


if __name__ == "__main__":
    main()
