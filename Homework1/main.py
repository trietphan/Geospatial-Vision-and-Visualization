from os import (listdir, path)
import numpy as np
from util import pipe_through
from image_util import (
    read_image,
    write_image,
    threshold,
    dilate,
    detect_edges,
    to_grayscale
)

def create_image_generator(folder):
    files = listdir(folder)

    return (read_image(path.join(folder, filename))
            for filename in files[:100])

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
