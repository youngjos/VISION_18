import cv2
import numpy as np
import math
import json

with open('config.json') as json_data_file:
    config = json.load(json_data_file)

class camera :
    FOV = config['camera']['fov']
    RESOLUTION_X = config['camera']['resolution_width']
    RESOLUTION_Y = config['camera']['resolution_height']

class hsv :

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

def get_width_of_target(image) : # takes an image and finds the width of the target
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

def get_x_offset(image) : # takes image and finds the x offset of the target in relation to the center of the image.
    center_image = get_center_of_image(image)
    center_target = get_center_of_target(image)

    return center_target[0] - center_image[0]

def get_y_offset(image) : # takes image and finds the y offset of the target in relation to the center of the image.
    center_image = get_center_of_image(image)
    center_target = get_center_of_target(image)

    return center_target[1] - center_image[1]

def get_offset_angle(image) : # takes an image and finds the angle offset of the target.
    x_offset = get_x_offset(image)
    x_res = camera.RESOLUTION_X
    y_res = camera.RESOLUTION_Y
    fov = camera.FOV
    x_res *= x_res
    y_res *= y_res
    diagonal_pixels = math.sqrt(x_res + y_res)
    degree_per_pixel = fov / diagonal_pixels
    offset_angle =  degree_per_pixel * x_offset

    return offset_angle

def get_horizontal_offset_degrees(image):
    centerPoint = get_center_of_target(image)
    horizontalFov = 63.54
    resWidth = get_width_of_image(image)
    return ((centerPoint[0] * horizontalFov) / resWidth) - (horizontalFov / 2)

def get_horizontal_offset_radians(image) :
    return (get_horizontal_offset_degrees(image)  * (2 * math.pi)) / 360.0

def get_x_offset_inches(image) :
    real_target_width = 12 # real target width in inches tho

    return (get_x_offset(image) * real_target_width) / get_width_of_target(image)

def get_distance(image) :
    return get_x_offset_inches(image) / math.tan(get_horizontal_offset_radians(image))

def get_distance_2(image) : # needs hella work...
    return math.sqrt((get_x_offset_inches(image) * get_x_offset_inches(image)) * (get_distance(image) * get_distance(image)))

image = cv2.imread("IMG_0184.JPG")
get_mask(image)
cv2.imwrite("masked.JPG", get_mask(image))

print(get_distance(image))




















