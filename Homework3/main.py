from centers import find_centers
from maps import get_images
from images import (stitch, write, bytes_to_image)


def run(latlon1, latlon2, result_path):
    (centers, num_columns) = find_centers(latlon1, latlon2)

    images = get_images(centers)
    write(result_path,
          stitch(map(bytes_to_image, images), num_columns))
