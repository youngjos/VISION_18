import cv2
import numpy as np
import configparser

config = configparser.RawConfigParser()
config.read('config.txt')

H_LOW = config.get('hsv_vals', 'h_low')
S_LOW = config.get('hsv_vals', 's_low')
V_LOW = config.get('hsv_vals', 'v_low')
H_HIGH = config.get('hsv_vals', 'h_high')
S_HIGH = config.get('hsv_vals', 's_high')
V_HIGH = config.get('hsv_vals', 'v_high')

def apply_threshold(image_name, h_low, s_low, v_low, h_high, s_high, v_high): #paramater 'image' to be replaced with a live steam from the robot.

    image = cv2.imread(image_name)

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    LOW_HSV = np.array([h_low, s_low, v_low], np.uint8)
    HIGH_HSV = np.array([h_high, s_high, v_high], np.uint8)

    threshold = cv2.inRange(hsv_image, LOW_HSV, HIGH_HSV)

    cv2.imwrite('ImageOutput.jpg', threshold)

    return

apply_threshold('image.jpg', H_LOW, S_LOW, V_LOW, H_HIGH, S_HIGH, V_HIGH)





