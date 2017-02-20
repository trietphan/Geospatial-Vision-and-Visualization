import cv2
import numpy as np

def read_image(path_to_image):
    return cv2.imread(path_to_image)

def write_image(path_to_result, result):
    cv2.imwrite(path_to_result, result)

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
