import cv2
import numpy as np
from utils import chunks
from maps import LABEL_PADDING

def bytes_to_image(bytes_image):
    np_array = np.fromstring(bytes_image, np.uint8)
    return cv2.imdecode(np_array, cv2.IMREAD_COLOR)

def stitch(images, num_columns):
    def process_column(column_images):
        trimmed = [image[LABEL_PADDING:-LABEL_PADDING, :, :] for image in column_images]
        return np.concatenate(trimmed[::-1], axis=0)

    column_images = [process_column(column_images)
                  for column_images in chunks(images, num_columns)]

    result = np.concatenate(column_images, axis=1)

    return result

    # col_img

def write(image):
    return cv2.imwrite("result1.jpg", image)
