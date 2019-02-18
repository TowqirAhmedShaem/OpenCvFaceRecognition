#********************************************************************************** #
#	    Project Name: Stellar Face Recognition Access Management System         #
#           Site : www.stellarbd.com                                                #
#	    Library Author: Abdullah Zowad Khan; Towqir Ahmed Shaem;                #
#	    Device Type: OrangePi One module                                        #
#	    Version: 1.0.0                                                          #
#	    License: Private                                                        #
#***********************************************************************************#


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
#os.system("sudo modprobe bcm2835-v4l2") #It is only for raspberry pi for loadind CS camera driver

ser = serial.Serial()
ser.baudrate = 115200
#ser.port = '/dev/ttyACM0'
ser.port = '/dev/ttyUSB0'
ser.open()

#Connecting with database 
db=MySQLdb.connect(host="localhost",user="root",passwd="rumy",db="opencv")
cursor=db.cursor()

cam=cv2.VideoCapture(0);  
cam.set(3,600)
cam.set(4,500)
cam.set(5, .1)

faceDetect =cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
eyeDetect =cv2.CascadeClassifier('haarcascade_eye.xml');

error = "Result: 0"
previouswritingdata = ""

# *******Data segment******** #

# Input Command
recogMode               =  "0010000"
registraionMode         =  "0020000"
deleteData              =  "0030000"
deleteAllData           =  "0040000"
readData                =  "0050000"
writeData               =  "0070000"
templateCount           =  "0080000"


# Error Command
inputError              =  "100000000"
commandError            =  "100000011"
blurryFaceError         =  "102000021"
recogModeError          =  "101000011"
regModeError            =  "102000011"
regMemoryFull           =  "102000022"
duplicateRegModeError   =  "102000023"
deleteModeError         =  "103000011"
deleteallModeError      =  "104000011"
readModeError           =  "105000001"
writeModeError          =  "107000011"
templateModeError       =  "108000011"

# Notification Command
notificationForFreeRegMode     =  "102000024"


def camera() :

    global RegFlag
    global checkOverWriteFlag
    global RecogFlag
    


    #id=raw_input('Enter User ID')
    id = PyFaces.templateCount()
    width = 15
    height = 11
    sampleLimit = 5
    sampleNumber = 1

    RegFlag = False
    RecogFlag = False
    FlagTimeStart = time.time()


    while 1:

            FlagTimeEnd = time.time()
            FlagTimeDifference = FlagTimeEnd - FlagTimeStart

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
                PyFaces.setRecognizeModeForThread(True)
                
            
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
            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces=faceDetect.detectMultiScale(gray,1.3,5);

            for(x,y,w,h) in faces:

    		if ( RegFlag == True and sampleNumber <= sampleLimit ):

                    id = PyFaces.templateCount()
                    print "present id : " + str(id)

                    ext = ".jpg"
                    Imagename = "" +str(id)+ ext
                    ImageDirectroy = "/home/pi/FaceAccessControl/OpencvDocuments/dataSet/"
                    print "Imagename : " + Imagename
 
                    cv2.imwrite(ImageDirectroy + Imagename, gray[y:y+h,x:x+w])

                    ImageFile = ImageDirectroy + Imagename
                    image = Image.open(ImageFile)
                    image = image.resize((width, height), Image.ANTIALIAS) 
                    image.save(ImageFile)
                
                    PyFaces.saveArrayDataForImage(ImageFile, sampleNumber)
        

                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                    print "width : "+ str(w)
                    print "Height : " + str(h)

                    cv2.waitKey(1);
            	    sampleNumber=sampleNumber+1;
                    cv2.imshow("Registration",img)


                if ( RecogFlag == True ):

                    ext = ".jpg"
                    Imagename = "TestImage" +ext
                    ImageDirectroy = "/home/pi/FaceAccessControl/OpencvDocuments/dataStore/"

                    cv2.imwrite(ImageDirectroy + Imagename, gray[y:y+h,x:x+w])

                    ImageFile = ImageDirectroy + Imagename
                    image = Image.open(ImageFile)
                    image = image.resize((width, height), Image.ANTIALIAS) 
                    image.save(ImageFile)

                    PyFaces.findMatchingImageForThis( )

                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                    print "width : "+ str(w)
                    print "Height : " + str(h)

                    cv2.waitKey(1);
                    cv2.imshow("RecogMode",img)
    
               # break;        
            cv2.imshow("FACE",img)
            #break; #for testing
            if(cv2.waitKey(10) == ord('q')):
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
        
        while 1:

                loopStartTime = time.time()
                #camera()

                data = ser.readline()
                print "Serial Data : " + str(data)

                if data.find(error) == -1 :
                    print "Right Data : " + data
                    #data = "0010000"
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
