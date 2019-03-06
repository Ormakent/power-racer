from collections import deque
import numpy as np
import math


def main():
    c_queue = deque([])
    init_queue(c_queue)
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


def init_queue(queue):
    queue.append([[1, 1], [5, 5]])
    queue.append([[2, 2], [7, 3]])


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
