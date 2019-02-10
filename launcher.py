import subprocess
import pyautogui
import time
import logging
import config
import PIL

log = logging.getLogger('launcher')
game_running = False


def launch_game():
    if game_running:
        restart_game()
    else:
        resolution = str(config.GAME['width']) + "x" + str(config.GAME['height'])
        process_options = ["mame", "amspdwy", "-resolution", resolution, "-window", "-sound", "none"]
        subprocess.Popen(process_options, cwd=config.GAME['path'])
        # wait for game to start up
        time.sleep(3)


    # skip machine info window
    for i in range(5):
        pyautogui.press("w")
        time.sleep(0.1)

    # wait for screen transition
    time.sleep(4)


def restart_game():
    pyautogui.press("f3")


def exit_game():
    pyautogui.press("esc")


def insert_coin():
    pyautogui.press("5")


def take_screenshot():
    start = time.time()
    # pretty slow screenshot taker, may need to replace
    img = pyautogui.screenshot(region=(config.SYSTEM['width'] / 2 - config.GAME['width'],
                                       config.SYSTEM['height'] / 2 - config.GAME['height'],
                                       config.GAME['width'] * 2,
                                       config.GAME['height'] * 2))
    img.thumbnail((config.GAME['width'], config.GAME['height']), PIL.Image.ANTIALIAS)
    img.save("test.png")
    print(f'it took {time.time() - start} seconds to process a screenshot')


def main():
    launch_game()
    take_screenshot()
    exit_game()


if __name__ == "__main__":
    main()
