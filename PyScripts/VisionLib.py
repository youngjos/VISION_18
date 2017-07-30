import cv2
import numpy as np
import math
import json

class hsv :

    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    # Reads calibrated HSV values and turns them into an array for class use.
    h_low = config['hsv']['h_low']
    s_low = config['hsv']['s_low']
    v_low = config['hsv']['v_low']
    h_high = config['hsv']['h_high']
    s_high = config['hsv']['s_high']
    v_high = config['hsv']['v_high']

    low_hsv = np.array([h_low, s_low, v_low], np.uint8)
    high_hsv = np.array([h_high, s_high, v_high], np.uint8)

    def refresh_hsv(self) : # reads calibrated HSV values and turns them into an array for script use.
        self.h_low = self.config['hsv']['h_low']
        self.s_low = self.config['hsv']['s_low']
        self.v_low = self.config['hsv']['v_low']
        self.h_high = self.config['hsv']['h_high']
        self.s_high = self.config['hsv']['s_high']
        self.v_high = self.config['hsv']['v_high']
        self.low_hsv = np.array([self.h_low, self.s_low, self.v_low], np.uint8)
        self.high_hsv = np.array([self.h_high, self.s_high, self.v_high], np.uint8)
        return

def get_mask(image) : # takes bgr image and converts it into filtered hsv image with no noise, assuiming hsv vals are calibrated.
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # converts original into hsv
    masked = cv2.inRange(hsv_image, hsv.low_hsv, hsv.high_hsv)  # applies hsv threshold to hsv image
    return masked

def get_contours(image): # takes an image and finds the contours.
    masked = get_mask(image)
    img, contours, hierarchy = cv2.findContours(masked, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours

def find_largest_contour(contours) : # takes an array of contours and find the largest one out of the array.
    largest_area = 0
    largest_contour_index = 0

    size = len(contours) # size is amount of objects in contours NOT the last index!

    for n in range(0, size):
        cnt = contours[n]
        if(cv2.contourArea(cnt) > largest_area):
            largest_area = cv2.contourArea(cnt)
            largest_contour_index = n

    return contours[largest_contour_index]

def get_largest_box(image) : # takes a image, draws a bounding box around the largest contour, and returns the x y cooridinates of the top left point, width and height.
    contours = get_contours(image)
    largest_contour = find_largest_contour(contours)
    x, y, w, h = cv2.boundingRect(largest_contour)
    #image = cv2.drawContours(image, largest_contour, 0, (0, 0, 255), 2)
    #cv2.imwrite("target.jpg", image)

    return x, y, w, h

def get_center_of_target(image) : # takes image and finds the center of the target.
    x, y, w, h = get_largest_box(image)
    half_width = w/2
    half_height = h/2
    center_x = int(x + half_width)
    center_y = int(y + half_height)
    center_point = [center_x, center_y]

    return center_point

def get_center_of_image(image) : # takes image and finds the center of the image.
    height, width, channels = image.shape
    center_point = [int(width/2), int(height/2)]
    return center_point

def get_area_of_target(image) : # takes an image and finds the area of the target
    x, y, w, h = get_largest_box(image)

    return w * h

def get_width_of_target(image) : # takes an image and finds the widtb of the target
    x, y, w, h = get_largest_box(image)

    return w

def get_height_of_target(image) : # takes an image and finds the height of the target
    x, y, w, h = get_largest_box(image)

    return h

def get_width_of_image(image) : # takes image and finds the width of the image.
    height, width, channels = image.shape

    return width

def get_height_of_image(image) : # takes image and finds the height of the image.
    height, width, channels = image.shape

    return height

















