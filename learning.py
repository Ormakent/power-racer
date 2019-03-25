import numpy as np
import random
import os
import evaluate

STATE_NUM = 10
CP_MAX = 200
MOVE_MAX = 50
PULL_MAX = 20

alpha = 0.4
gamma = 0.95
epsilon = 1

q_table = []
moves = ['F', 'R', 'S', 'L', 'FL', 'FR']
prev_state = dict()
prev_action = 'F'
cps_crossed = 0
tiles = evaluate.get_tiles(evaluate.MAP_DIM_X, evaluate.MAP_DIM_Y)


def init():
    global prev_action, prev_state, q_table, cps_crossed
    # if there is a save file, load it
    # else
    if os.path.isfile('qt.npy'):
        q_table = np.load('qt.npy')
    q_table = np.zeros([STATE_NUM ** 6, 6])
    prev_state = {
        'cpx': -23.0,
        'cpy': 0.,
        'movex': 0.,
        'movey': 0.,
        'pullx': -14.,
        'pully': 2.,
        'wp_crossed': 0
    }
    prev_action = 'F'
    cps_crossed = 0


def do_iteration(state):
    global prev_action, prev_state, cps_crossed
    cps_crossed += state['wp_crossed']
    conv_s = convert_state(state)
    if random.uniform(0, 1) < epsilon:
        next_action = moves[np.argmax(q_table[ind_from_s(conv_s)])]
    else:
        next_action = random.choice(moves)
    cur_q = q_table[ind_from_s(prev_state)][moves.index(prev_action)]
    q_table[ind_from_s(prev_state)][moves.index(prev_action)] = \
        cur_q + alpha * (reward(conv_s) + gamma * q_table[ind_from_s(conv_s)][moves.index(next_action)] - cur_q)
    print(f'Q( {ind_from_s(prev_state)}, {moves.index(prev_action)}) ='
          f' {q_table[ind_from_s(prev_state)][moves.index(prev_action)]}')
    prev_action = next_action
    prev_state = conv_s
    return next_action


def reward(sp):
    global cps_crossed
    rew = sp['wp_crossed'] * 2000
    if cps_crossed >= 13:
        cps_crossed -= 13
        rew += 8000
    player_pos = sp['player_pos']
    conv_coords = [int(player_pos[0] / 4), int(player_pos[1] / 4)]
    if tiles[conv_coords[1]][conv_coords[0]] == 'o':
        rew -= 50
    move_mid = (STATE_NUM - 1) / 2
    move_dist = np.sqrt((sp['movex'] - move_mid) ** 2 + (sp['movey'] - move_mid) ** 2)
    rew += 1 / (1 + move_dist) * -50
    cp_mid = (STATE_NUM - 1) / 2
    cp_dist = np.sqrt((sp['cpx'] - cp_mid) ** 2 + (sp['cpy'] - cp_mid) ** 2)
    rew += cp_dist * -50
    return rew


def ind_from_s(s):
    ind = 0
    ind += s['cpx']
    ind += s['cpy'] * STATE_NUM
    ind += s['movex'] * STATE_NUM ** 2
    ind += s['movey'] * STATE_NUM ** 3
    ind += s['pullx'] * STATE_NUM ** 4
    ind += s['pully'] * STATE_NUM ** 5
    return int(ind)


def convert_state(state):
    ret = dict()
    orig_cp = state['cp_vector']
    ret['cpx'] = squish(CP_MAX, orig_cp[0], STATE_NUM)
    ret['cpy'] = squish(CP_MAX, orig_cp[1], STATE_NUM)
    orig_move = state['move_vector']
    ret['movex'] = squish(MOVE_MAX, orig_move[0], STATE_NUM)
    ret['movey'] = squish(MOVE_MAX, orig_move[1], STATE_NUM)
    orig_pull = state['push_vector']
    ret['pullx'] = squish(PULL_MAX, orig_pull[0], STATE_NUM)
    ret['pully'] = squish(PULL_MAX, orig_pull[1], STATE_NUM)
    ret['wp_crossed'] = state['wp_crossed']
    ret['player_pos'] = state['player_pos']
    return ret


def squish(max, val, factor):
    if val >= max:
        return factor - 1
    elif val <= -1 * max:
        return 0
    else:
        return int((val + max) / (2 * max / factor))


def save_q(): np.save('qt', q_table)
