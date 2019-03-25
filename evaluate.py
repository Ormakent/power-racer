from collections import deque
import numpy as np
import math
import cv2

MAP_DIM_X = 160
MAP_DIM_Y = 120

c_queue = deque([])


def main():
    init_queue()
    point1, point2 = c_queue[0]
    point3 = [1, 4]
    point4 = [4, 2]
    print(point1, point2, point3, point4)
    inter = get_intersect(point1, point2, point3, point4)
    print(inter)
    if is_between(point1, inter, point2) and is_between(point3, inter, point4):
        print("WP was crossed")
        c_queue.rotate(-1)
    else:
        print("WP was not crossed")

    get_pull_vector([10, 10])

    # img = cv2.imread("test1.png")
    # img = cv2.resize(img, (160, 120))
    # cv2.imshow('img', img)
    # cv2.waitKey(0)


def wp_crossed(p1, p2, p3, p4):
    inter = get_intersect(p1, p2, p3, p4)
    return is_between(p1, inter, p2) and is_between(p3, inter, p4)


def get_pull_vector(player_coords):
    tileset = get_tiles(MAP_DIM_X, MAP_DIM_Y)
    pCoords = [int(player_coords[0] / 4), int(player_coords[1] / 4)]
    radius = 12
    vector = np.array([0.0, 0.0])
    weights = dict()
    weights['w'] = 1.5
    weights['o'] = 0.05
    weights['r'] = -0.1
    for x in range(pCoords[0] - radius, pCoords[0] + radius + 1):
        for y in range(pCoords[1] - radius, pCoords[1] + radius + 1):
            push_vector = np.array([x - pCoords[0], y - pCoords[1]])
            dist = np.linalg.norm(push_vector)
            if dist <= 20 and not math.isclose(dist, 0) and 0 <= x < MAP_DIM_X and 0 <= y < MAP_DIM_Y:
                tmp = weights[tileset[x][y]] * push_vector / dist ** 2
                vector += tmp
    return vector


def get_tiles(dimX, dimY):
    tiles = [['r' for _ in range(dimY)] for _ in range(dimX)]
    for x in range(4):
        for y in range(dimY):
            tiles[x][y] = 'w'
            tiles[dimX - x - 1][y] = 'w'
    for y in range(4):
        for x in range(dimX):
            tiles[x][y] = 'w'
            tiles[x][dimY - y - 1] = 'w'
    fill_triangle([4, 24], [28, 4], [4, 4], tiles, 'o')
    fill_triangle([4, 94], [28, 116], [4, 116], tiles, 'o')
    fill_triangle([120, 4], [156, 24], [156, 4], tiles, 'o')
    fill_triangle([120, 116], [156, 96], [156, 116], tiles, 'o')
    fill_triangle([45, 81], [71, 60], [45, 60], tiles, 'o')
    fill_triangle([90, 60], [115, 81], [115, 60], tiles, 'o')
    fill_triangle([95, 94], [120, 116], [95, 116], tiles, 'o')
    fill_triangle([75, 94], [50, 116], [75, 116], tiles, 'o')
    for x in range(35, 125):
        for y in range(30, 60):
            tiles[x][y] = 'w'
    for x in range(35, 45):
        for y in range(60, 85):
            tiles[x][y] = 'w'
    for x in range(115, 125):
        for y in range(60, 85):
            tiles[x][y] = 'w'
    for x in range(75, 95):
        for y in range(94, 116):
            tiles[x][y] = 'w'
    return tiles


def fill_triangle(pA, pB, pC, arr, val):
    slope = (pB[1] - pA[1]) / (pB[0] - pA[0])
    b = pB[1] - slope * pB[0]
    fill_above_line = pC[1] >= pC[0] * slope + b
    x_from = min(pA[0], pB[0])
    x_to = max(pA[0], pB[0])
    y_from = min(pA[1], pB[1])
    y_to = max(pA[1], pB[1])
    for x in range(x_from, x_to):
        for y in range(y_from, y_to):
            if fill_above_line and (y >= x * slope + b):
                arr[x][y] = val
            elif not fill_above_line and (y <= x * slope + b):
                arr[x][y] = val


def init_queue():
    c_queue.clear()
    c_queue.append([[390, 20], [390, 120]])
    c_queue.append([[250, 20], [250, 120]])
    c_queue.append([[159, 136], [20, 20]])
    c_queue.append([[140, 230], [20, 230]])
    c_queue.append([[140, 330], [20, 460]])
    c_queue.append([[160, 340], [160, 465]])
    c_queue.append([[180, 330], [310, 390]])
    c_queue.append([[340, 380], [320, 240]])
    c_queue.append([[460, 320], [375, 390]])
    c_queue.append([[480, 340], [480, 460]])
    c_queue.append([[500, 330], [620, 460]])
    c_queue.append([[500, 230], [620, 230]])
    c_queue.append([[480, 140], [620, 20]])


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def is_between(a, c, b):
    return math.isclose(distance(a, c) + distance(c, b), distance(a, b))


# Taken from https://stackoverflow.com/a/42727584
# Finds intersections of 2 lines
def get_intersect(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1, a2, b1, b2])  # s for stacked
    h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
    l1 = np.cross(h[0], h[1])  # get first line
    l2 = np.cross(h[2], h[3])  # get second line
    x, y, z = np.cross(l1, l2)  # point of intersection
    if z == 0:  # lines are parallel
        return float('inf'), float('inf')
    return x / z, y / z


if __name__ == "__main__":
    main()
