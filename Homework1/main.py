import cv2
from os import (listdir, path)
import numpy as np
from util import pipe_through

def read_image(path_to_image):
    return cv2.imread(path_to_image)

def write_image(path_to_result, result):
    cv2.imwrite(path_to_result, result)

def create_image_generator(folder):
    files = listdir(folder)

    return (read_image(path.join(folder, filename))
            for filename in files[:100])

def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def detect_edges(image):
    (treshold_low, treshold_high) = (20, 120)
    return cv2.Canny(image, treshold_low, treshold_high)

def dilate(image):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)

def threshold(image):
    (treshold_low, threshold_high) = (120, 255)
    _, result = cv2.threshold(image,
                              treshold_low,
                              threshold_high,
                              cv2.THRESH_BINARY_INV)
    return result

def equalize_hist(image):
    return cv2.equalizeHist(image)

def main():
    image_folder = '/vagrant/Homework1/sample_drive/cam_3'

    # second generator is for pairwise images
    # and to get the first image dimensions
    images_from_1 = create_image_generator(image_folder)
    images_from_2 = create_image_generator(image_folder)
    first_image = next(images_from_2)

    process = pipe_through(to_grayscale, threshold, dilate, detect_edges)

    acc = np.zeros(to_grayscale(first_image).shape, np.uint8)
    for (idx, image) in enumerate(images_from_1):
        acc = acc + process(image)
        write_image('/vagrant/Homework1/results/res' + str(idx) + '.jpg', acc)

    write_image('/vagrant/Homework1/results/res.jpg', acc)

if __name__ == '__main__':
    main()
