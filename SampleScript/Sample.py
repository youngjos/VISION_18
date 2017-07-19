import cv2
import numpy as np

# Gimp uses H = 0-360, S = 0-100 and V = 0-100. But OpenCV uses  H: 0 - 180, S: 0 - 255, V: 0 - 255

#live image capture filtering our yellow stuff and light green for some reason... Still looking into hsv color ranges kinda just trial and error until it worked...
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()
    hsv_cap = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    YELLOW_MIN = np.array([20,175,75],np.uint8)
    YELLOW_MAX = np.array([75,255,255],np.uint8);

    cap_treshhold = cv2.inRange(hsv_cap, YELLOW_MIN, YELLOW_MAX)
    cv2.imshow('frame', cap_treshhold)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#code for changing that one sample image
img = cv2.imread('SampleInput.jpg')
hLow = 5
sLow = 50
vLow = 50
hHigh = 15
sHigh = 255
vHigh = 255

ORANGE_MIN = np.array([hLow, sLow, vLow],np.uint8)
ORANGE_MAX = np.array([hHigh, sHigh, vHigh],np.uint8)

hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

frame_threshed = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
cv2.imwrite('SampleOutput.jpg', frame_threshed)