import cv2
import numpy as np
import time
from scipy.cluster.vq import whiten, kmeans2
import scipy.misc
import matplotlib.pyplot as plt
import evaluate


def main():
    img = cv2.imread("test1.png", 1)
    print(f'car positions: {find_cars_approximate(img)}')
    cv2.imshow('img', cv2.imread("test2.png", 1))
    cv2.waitKey(1)
    find_car_direction(img, [25, 55], (640, 480))


def process_img(img):
    state = {}
    cars_pos = find_cars_approximate(img)
    state["player_pos"] = np.array(cars_pos[0])
    state["other_cars_pos"] = np.array(cars_pos[1:])
    state["push_vector"] = evaluate.get_pull_vector(cars_pos[0])
    return state


# Returns positions of the cars
# Player's position is first in the return array
def find_cars_approximate(img):
    st = time.time()

    img_copy = img.copy()

    # crop image to exclude map border
    marginY = 17
    marginX = 21
    img = img[marginY:-marginY, marginX:-marginX]

    # find red pixels
    r = np.array([
        [210, 0, 0],
        [255, 25, 25]
    ])
    within_red = find_close_colors(r, img)
    red_pixels = list(map(list, (zip(within_red[0], within_red[1]))))
    # get rid of outliers in inaccessible parts of the map
    red_pixels = list(filter(lambda x: not ((160 < x[1] < 460) and (100 < x[0] < 220)), red_pixels))

    # find blue pixels
    b = np.array([
        [0, 0, 190],
        [25, 25, 255]
    ])
    within_blue = find_close_colors(b, img)
    blue_pixels = list(map(list, (zip(within_blue[0], within_blue[1]))))

    # find yellow pixels
    y = np.array([
        [180, 180, 0],
        [255, 255, 25]
    ])
    within_yellow = find_close_colors(y, img)
    yellow_pixels = list(map(list, (zip(within_yellow[0], within_yellow[1]))))

    # find 2 cars from collection of pixels
    blue_cars_coords = find_clusters(blue_pixels + yellow_pixels)
    red_cars_coords = find_clusters(red_pixels)

    # convert coordinates to original  resolution
    no_margin_coords = list(map(lambda x: [x[0] + marginY, x[1] + marginX], red_cars_coords + blue_cars_coords))

    print(f'time elapsed: {time.time() - st}')

    # # display found pixels
    # img[within_yellow] = [255, 255, 255]
    # img[within_blue] = [240, 150, 60]
    # img[within_red] = [240, 60, 240]
    # cv2.imshow('original', img_copy)
    # cv2.imshow('changed', img)
    # cv2.waitKey(0)

    return no_margin_coords


# finds positions of pixels such that
# colors[0] < pixel_color < colors[1]
def find_close_colors(colors, img):
    within = np.where(np.all(np.logical_and(
        img >= colors[0],
        img <= colors[1]
    ), axis=-1))
    return within


# divides list of color pixels into 2 clusters
def find_clusters(pos_arr):
    coords = np.array(pos_arr)
    x, y = kmeans2(whiten(coords), 2, 20)
    result = find_pos_from_clusters(coords, y)
    # redo if kmeans haven't found 2 clusters
    while result is None:
        x, y = kmeans2(whiten(coords), 2, 20)
        result = find_pos_from_clusters(coords, y)
    # plt.scatter(coords[:, 0], coords[:, 1], c=y)
    # plt.show()
    return result


# finds average coordinates of 2 clusters
# car with more data points is returned first
def find_pos_from_clusters(coords, distribution):
    pos1 = [0, 0]
    num1 = 0
    pos2 = [0, 0]
    num2 = 0
    for i, point in enumerate(coords):
        if distribution[i] == 0:
            num1 += 1
            pos1 = [pos1[0] + point[0], pos1[1] + point[1]]
        else:
            num2 += 1
            pos2 = [pos2[0] + point[0], pos2[1] + point[1]]
    if num1 == 0 or num2 == 0:
        return None
    pos1 = [int(pos1[0] / num1), int(pos1[1] / num1)]
    pos2 = [int(pos2[0] / num2), int(pos2[1] / num2)]
    return [pos1, pos2] if num1 >= num2 else [pos2, pos1]


def find_car_direction(img, coords, res):
    vic_range = 15
    vicinity = np.full((vic_range * 2, vic_range * 2, 3), 255)
    for x in range(coords[0] - vic_range, coords[0] + vic_range):
        for y in range(coords[1] - vic_range, coords[1] + vic_range):
            if (0, 0) <= (x, y) < res:
                vicinity[x - (coords[0] - vic_range)][y - (coords[1] - vic_range)] = img[x][y]
    for i in vicinity:
        print(i)
    cv2.imshow('1', vicinity / 255.0)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
