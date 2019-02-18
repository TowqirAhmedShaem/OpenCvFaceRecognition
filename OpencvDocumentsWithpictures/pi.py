#*********************************************************************************
#   Project Name: Stellar Face Access Management System
 #  Author:
 #         ESP Section: Sopan Sarkar
 #         Module Library: Abdullah Zowad Khan
 #         Module internal processing: Towqir Ahmed Shaem
 #   Contributor: Stellarbd
 #  Author URI: https://www.gitlab.com/AZKZero
 #              https://www.gitlab.com/Shaem
 #  Device Type: Face Recognition
 #  Version: 1.0.0
 #  License: Private
 #*********************************************************************************/

from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import argparse
import imutils
import dlib
from pyfaces import pyfaces
from numpy import asfarray
from PIL import Image
import sys,time
import serial
import cv2
import numpy as np
import MySQLdb
import threading
import Image
import os
os.system("sudo modprobe bcm2835-v4l2")

ser = serial.Serial()
ser.baudrate = 115200
#ser.port = '/dev/ttyACM1'
ser.port = '/dev/ttyACM0'
#ser.port = '/dev/ttyUSB0'
ser.open()

#Connecting with database 
db=MySQLdb.connect(host="localhost",user="root",passwd="rumy",db="opencv")
cursor=db.cursor()

cam=cv2.VideoCapture(0);  
cam.set(3,350)
cam.set(4,250)
cam.set(5, .1)

#For face Allignment

detector = dlib.get_frontal_face_detector()
predictor_path = 'shape_predictor_68_face_landmarks.dat_2'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)


#faceDetect =cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
faceDetect =cv2.CascadeClassifier('lbpcascade_frontalface.xml');
eyeDetect =cv2.CascadeClassifier('haarcascade_eye.xml');

error = "Result: 0"
previouswritingdata = ""

# *******Data segment******** #

# Input Command
recogMode                 =  "0010000"
registraionMode        =  "0020000"
deleteData                  =  "0030000"
deleteAllData             =  "0040000"
readData                     =  "0050000"
writeData                    =  "0070000"
templateCount           =  "0080000"
setSecureLevel           = "0090000"
getSecureLevel           = "0100000"
deviceReadyMode     = "0110000"


# Error Command
inputError                          =  "100000000"
commandError                 =  "100000011"
blurryFaceError                 =  "102000021"
recogModeError                =  "101000011"
regModeError                     =  "102000011"
regMemoryFull                  =  "102000022"
duplicateRegModeError   =  "102000023"
deleteModeError                =  "103000011"
deleteallModeError            =  "104000011"
readModeError                   =  "105000001"
writeModeError                   =  "107000011"
templateModeError            =  "108000011"
securityModeError              =  "109000091"

# Notification Command
notificationForFreeRegMode     =  "102000024"


def faceAllignment(img_path):

    fa = FaceAligner(predictor)
    image = cv2.imread(img_path)
    print img_path
    cv2.imshow("FACE2",image)	
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 2)
    for rect in rects:
	    faceAligned = fa.align(image, gray, rect)
	    cv2.imwrite(img_path, faceAligned)
	    break
	    


def camera() :

    global RegFlag
    global checkOverWriteFlag
    global RecogFlag
    
    #id=raw_input('Enter User ID')
    #id = PyFaces.templateCount()
    id = 1;
    width = 15
    height = 11
    sampleLimit = 4
    sampleNumber = 1
    blurLimit = 500

    RegFlag = False
    RecogFlag = False
    FlagTimeStart = time.time()

    while 1:

            countingTimeStart = time.time()
            FlagTimeEnd = time.time()
            FlagTimeDifference = FlagTimeEnd - FlagTimeStart

            #securityLevel, blurLimit = PyFaces.getSecurityLevel()
	    securityLevel = 2
	    blurLimit = 500

            print 'Security Level : ', securityLevel, '   BlurLimit :  ', blurLimit

            if ( RegFlag == False ) :
                print "Checking For Registration Flag"

                RegFlag = PyFaces.getRegistrationModeForThread()
                if ( RegFlag == True ) :
                    FlagTimeStart = time.time()
                    sampleNumber = 1
                    PyFaces.setRecognizeModeForThread(False)
                    
 
            if( RegFlag == True and FlagTimeDifference < 60 ):
                print "Registration Mode is Still On || Time : " + str(FlagTimeDifference)
                checkOverWriteFlag = PyFaces.getRegistrationModeForThread()

                if ( checkOverWriteFlag == True ) :
                    ser.write (duplicateRegModeError)
                    print "Writing Error Data : " + duplicateRegModeError
                    PyFaces.setRegistrationModeForThread(False)
                    

            if( RegFlag == True and FlagTimeDifference > 59  and FlagTimeDifference < 60):
                print "Time Notification On || Time : " + str(FlagTimeDifference)


            if( RegFlag == True and FlagTimeDifference > 60  and FlagTimeDifference < 61):
                print "Registration Mode is Over ||  + str(FlagTimeDifference)" + str(FlagTimeDifference)
                RegFlag = False
                ser.write (notificationForFreeRegMode)
                print "Writing Notification forFreeregMode : " + notificationForFreeRegMode
                #PyFaces.setRecognizeModeForThread(True)
                
            
            #Recognize Mode         
            if ( RecogFlag == False ) :
                print "Checking For Recognize Flag"
                #RegFlag = PyFaces.setRegistrationModeForThread(True, "Thread")
                RecogFlag = PyFaces.getRecognizeModeForThread()
            
            if ( RecogFlag == True ) :
                print "Checking For Recognize Flag"
                #RegFlag = PyFaces.setRegistrationModeForThread(True, "Thread")
                RecogFlag = PyFaces.getRecognizeModeForThread()

            print "REGFLAG : " , RegFlag
            print "RECOGGFLAG : ", RecogFlag
            
            ret,img=cam.read();
	    '''
            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces=faceDetect.detectMultiScale(gray,1.3,5);
	    '''
            faces=faceDetect.detectMultiScale(img,1.3,5);
            #faces=faceDetect.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5,minSize=(20,20), flags = 0);
            
 


            for(x,y,w,h) in faces:

    		if ( RegFlag == True and sampleNumber <= sampleLimit ):
                    #id = PyFaces.templateCount()
                    
                    ext = ".jpg"
                   
                    Imagename = "" +str(id)+ ext
                    #ImageDirectroy = "/home/pi/FaceAccessControl/OpencvDocuments/dataSet/"
	            ImageDirectroy = "database/"
                    ImageDirectroyFullPicture = "databaseFullPicture/"
                    print "Imagename : " + Imagename
 
                    cv2.imwrite(ImageDirectroy + Imagename, img[y:y+h,x:x+w])
                    ImageFile = ImageDirectroy + Imagename

		    faceAllignment(ImageFile)

                    image = Image.open(ImageFile)
                    image = image.resize((width, height), Image.ANTIALIAS) 
                    image.save(ImageFile)
                    # Checking image whether it is blur or not
                    image = cv2.imread (ImageFile)
                    blurThreshold = cv2.Laplacian( image, cv2.CV_64F).var()
                    blurFlag = True

                    if ( float(blurThreshold) < float(blurLimit) ) :
                        print "Blur Picture Found"
                        blurFlag = False
                    print "Blur value of picture : ", blurThreshold
 
                    # If the picture is good  or not blur 
                    if ( blurFlag ):
                        print "Picture is good"
                        time.sleep(2)
                        PyFaces.saveArrayDataForImage(ImageFile, sampleNumber, sampleLimit)
                        cv2.imwrite( ImageDirectroyFullPicture + Imagename, gray[y:y+h,x:x+w] )

                        if ( sampleNumber == sampleLimit) :
                            RegFlag = False
                            PyFaces.setRegistrationModeForThread(False)
                            FlagTimeStart = time.time()
                            #PyFaces.setRecognizeModeForThread(True)

                        sampleNumber=sampleNumber+1;
                        id = id+1;
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                    print "width : "+ str(w)
                    print "Height : " + str(h)

                    cv2.waitKey(1);

                if ( RecogFlag == True ):
                    matchingTimeStart = time.time()

                    ext = ".jpg"
                    Imagename = "TestImage" +ext
                    #ImageDirectroy = "/home/pi/FaceAccessControl/OpencvDocuments/dataStore/"
                    ImageDirectroyFullPicture = "testFullPicture/"
                    ImageDirectroy=  'test/'

                    cv2.imwrite(ImageDirectroy + Imagename, img[y:y+h,x:x+w])
                    ImageFile = ImageDirectroy + Imagename
		    faceAllignment(ImageFile)

                    image = Image.open(ImageFile)
                    image = image.resize((width, height), Image.ANTIALIAS) 
                    image.save(ImageFile)

                   # Checking image whether it is blur or not
                    image = cv2.imread (ImageFile)
                    blurThreshold = cv2.Laplacian( image, cv2.CV_64F).var()
                    blurFlag = True

                    print "Blur value of picture : ", blurThreshold, "tyepe : ", type(blurThreshold)
                    print "Blur Limit : ", blurLimit , "tyepe : ", type(blurLimit)

                    if ( float(blurThreshold) < float(blurLimit ) ) :
                        print "Blur Picture Found"
                        blurFlag = False
                    print 'Blur Limit : ', blurLimit, '     BlurFlag : ', blurFlag

                    # If the picture is good  or not blur 
                    if  ( blurFlag ):
                         PyFaces.findMatchingImageForThis(countingTimeStart)
                         cv2.imwrite( ImageDirectroyFullPicture + Imagename, gray[y:y+h,x:x+w])
                         time.sleep(.150)

                    # PyFaces.findMatchingImageForThis(countingTimeStart)

                    # time.sleep(.100)
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

                    cv2.waitKey(1);
                    matchingTimeEnd = time.time()
                    print "Matching Time : ",  matchingTimeEnd - matchingTimeStart

    
            cv2.imshow("FACE",img)
            if(cv2.waitKey(1) == ord('q')):
            	break;

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
	print
	print
	print
	print "--------------------------------------------------------------------------------"
        start = time.time()
        PyFaces = pyfaces.PyFacesForGeneralPurpose()

        # Enabling Camera Thread        
        t = threading.Thread(target = camera)
        t.start()
        '''
        #Device Ready Mode Command
        ser.write(deviceReadyMode)
        ser.flush()
        time.sleep(.100)
        '''
        while 1:

                loopStartTime = time.time()
                data = ser.readline()
                print "Serial Data : " + str(data)

                if data.find(error) == -1 :
                    print "Right Data : " + data
                    #data = "0020000"
                    if(len(data) > 0 ):
                        pyf=pyfaces.PyFaces(data)
                   
                loopEndTime = time.time()
                print "Loop processing time : " + str(loopEndTime - loopStartTime)


        end = time.time()
        print 'Took :',(end-start),'Sec'
	print "--------------------------------------------------------------------------------"
	print
	print
	print
    except Exception,detail:
        print detail.args
        print "usage:python pyfacesdemo imgname dirname numofeigenfaces threshold "
