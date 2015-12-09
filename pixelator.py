__author__ = 'Rick'

import cv2
import numpy as np


def main():

    img = cv2.imread('/images/test002/in.jpg', 0)
    img = cv2.equalizeHist(img)
    dst_img = pixelate(img, 64, 64)
    c_img = colorize(dst_img, [0, 31, 63, 95, 127, 159, 191, 223, 255])
    s_dst_img = scale_image(c_img, 10, 14)

    cv2.imwrite('/images/test002/outc.png', c_img)
    cv2.imwrite('/images/test002/outg.png', img)
    cv2.imwrite('/images/test002/outp.png', dst_img)
    cv2.imwrite('/images/test002/outsp.png', s_dst_img)


def pixelate(image, blocks_in_width, blocks_in_height):
    dst_img = np.zeros((blocks_in_height, blocks_in_width), np.uint8)
    height, width = image.shape

    width_of_block, y_r = divmod(width, blocks_in_width)
    y0 = y_r // 2

    height_of_block, x_r = divmod(height, blocks_in_height)
    x0 = x_r // 2
    for i in range(blocks_in_height):
        for j in range(blocks_in_width):
            i_min = x0 + i * height_of_block
            i_max = i_min + height_of_block
            j_min = y0 + j * width_of_block
            j_max = j_min + width_of_block
            mask = image[i_min:i_max, j_min:j_max]

            dst_img[i][j] = mask.mean()

    return dst_img


def scale_image(image, scale_width, scale_height):
    height, width = image.shape
    dst_img = np.zeros((height*scale_height, width*scale_width), np.uint8)
    for i in range(height):
        for j in range(width):
            dst_img[i*scale_height:(i+1)*scale_height, j*scale_width:(j+1)*scale_width] = image[i][j]

    return dst_img


def colorize(image, color_set):
    height, width = image.shape
    for i in range(height):
        for j in range(width):
            image[i][j] = get_closest_color(image[i][j], color_set)
    return image


def get_closest_color(pixel, color_set):
    c = color_set[0]
    min_c_dist = color_distance1(c, pixel)
    for color in color_set:
        c_dist = color_distance1(color, pixel)
        if c_dist < min_c_dist:
            c = color
            min_c_dist = c_dist
    return c


def color_distance1(c1, c2):
    return abs(c1 - c2)


if __name__ == "__main__":
    main()
