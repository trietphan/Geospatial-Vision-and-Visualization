from os import (listdir, path, makedirs)
import numpy as np
from util import (pipe_through, last)
from image_util import (
    read_image,
    write_image,
    threshold,
    dilate,
    detect_edges,
    to_grayscale,
    empty_image
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
    process = pipe_through(to_grayscale, threshold, dilate, detect_edges)

    acc = empty_image(image_shape)
    for (idx, image) in enumerate(images):
        if idx % reset_every == 0:
            yield (acc, idx)
            acc = empty_image(image_shape)
        acc = acc + process(image)


def main():
    input_folder = '/vagrant/Homework1/sample_drive/cam_3'
    output_folder = '/vagrant/Homework1/results'

    if not path.exists(output_folder):
        makedirs(output_folder)

    get_result_title = lambda idx: last(path.split(input_folder)) + '@' + str(idx) + '.jpg'
    get_result_path = lambda idx: path.join(output_folder, get_result_title(idx))

    for (clean_image, idx) in clean_images(input_folder, reset_every=500):
        # TODO: look for stains in clean_image
        write_image(get_result_path(idx), clean_image)

if __name__ == '__main__':
    main()
