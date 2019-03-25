import os
import subprocess
import pyautogui
import time
import logging
import config
import PIL
from mss import mss
import cv2
import numpy as np
import image_scanner
import evaluate
import learning

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
    pyautogui.press("f3", pause=0.1)
    time.sleep(0.1)
    pyautogui.press("f3", pause=0.1)


def exit_game():
    pyautogui.press("esc", pause=0.15)
    pyautogui.press("esc", pause=0.15)


def insert_coin():
    pyautogui.press("5", pause=0.15)
    pyautogui.press("5", pause=0.15)
    pyautogui.press("5", pause=0.15)
    log.debug("Coin was inserted")


def take_screenshot(name=None):
    start = time.time()
    monitor = {"width": 640,
               "height": 480,
               "left": (config.SYSTEM['width'] / 2 - config.GAME['width']) / 2,
               "top": (config.SYSTEM['height'] / 2 - config.GAME['height']) / 2}
    img_src = mss().grab(monitor)
    img = PIL.Image.frombytes('RGB', img_src.size, img_src.bgra, 'raw', 'BGRX')
    img.thumbnail((config.GAME['width'], config.GAME['height']), PIL.Image.ANTIALIAS)
    log.debug(f'it took {time.time() - start} seconds to process a screenshot')
    if name is not None:
        img.save(name)
    else:
        return img


def move_car(direction):
    possible = ['up', 'left', 'right']
    dirs = {
        'L': ['left'],
        'R': ['right'],
        'F': ['up'],
        'FR': ['up', 'right'],
        'FL': ['up', 'left'],
        'S': None
    }
    for move in possible:
        if dirs[direction] and move in dirs[direction]:
            pyautogui.keyDown(move)
        else:
            pyautogui.keyUp(move)


def main():
    launch_game()
    test_img = cv2.resize(cv2.imread('test1.png'), (320, 240))
    cv2.namedWindow('img')
    cv2.moveWindow('img', 0, 0)
    cv2.imshow('img', test_img)
    cv2.waitKey(1)
    while True:
        run_first_map()
        restart_game()


def end_cond_met(img, time_start):
    return np.all(img[200][33] >= [254, 0, 0]) or time.time() - time_start > 60


def run_first_map():
    insert_coin()
    # wait until loaded into the game
    time.sleep(8)
    # take screenshot
    img = np.array(take_screenshot())
    time_start = time.time()
    # starting coords
    cur_coords = np.array([34, 413])
    # checkpoints
    evaluate.init_queue()
    learning.init()
    # while the map hasn't finished
    while not end_cond_met(img, time_start):
        # process screenshot
        state = image_scanner.process_img(img)
        vec = state['player_pos'] - cur_coords
        if abs(vec[0]) > 50 or abs(vec[1]) > 50:
            vec = np.array([0, 0])
        p1_rev = [cur_coords[1], cur_coords[0]]
        p2_rev = [state['player_pos'][1], state['player_pos'][0]]
        state['move_vector'] = vec
        state['cp_vector'] = get_cp_vector(evaluate.c_queue[0][0], evaluate.c_queue[0][1], p1_rev)
        state['wp_crossed'] = 0
        while evaluate.wp_crossed(p1_rev, p2_rev, evaluate.c_queue[0][0], evaluate.c_queue[0][1]):
            evaluate.c_queue.rotate(-1)
            state['wp_crossed'] += 1
        print(state)
        move_car(learning.do_iteration(state))
        draw_state(img, state)
        img = np.array(take_screenshot())
        cur_coords = state['player_pos']
    print("we stop now")
    move_car('S')
    learning.save_q()
    return None


def get_cp_vector(p1, p2, pt):
    print(p1, p2, pt)
    p1 = np.array(p1)
    p2 = np.array(p2)
    pt = np.array(pt)
    v1 = p1 - p2
    v2 = pt - p2
    a1 = np.dot(v1, v2) * v1 / (np.linalg.norm(v1) ** 2)
    return a1 - v2


def draw_state(img, state):
    # white rectangle - player_pos
    player_pos = state['player_pos']
    cv2.rectangle(img, (player_pos[1] + 5, player_pos[0] + 5),
                  (player_pos[1] - 5, player_pos[0] - 5), (255, 255, 255), 2)
    # pink rectangles - other_pos
    for car_pos in state['other_cars_pos']:
        cv2.rectangle(img, (car_pos[1] + 5, car_pos[0] + 5),
                      (car_pos[1] - 5, car_pos[0] - 5), (180, 105, 255), 2)
    cv2.line(img, (player_pos[1], player_pos[0]),
             (int(player_pos[1] - state['push_vector'][1]), int(player_pos[0] - state['push_vector'][0])), (0, 0, 255),
             2)
    for cp in evaluate.c_queue:
        cv2.line(img, tuple(cp[0]), tuple(cp[1]), (0, 255, 255), 2)
    cv2.imshow('img', cv2.resize(img, (320, 240)))
    cv2.waitKey(1)


if __name__ == "__main__":
    main()
