import sys
import serial
import numpy as np
from numpy import max
from numpy import zeros
from numpy import average
from numpy import dot
from numpy import asfarray
from numpy import sort
from numpy import trace
from numpy import argmin
from numpy.linalg import *
import MySQLdb


from os.path import isdir,join,normpath
from os import listdir,mkdir
from shutil import rmtree
import pickle
from math import sqrt

import imageops

ser = serial.Serial()
ser.baudrate = 115200
#ser.port = '/dev/ttyACM1'
#ser.port = '/dev/ttyACM0'
ser.port = '/dev/ttyUSB0'
ser.open()

#Connecting with database 
db=MySQLdb.connect(host="localhost",user="root",passwd="rumy",db="opencv")
cursor=db.cursor()

#Variable 
global pictureData
pictureData = ""


class ImageError(Exception):
    pass

class DirError(Exception):
    pass 

class FaceBundle:
    def __init__(self,wd,ht,adjfaces,fspace,avgvals,evals):

        self.wd=wd
        self.ht=ht
        self.adjfaces=adjfaces
        self.eigenfaces=fspace
        self.avgvals=avgvals
        self.evals=evals
        
class FaceRec:    
    
    def findmatchingimage(self,imagename,selectedfacesnum,thresholdvalue):    

        print "Selected Eigenfaces Number : ", selectedfacesnum
        print "Imagename : ", imagename

        selectimg=imageops.XImage(imagename)
        inputfacepixels=selectimg._pixellist
        inputface=asfarray(inputfacepixels)
        pixlistmax=max(inputface)
        inputfacen=inputface/pixlistmax        
        inputface=inputfacen-self.bundle.avgvals
        usub=self.bundle.eigenfaces[:selectedfacesnum,:]
        input_wk=dot(usub,inputface.transpose()).transpose()        

        dist = ((self.weights-input_wk)**2).sum(axis=1)
        idx = argmin(dist)
        mindist=sqrt(dist[idx])
        result=""
        print "MinDist : ", mindist
        if mindist < thresholdvalue:
            #result = ""+str(idx)
            result = self.bundle.imglist[idx]
        '''
        if mindist <  1e-10:
            mindist = 0
        '''        
        return mindist,result,idx
        

    def saveArrayInDatabase(self,imagename, sampleNumber, Samplelimit):    
        global pictureData
        numpixels = 165
        fulldata = ""
        fulldataHex = ""
        selectimg=imageops.XImage(imagename)
        inputfacepixels=selectimg._pixellist
        inputface=asfarray(inputfacepixels)

        #Converting Image data into system Hex string data
        for j in range(numpixels):
 
            inputHexface = hex( inputface[j] ).rstrip("L").lstrip("0x")

            if( len(str(inputHexface)) == 0):
                fulldataHex += "00" + str(inputHexface)

            if( len(str(inputHexface)) == 1):
                fulldataHex += "0" + str(inputHexface)

            if( len(str(inputHexface)) == 2 ):
                fulldataHex += str(inputHexface)

            if( len(str(inputHexface)) > 2 ):
                fulldataHex += str(inputHexface)

        print "fulldataHex : ", fulldataHex
        print "length of data : ", len(fulldataHex)

        pictureData += fulldataHex

        print "Picture Data [ "+ str(sampleNumber) + " ] : " + str(inputface)
        print "Samplenumber [", sampleNumber, " ] "

        if( sampleNumber == Samplelimit ) : 
            senddata = "102" + "0000" + "00" + pictureData
            ser.write(senddata)
            print "Writing Data : ",senddata
            print "Length of Picture Data : ", len(pictureData)
            print "Length of Writing Data : ", len(senddata)
            pictureData= ""

        '''
        senddata = "102" + "0000" + "00" + fulldataHex
        ser.write(senddata)
        print "Writing Data : ",senddata
        '''

    def doCalculations(self,dir,selectednumeigenfaces): 

        self.createFaceBundle();
        #print "selected Number of Eigenfaces : ", selectednumeigenfaces 
        #print "Directory : ", dir
   
        egfaces=self.bundle.eigenfaces
        adjfaces=self.bundle.adjfaces
        self.weights=self.calculateWeights(egfaces,adjfaces,selectednumeigenfaces)
           
    
    def calculateWeights(self,eigenfaces,adjfaces,selectedfacesnum):  

        usub=eigenfaces[:selectedfacesnum,:]        
        wts=dot(usub,adjfaces.transpose()).transpose()  
        return wts           
            
    def createFaceBundle(self):
                 
        imgwdth = 15
        imght = 11
        numpixels = 165
        '''
        query = "select count(id) from test"
        cursor.execute(query)
	var = cursor.fetchone ()

        numimgs = int ( var[0] )
        '''
        query = "select max(serial) from test"
        cursor.execute(query)
	var = cursor.fetchone ()

        numimgs = int ( var[0] ) + 1

        #trying to create a 2d array ,each row holds pixvalues of a single image
        facemat=zeros((numimgs, numpixels))
        
        for i in range(numimgs):
            listdata = []
            pixarrayfloat = []
            fulldata = ""
            chardata = ""
            stringdata = ""

            # Selecting data  from  database
            query = "select * from test where serial like " + str(i)
            cursor.execute(query)
	    val = cursor.fetchall ()


            for s in val:
                k = s[0]
                stringdata = s[2]
            fulldata = stringdata
            datalength = len(fulldata)

        #***************************************************************************
            # Adding String item into listdata
            for n in range(len(fulldata)):
                chardata += fulldata[n]
                if(len(chardata) == 2):
                    listdata.append(chardata)
		    chardata = ""
 
            # Converting listdata to float list to calculate
            for m in listdata:
                if ( m != "\r\n" ) : 
                    hexdata = "0x"+str(m)
                    floatdata = int(hexdata, 16)
                    pixarrayfloat.append(float(floatdata))

            if(datalength > 10) : 
                pixarraymax=max(pixarrayfloat)
                pixarrayn = pixarrayfloat/pixarraymax                       
                facemat[i,:]=pixarrayn  
            '''
            pixarraymax=max(pixarrayfloat)
            pixarrayn = pixarrayfloat/pixarraymax                       
            facemat[i,:]=pixarrayn  
            '''

        #create average values ,one for each column(ie pixel)        
        avgvals=average(facemat,axis=0)      
   
          
        #substract avg val from each orig val to get adjusted faces(phi of T&P)     
        adjfaces=facemat-avgvals       
        adjfaces_tr=adjfaces.transpose()
        L=dot(adjfaces , adjfaces_tr)
        evals1,evects1=eigh(L)

        #to use svd ,comment out the previous line and uncomment the next
        #evects1,evals1,vt=svd(L,0)        
        reversedevalueorder=evals1.argsort()[::-1]
        evects=evects1[:,reversedevalueorder]               
        evals=sort(evals1)[::-1]                

        #rows in u are eigenfaces        
        u=dot(adjfaces_tr,evects)
        u=u.transpose()   
            
        #NORMALISE rows of u
        for i in range(numimgs):
            ui=u[i] 
            ui.shape=(imght,imgwdth)
            norm=trace(dot(ui.transpose(), ui))       
            u[i]=u[i]/norm    
         
        self.bundle=FaceBundle(imgwdth,imght,adjfaces,u,avgvals,evals)
    
