import cv2
import numpy as np
from utils import chunks
from maps import LABEL_PADDING

def bytes_to_image(bytes_image):
    '''
    :param bytes_image: encoded image
    :type bytes_image: bytes

    :return: cv2 image
    :type bytes_image: numpy.ndarray
    '''
    np_array = np.fromstring(bytes_image, np.uint8)
    return cv2.imdecode(np_array, cv2.IMREAD_COLOR)

def stitch(images, num_columns):
    '''
    :param images: iterable with images
    :type images: iterable[numpy.ndarray]
    :param num_columns: number of columns present in the image
    :type num_columns: int

    :return: stitched image
    :type bytes_image: numpy.ndarray
    '''
    def process_column(column_images):
        trimmed = [image[LABEL_PADDING:-LABEL_PADDING, :, :] for image in column_images]
        return np.concatenate(trimmed[::-1], axis=0)

    column_images = [process_column(column_images)
                  for column_images in chunks(images, num_columns)]

    result = np.concatenate(column_images, axis=1)

    return result

def write(filename, image):
    return cv2.imwrite(filename, image)
