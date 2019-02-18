import cv2
import numpy as np

image = cv2.imread('/home/shaem/blackimage/3.jpg')
r = 150.0 / image.shape[1]
dim = (150, int(image.shape[0] * r))
resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
lower_white = np.array([220, 220, 220], dtype=np.uint8)
upper_white = np.array([255, 255, 255], dtype=np.uint8)
mask = cv2.inRange(resized, lower_white, upper_white) # could also use threshold
res = cv2.bitwise_not(resized, resized, mask)
cv2.imshow('res', res) # gives black background
