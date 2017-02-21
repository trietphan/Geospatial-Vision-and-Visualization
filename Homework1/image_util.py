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

def threshold(low):
    high = 255
    def threshold_fn(image):
        _, result = cv2.threshold(image,
                                  low,
                                  high,
                                  cv2.THRESH_BINARY)
        return result
    return threshold_fn

def equalize_hist(image):
    return cv2.equalizeHist(image)

def median_blur(image):
    return cv2.medianBlur(image, 7)

def bilateral(image):
    return cv2.bilateralFilter(image, 11, 17, 17)

def clahe(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apply(image)

def draw_contours(take):
    ''' Returns a function that draws `take` contours '''
    (max_contour_area, min_contour_area) = (20000, 2000)

    def draw_contours_fn(image):
        ''' Draws `take` contours found on `image`
            Returns a grayscale canvas with just `take` contours
            drawn on it.
            Original `image` is not modified.
        '''

        result = empty_image(image.shape)
        image_copy = image.copy()
        _, contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        image = image_copy # findContours modifies image so we swap it out for a copy
        contours = [c
                    for c in contours
                    if cv2.contourArea(c) > min_contour_area and cv2.contourArea(c) < max_contour_area]

        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:take]
        cv2.drawContours(result, contours, -1, 255, cv2.FILLED)
        return result

    return draw_contours_fn

def empty_image(image_shape):
    return np.zeros(image_shape, np.uint8)
