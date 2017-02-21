import cv2
import numpy as np

def read_image(path_to_image):
    return cv2.imread(path_to_image)

def write_image(path_to_result, result):
    cv2.imwrite(path_to_result, result)

def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def detect_edges(image):
    (treshold_low, treshold_high) = (130, 150)
    return cv2.Canny(image, treshold_low, treshold_high)

def dilate(image):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)

def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

def threshold(image):
    (treshold_low, threshold_high) = (130, 255)
    _, result = cv2.threshold(image,
                              treshold_low,
                              threshold_high,
                              cv2.THRESH_BINARY)
    return result

def equalize_hist(image):
    return cv2.equalizeHist(image)

def median_blur(image):
    return cv2.medianBlur(image, 7)

def bilateral(image):
    return cv2.bilateralFilter(image, 11, 17, 17)

def clahe(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apply(image)

def draw_contours(image):
    (max_contour_area, min_contour_area) = (20000, 2000)

    result = image.copy()
    _, contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = [c
                for c in contours
                if cv2.contourArea(c) > min_contour_area and cv2.contourArea(c) < max_contour_area]

    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
    result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(result, contours, -1, (0, 255, 0), 3)
    return result

def empty_image(image_shape):
    return np.zeros(image_shape, np.uint8)
