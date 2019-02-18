# import the necessary packages
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import argparse
import imutils
import dlib
import cv2
import time
import os
os.system("sudo modprobe bcm2835-v4l2")

'''
Wroking Procedure 
*) Image Read
*) DetectMultiScale
*) Allignment
*) Save
Time Needed : 6s for Picture Size : 340x255

'''
fulltimeStart = time.time()
detector = dlib.get_frontal_face_detector()
faceDetect =cv2.CascadeClassifier('lbpcascade_frontalface.xml');
predictor_path = 'shape_predictor_68_face_landmarks.dat_2'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
fa = FaceAligner(predictor)

cam=cv2.VideoCapture(0);  
cam.set(3,350)
cam.set(4,250)
cam.set(5, .1)

startingTime = time.time()
print 'starting'

# load the input image, resize it, and convert it to grayscale
img_path = '/home/pi/gitlab/FaceAccessControl/ImageProcessingfordetection/blackimage/19.jpg'
image = cv2.imread(img_path)

graytimeStart = time.time()
gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
graytimeEnd = time.time()
print "Time For converting picture into gray : ", graytimeEnd-graytimeStart

faces=faceDetect.detectMultiScale(gray,1.3,5);
print 'Face Extracted'
Imagename = '/home/pi/gitlab/FaceAccessControl/ImageProcessingfordetection/blackimage/230.jpg' 
for(x,y,w,h) in faces:
        cv2.imwrite( Imagename, gray[y:y+h,x:x+w] )


img_path = '/home/pi/gitlab/FaceAccessControl/ImageProcessingfordetection/blackimage/230.jpg'
image = cv2.imread(img_path)
gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
rects = detector(gray, 2)

# loop over the face detections
for rect in rects:
	faceAligned = fa.align(image, gray, rect)
	cv2.imwrite('/home/pi/gitlab/FaceAccessControl/ImageProcessingfordetection/blackimage/231.jpg', faceAligned)
	endingTime = time.time()
	print 'Time for Image processing', endingTime - startingTime
	print 'Total Time for Image processing', endingTime - fulltimeStart	
	break

















