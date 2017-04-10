from centers import find_centers
from maps import get_images
from images import (stitch, write, bytes_to_image)


def main():
    latlon1 = (41.835095, -87.628891)
    latlon2 = (41.836216, -87.627802)

    (centers, num_columns) = find_centers(latlon1, latlon2)

    images = get_images(centers)
    write(stitch(map(bytes_to_image, images), num_columns))


if __name__ == '__main__':
    main()
