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

def get_contours(image): # takes an image (probably masked) and finds the contours.
    img, contours, hierarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
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

def draw_largest_box(image) : # takes a masked image, draws a bounding box around the largest contour, and returns the x y cooridinates of the top left point, width and height, and angle of box.
    masked_im = get_mask(image)
    contours = get_contours(masked_im)
    largest_contour = find_largest_contour(contours)
    rect = cv2.minAreaRect(largest_contour)
    (x,y),(width,height), theta = cv2.minAreaRect(largest_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    image = cv2.drawContours(image, [box], 0, (0, 0, 255), 2)
    cv2.imwrite("target.jpg", image)

    return theta


masked = cv2.imread("image.jpg")
print(draw_largest_box(masked))









