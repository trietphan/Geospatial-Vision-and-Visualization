import cv2
from os import (listdir, path)
import numpy as np


def read_image(path_to_image, gray=True):
    return cv2.imread(path_to_image, 0 if gray is True else 1)

def write_image(path_to_result, result):
    cv2.imwrite(path_to_result, result)

def create_image_generator(folder):
    [first_file, *remaining_files] = listdir(folder)

    def generator():
        for filename in remaining_files[:20]:
            yield read_image(path.join(folder, filename))

    return (read_image(path.join(folder, first_file)), generator)

def main():
    image_folder = '/vagrant/Homework1/sample_drive/cam_3'

    (first_image, images) = create_image_generator(image_folder)

    print('first', first_image.shape)
    for image in images():
        print(image.shape)

main()
