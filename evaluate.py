from collections import deque
import numpy as np
import math

def main():
    c_queue = deque([])
    pos_queue = deque([])
    init_queue(c_queue)
    init_pos_queue(pos_queue)
    n = 1
    while n < 15:
        print(n)
        point1, point2 = c_queue[0]
        #Position of car
        point3, point4 = pos_queue[0]
        print(point1, point2, point3, point4)
        inter = get_intersect(point1, point2, point3, point4)
        print(inter)
        if is_between(point1, inter, point2) and is_between(point3, inter, point4):
            print("WP was crossed")
            c_queue.rotate(-1)
            pos_queue.rotate(-1)
            n = n + 1
        else:
            print("WP was not crossed")
            #print(is_between(point1, inter, point2))
            #print(is_between(point3, inter, point4))
            pos_queue.rotate(-1)
            n = n + 1


def init_queue(queue):
    queue.append([[645, 38], [645, 270]])
    queue.append([[240, 347], [558, 347]])
    queue.append([[240, 736], [558, 736]])
    queue.append([[602, 769], [602, 1080]])
    queue.append([[974, 540], [974, 851]])
    queue.append([[1323, 769], [1323, 1080]])
    queue.append([[1366, 736], [1682, 736]])
    queue.append([[1366, 348], [1682, 348]])
    queue.append([[1276, 273], [1276, 1]])
    queue.append([[939, 38], [939, 271]])

def init_pos_queue(queue):
    queue.append([[723, 140], [478, 172]])
    queue.append([[478, 172], [445, 420]])
    queue.append([[445, 420], [441, 683]])
    queue.append([[441, 683], [451, 901]])
    queue.append([[451, 901], [714, 899]])
    queue.append([[714, 899], [803, 683]])
    queue.append([[803, 683], [1139, 655]])
    queue.append([[1139, 655], [1255, 893]])
    queue.append([[1255, 893], [1437, 883]])
    queue.append([[1437, 883], [1471, 579]])
    queue.append([[1471, 579], [1547, 299]])
    queue.append([[1547, 299], [1361, 145]])
    queue.append([[1361, 145], [1067, 163]])
    queue.append([[1067, 163], [901, 169]])


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
