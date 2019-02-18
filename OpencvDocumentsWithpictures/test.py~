
import  cv2
from PIL import Image
import os
os.system("sudo modprobe bcm2835-v4l2")

#faceDetect =cv2.CascadeClassifier('haarcascade_frontalface_default.xml');

#faceDetect =cv2.CascadeClassifier('lbpcascade_profileface.xml');
#faceDetect =cv2.CascadeClassifier('lbpcascade_silverware.xml');
#faceDetect =cv2.CascadeClassifier('lbpcascade_frontalface.xml');
faceDetect =cv2.CascadeClassifier('lbpcascade_frontalface.xml');

cam = cv2.VideoCapture(0)
cam.set(3,350)
cam.set(4,250)
cam.set(5, .1)

width = 15
height = 11

while True:

    ret, img = cam.read(0)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    
    for(x,y,w,h) in faces:
        ext = ".jpg"
        Imagename = "" +str(id)+ ext
        ImageDirectroy = "/home/pi/FaceAccessControl/OpencvDocuments/dataSet/"

        cv2.imwrite(ImageDirectroy + Imagename, gray[y:y+h,x:x+w])
        '''
        ImageFile = ImageDirectroy + Imagename
        # Checking image whether it is blur or not
        image = cv2.imread (ImageFile)
        blurThreshold = cv2.Laplacian( image, cv2.CV_64F).var()
        print "Blur Value : ",blurThreshold

        image = Image.open(ImageFile)
        image = image.resize((width, height), Image.ANTIALIAS) 
        image.save(ImageFile)

        image = cv2.imread (ImageFile)
        blurThreshold = cv2.Laplacian( image, cv2.CV_64F).var()
        print "Blur Value for 15x11  : ", blurThreshold
        '''
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.waitKey(1);   

    cv2.imshow("Image",img)

    if cv2.waitKey(1)==ord('q'):
        break



