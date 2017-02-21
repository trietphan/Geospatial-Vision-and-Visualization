from os import (listdir, path, makedirs)
from math import floor
import numpy as np
from util import (pipe_through, last)
from image_util import (
    read_image,
    write_image,
    threshold,
    dilate,
    detect_edges,
    to_grayscale,
    empty_image,
    erode,
    median_blur,
    draw_contours
)

def create_image_generator(folder):
    files = listdir(folder)

    return (read_image(path.join(folder, filename))
            for filename in files)

def clean_images(input_folder, reset_every=500):
    ''' Generator of clean images. Applies `process` function on
        every image in `input_folder` and sums them up.

        yields ([[np.uint8]], int) - (summed up results `process`d images, index)
    '''
    images = create_image_generator(input_folder)
    first_image = next(images) # given the number of images we can safely ignore the first
    image_shape = to_grayscale(first_image).shape

    # TODO: add/change function in this pipeline for better results
    # TODO: try to adjust number in any of the existing functions at image_util.py
    process = pipe_through(to_grayscale, threshold(120), dilate, detect_edges)

    acc = empty_image(image_shape)
    for (idx, image) in enumerate(images):
        acc = acc + process(image)
        if idx % reset_every == 0:
            yield (acc, idx)
            acc = empty_image(image_shape)

def get_most_frequent_contours(input_images):
    ''' Takes in an iterable with clean (must be grayscale) images and
        finds the most common contours that occur in every image.
    '''
    postprocess = pipe_through(erode, dilate, median_blur, threshold(120), draw_contours(5))
    images = list(input_images)

    result_image = sum([postprocess(image) / len(images)
                        for (image, _) in images])

    tollerance = 5
    max_pixel_value = max(result_image.flatten())

    return threshold(floor(max_pixel_value) - tollerance)(result_image.astype(np.uint8))


def main():
    input_folder = '/vagrant/Homework1/sample_drive/cam_3'
    output_folder = '/vagrant/Homework1/results'

    if not path.exists(output_folder):
        makedirs(output_folder)

    get_result_title = lambda input_folder: '.'.join([last(path.split(input_folder)), 'result', 'jpg'])
    get_result_path = lambda input_folder, output_folder: path.join(output_folder, get_result_title(input_folder))

    write_image(path.join(output_folder, get_result_path(input_folder, output_folder)),
                get_most_frequent_contours(clean_images(input_folder, reset_every=500)))


if __name__ == '__main__':
    main()
