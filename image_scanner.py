import cv2
import numpy as np
import time
from scipy.cluster.vq import whiten, kmeans2
import matplotlib.pyplot as plt


def main():
    print(f'car positions: {find_cars_approximate()}')


# TODO: separate player's car position from other cars
def find_cars_approximate():
    st = time.time()

    img = cv2.imread('test.png', 1)
    img_copy = img.copy()

    # crop image to exclude map border
    marginY = 17
    marginX = 21
    img = img[marginY:-marginY, marginX:-marginX]

    # find red pixels
    r = np.array([
        [0, 0, 210],
        [25, 25, 255]
    ])
    within_red = find_close_colors(r, img)
    red_pixels = list(map(list, (zip(within_red[0], within_red[1]))))
    # get rid of outliers in inaccessible parts of the map
    red_pixels = list(filter(lambda x: not ((160 < x[1] < 460) and (100 < x[0] < 220)), red_pixels))

    # find blue pixels
    b = np.array([
        [190, 0, 0],
        [255, 25, 25]
    ])
    within_blue = find_close_colors(b, img)
    blue_pixels = list(map(list, (zip(within_blue[0], within_blue[1]))))

    # find yellow pixels
    y = np.array([
        [0, 180, 180],
        [25, 255, 255]
    ])
    within_yellow = find_close_colors(y, img)
    yellow_pixels = list(map(list, (zip(within_yellow[0], within_yellow[1]))))

    # find 2 cars from collection of pixels
    blue_cars_coords = find_clusters(blue_pixels + yellow_pixels)
    red_cars_coords = find_clusters(red_pixels)

    # convert coordinates to original  resolution
    no_margin_coords = list(map(lambda x: [x[0] + marginY, x[1] + marginX], blue_cars_coords + red_cars_coords))

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
    return [pos1, pos2]


if __name__ == "__main__":
    main()
