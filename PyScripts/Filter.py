import cv2
import numpy as np
import configparser
from scipy.interpolate import splprep, splev

config = configparser.RawConfigParser()
config.read('config.txt')

H_LOW = config.get('hsv_vals', 'h_low')
S_LOW = config.get('hsv_vals', 's_low')
V_LOW = config.get('hsv_vals', 'v_low')
H_HIGH = config.get('hsv_vals', 'h_high')
S_HIGH = config.get('hsv_vals', 's_high')
V_HIGH = config.get('hsv_vals', 'v_high')

LOW_HSV = np.array([H_LOW, S_LOW, V_LOW], np.uint8)
HIGH_HSV = np.array([H_HIGH, S_HIGH, V_HIGH], np.uint8)

def filter(image_name): #paramater 'image' to be replaced with a live steam from the robot.

    image = cv2.imread(image_name) #reads in image

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # converts original into hsv

    threshold = cv2.inRange(hsv_image, LOW_HSV, HIGH_HSV) # applys hsv threshold to hsv image

    cv2.imwrite('image_output.jpg', threshold) # writes out result from previous

    cv2.imwrite('image_output.jpg', threshold) # prints it

    res = cv2.bitwise_and(image, image, mask = threshold) #cturns into more basic, contourable image

    res_grayscale = cv2.imread('image_output.jpg', 0) # turns into grayscale for contouring

    res_grayscale_contoured, contours, hierarchy = cv2.findContours(res_grayscale, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # finds contours

    cv2.drawContours(res, contours, -1, (0, 0, 255), 2) # draws contours onto res image

    cv2.imwrite('image_output_2.jpg', res) # prints image with contours

    return

filter('image.jpg')





