from os import (listdir, path)
import numpy as np
from util import pipe_through
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

def main():
    image_folder = '/vagrant/Homework1/sample_drive/cam_3'
    reset_every = 500

    images = create_image_generator(image_folder)
    first_image = next(images) # given the number of images we can safely ignore the first

    process = pipe_through(to_grayscale, threshold, dilate, detect_edges)

    image_shape = to_grayscale(first_image).shape
    acc = empty_image(image_shape)

    for (idx, image) in enumerate(images):
        if idx % reset_every == 0:
            write_image('/vagrant/Homework1/results/res@3:' + str(idx) + '.jpg', acc)
            acc = empty_image(image_shape)
        acc = acc + process(image)


if __name__ == '__main__':
    main()
