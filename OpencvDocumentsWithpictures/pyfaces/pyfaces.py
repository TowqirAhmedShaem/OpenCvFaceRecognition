import  sys
import time
import serial
from string import split
from os.path import basename
import eigenfaces
import MySQLdb

#Serial Parameters
ser = serial.Serial()
ser.baudrate = 115200
#ser.port = '/dev/ttyACM1'
ser.port = '/dev/ttyACM0'
#ser.port = '/dev/ttyUSB0'
ser.open()

# *********Data segment******** #

# Input Command
recogMode                 =  "0010000"
registraionMode        =  "0020000"
deleteData                 =  "0030000"
deleteAllData             =  "0040000"
readData                    =  "0050000"
writeData                   =  "0070000"
templateCount           =  "0080000"
setSecureLevel           = "0090000"
getSecureLevel          = "0100000"
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

# Connecting with database 
db=MySQLdb.connect(host="localhost",user="root",passwd="rumy",db="opencv")
cursor=db.cursor()

# Variable
global previousID
previousID = "Null"


# Flag
global FLAG 
global recogFlag
global blurValue
global SecurityLevel
global checKFirstTimeSecurity

FLAG = False
recogFlag = False
checKFirstTimeSecurity = True
blurValue = 700
SecurityLevel = 3
Facet = eigenfaces.FaceRec()

class PyFaces:
    def __init__(self,command):
 
        self.command=command      
        inputcommand = ""
        commandnumber = ""
        commandid = ""

        inputcommand = str(self.command[0])
        print "InputCommand : "+ inputcommand


        if ( inputcommand == "0" ):

            print "working for input command"
            commandnumber = str( self.command[1] + self.command[2] )
            print "CommandNumber : " + commandnumber
            commandid = str( self.command[3] + self.command[4] + self.command[5] + self.command[6])
            print "CommandId : " + commandid

            self.checkForCorrespodingCommandNumber(commandnumber, commandid, command)

        else:
            # inputError = 100000000
            ser.write( inputError )
            ser.flush()
            print "Writing data : " +  inputError

  
        #self.facet= eigenfaces.FaceRec()
        #self.egfnum=self.set_selected_eigenfaces_count(self.egfnum,extn)

        #self.facet.checkCache(self.imgsdir,extn,self.imgnamelist,self.egfnum,self.threshold)
        #self.facet.doCalculations(self.imgsdir,self.imgnamelist,self.egfnum)
        #mindist,matchfile,idx=self.facet.findmatchingimage(self.testimg,self.egfnum,self.threshold)

        #if mindist < 1e-10:
            #mindist=0
        #if not matchfile:
            #print "NOMATCH! try higher threshold"
        #else:
	    # print "******************************************************************"
	    #print
            #print
	    #print "Images : "+ str(self.testimg)
            #print "Matches :"+matchfile # +" dist :"+str(mindist)
	    # print "******************************************************************"
            #print "Dist Value : "+str(mindist)
	#print "Pyfaces __init__ ends ..."

    def checkForCorrespodingCommandNumber(self, commandNumber, commandId, command):
        
        if   ( commandNumber == "01" ):
            self.recogMode( commandId )

        elif ( commandNumber == "02" ):
            self.registrationMode( commandId )

        elif ( commandNumber == "03" ):
            self.deleteData( commandId )

        elif ( commandNumber == "04" ):
            self.deleteAllData( commandId )

        elif ( commandNumber == "05" ):
            self.readData( commandId )

        elif ( commandNumber == "07" ):
            self.writeData( commandId , command )

        elif ( commandNumber == "08" ):
            self.templateCount( commandId )

        elif ( commandNumber == "09" ):
            self.setSecureLevel( commandId )

        elif ( commandNumber == "10" ):
            self.getSecureLevel( commandId )

        else :
            # commandError = "100000011"
            ser.write ( commandError );
            print "Writing data : " +  commandError



   # All FUnctions for correspoding CommandNumber
    def registrationMode(self, commandID):

        #regModeError =  102000011
        Flag = False
        if ( commandID == "0000" ):
            Flag = True
        else :
            ser.write (regModeError)
            Flag = False
   
        PYFACES = PyFacesForGeneralPurpose()
        checker = PYFACES.setRegistrationModeForThread( Flag )
        


    def templateCount(self, commandID):

        # templateModeError =  "108000011"
        if ( commandID == "0000" ) :
            query = "select count(id) from test"
            cursor.execute(query)
	    var = cursor.fetchone ()
            print var[0]
            VAR = str( var[0] )

            if( len(VAR) < 2):
                VAR = "000" + VAR
            if( len(VAR) < 3 and len(VAR) > 1 ):
                VAR = "00" + VAR
            if( len(VAR) < 4 and len(VAR) > 2 ):
                VAR = "0" + VAR
            senddata = "108"+ VAR + "00"
            ser.write(senddata)
            print "Writing data : " +  senddata

        else :
            ser.write (templateModeError)
            print "Writing data : " +  templateModeError


    def deleteData(self, commandID):

        # deleteModeError   =  "103000011"
        query = "select count(id) from test"
        cursor.execute(query)
	var = cursor.fetchone ()        
        if( int(commandID) >= var[0] or int(commandID) < 0) :
            ser.write(deleteModeError)
            print "Writing data : " +  deleteModeError

        else :
            query = "delete from test where id like "+commandID
            cursor.execute(query)
            db.commit()
            senddata = "103" + commandID + "00"
            ser.write (senddata)
            print "Writing data : " +  senddata


    def deleteAllData(self, commandID):

        # deleteallModeError=  "104000011"
        if ( commandID == "0000" ) :
            query = "delete from test"
            cursor.execute(query)
            db.commit()
            senddata = "104" + commandID + "00"
            print "Writing data : " +  senddata

        else :
            ser.write( deleteallModeError )
            print "Writing data : " + deleteallModeError


    def readData(self, commandID) :

        #readModeError     =  "105000011"
        query = "select count(id) from test"
        cursor.execute(query)
	var = cursor.fetchone ()    
    
        if( int(commandID) >= var[0] or int(commandID) < 0) :
            ser.write(readModeError)
            print "Writing data : " + readModeError

        else :
            stringdata = ""
            query = "select * from test where id like " + commandID
            cursor.execute(query)
            var = cursor.fetchall ()

            for s in var:
                k = s[0]
                serialx = s[1]
                stringdata += s[2] + "S"
            senddata = "105" + commandID + "00" + stringdata
            ser.write(senddata)
            print "Writing data : " + senddata


    def writeData(self, commandID, command ):
        print "Write Data Mode Starts"
        data = ""
        # writeModeError    =  "107000011"

        if ( commandID == "0000" ):
            

            # Calculating Present Serial No  to insert into database
            query = "select count(serial) from test"
            cursor.execute(query)
	    var = cursor.fetchone ()
            SerialVar = int ( var[0] ) 
            print 'SerialVar : ', SerialVar

           #Calculating Present id from database
            query = "select  max(id) from test"
            cursor.execute(query)
	    var = cursor.fetchone ()
            print "var : ", var
            if(SerialVar == 0):
                IDVar = 1
            else : 
                IDVar =  int(var[0] ) 
                IDVar += 1
            print 'IDVar : ', IDVar

            length = len(command)
            print "Length of Command : " + str(length)
            stringdata = command[ 7: ]
            picturedata1 = stringdata[ : 330]
            picturedata2 = stringdata[330: 660]
            picturedata3 = stringdata[660: 990]
            picturedata4 = stringdata[990: 1320]
           
            print "Receive Data : " + stringdata;
            print "Length of full combined picture : " , len ( stringdata ) 
            print "Length of picture1 : " , len ( picturedata1 ) 
            print "Length of picture2 : " , len ( picturedata2 ) 
            print "Length of picture3 : " , len ( picturedata3 ) 
            print "Length of picture4 : " , len ( picturedata4 )

     
            cursor.execute("INSERT INTO test (id,serial,data) values (%s,%s,%s)",(IDVar , SerialVar , picturedata1))
            print "Inserting : ", picturedata1
            db.commit()   
            SerialVar += 1

            cursor.execute("INSERT INTO test (id,serial,data) values (%s,%s,%s)",(IDVar , SerialVar , picturedata2))
            print "Inserting : ", picturedata2
            db.commit()   
            SerialVar += 1

            cursor.execute("INSERT INTO test (id,serial,data) values (%s,%s,%s)",(IDVar , SerialVar , picturedata3))
            print "Inserting : ", picturedata3
            db.commit()   
            SerialVar += 1

            cursor.execute("INSERT INTO test (id,serial,data) values (%s,%s,%s)",(IDVar , SerialVar , picturedata4))
            print "Inserting : ", picturedata4
            db.commit()   
            SerialVar += 1

            '''
            # Picture Data Parsing 
            for m in stringdata:
                
                if ( m == "\r\n" ) : 
                    print " Carriage Return Found"
           
                if ( m == "S" ) : 
                    cursor.execute("INSERT INTO test (id,serial,data) values (%s,%s,%s)",(IDVar , SerialVar , data))
                    print "Inserting : ", data
                    db.commit()   
                    SerialVar += 1
                    data = ""

                else :
                    data +=m

            '''


            VAR = str(IDVar)

            if( len(VAR) < 2):
                VAR = "000" + VAR
            if( len(VAR) < 3 and len(VAR) > 1 ):
                VAR = "00" + VAR
            if( len(VAR) < 4 and len(VAR) > 2 ):
                VAR = "0" + VAR
            senddata = "107" + VAR + "00"
            ser.write(senddata)
            print "Writing data : ", senddata

        else :
            ser.write(writeModeError)
            print "Writing data : " + writeModeError

            ''''
            cursor.execute("INSERT INTO test (id,data) values (%s,%s)",(var[0], stringdata))
            db.commit()

            VAR = str(var[0])

            if( len(VAR) < 2):
                VAR = "000" + VAR
            if( len(VAR) < 3 and len(VAR) > 1 ):
                VAR = "00" + VAR
            if( len(VAR) < 4 and len(VAR) > 2 ):
                VAR = "0" + VAR
            senddata = "107" + VAR + "00"
            ser.write(senddata)
            print "Writing data : ", senddata

        else :
            ser.write(writeModeError)
            print "Writing data : " + writeModeError
        '''

    def setSecureLevel(self, commandID) :
        PYFACES = PyFacesForGeneralPurpose()

        if ( commandID == "0001" ):
            PYFACES.setSecureLevel( 1 )
        elif ( commandID == "0002" ):
            PYFACES.setSecureLevel( 2 )
        elif ( commandID == "0003" ):
            PYFACES.setSecureLevel( 3 )
        elif ( commandID == "0004" ):
            PYFACES.setSecureLevel( 4 )
        elif ( commandID == "0005" ):
            PYFACES.setSecureLevel( 5 )
        else :
            ser.write(securityModeError)
            ser.flush()
            print 'Writing Data : ', securityModeError

    def getSecureLevel(self, commandID) :
        PYFACES = PyFacesForGeneralPurpose()

        if ( commandID == "0000" ):
            Level, blurvalue = PYFACES.getSecurityLevel(  )
            StrLevel = "000"+ str(Level)
            senddata = "110" + StrLevel + "00"
            ser.write(senddata)
            ser.flush()
            print 'Writing Data : ', senddata
        else :
            ser.write(securityModeError)
            ser.flush()
            print 'Writing Data : ', securityModeError

    def recogMode(self, commandID) :

        # recogModeError    =  101000011
        recogFlag = False

        if ( commandID == "0000" ):
            query = "select count(id) from test"
            cursor.execute(query)
	    var = cursor.fetchone ()
            if( var[0]  > 0) :
                recogFlag = True
            else :          
                ser.write (recogModeError)
                print "writing data : ", recogModeError

        else :          
            ser.write (recogModeError)
            recogFlag = False

        PYFACES = PyFacesForGeneralPurpose()
        checker = PYFACES.setRecognizeModeForThread( recogFlag )
            
            
    def set_selected_eigenfaces_count(self,selected_eigenfaces_count,ext):        
       
        numimgs = 69
        if(selected_eigenfaces_count >= numimgs  or selected_eigenfaces_count == 0):
            selected_eigenfaces_count=numimgs/2    
        return selected_eigenfaces_count


class PyFacesForGeneralPurpose(object):

    # Registartion Mode
    def setRegistrationModeForThread(self, flag):
        print "setRegistration Mode Starts"
        global FLAG
	FLAG = flag
        print "Flag on setRegistration : "
        print FLAG
       
    def getRegistrationModeForThread(self):
        print "getRegistration Mode Starts"
        global FLAG
        return FLAG

    def saveArrayDataForImage(self, ImageFile, sampleNumber, Samplelimit ):
        print "Imagefile in SaveArrayData : " , ImageFile
        Facet.saveArrayInDatabase(ImageFile, sampleNumber, Samplelimit)



    # Recognize Mode
    def setRecognizeModeForThread(self, flag):
        print "setRecognizeModeForThread  Starts"
        global recogFlag
	recogFlag = flag
        print "Flag on setRecognizeModeForThread : "
        print recogFlag

    def getRecognizeModeForThread( self ):
        print "getRecognize Mode Starts"
        global recogFlag
        return recogFlag


    def findMatchingImageForThis( setSecureLevelself , countingTimeStart) :  
        global previousID
        idx = ""
        serialx = ""
        datax = ""

        #imgsdir = "/home/pi/FaceAccessControl/OpencvDocuments/dataStore/"
        #testimg = "/home/pi/FaceAccessControl/OpencvDocuments/dataStore/TestImage.jpg"

	testimg=  '/home/pi/gitlab/FaceAccessControl/OpencvDocumentsWithpictures/test/TestImage.jpg'
	imgsdir = '/home/pi/gitlab/FaceAccessControl/OpencvDocumentsWithpictures/database'

        ext = "gif"

        query = "select count(serial) from test"
        cursor.execute(query)
	var = cursor.fetchone ()

        egfnum = var[0]
        threshold = 3

        query = "select count(serial) from test"
        cursor.execute(query)
	var = cursor.fetchone ()

        if ( var[0] > 0) :

            imglist = Facet.parsefolder(imgsdir, ext)
            Facet.doCalculations(imgsdir, egfnum, imglist, ext)
            Mindist,Matchfile,serial = Facet.findmatchingimage(testimg, egfnum, threshold)
            
            if Mindist < 1e-10:
                Mindist = 0

            countingTimeend = time.time()
            totalTime = countingTimeend - countingTimeStart

            # Selecting data  from  database
            query = "select * from test where serial like " + str(serial)
            cursor.execute(query)
	    val = cursor.fetchall ()
            print 'val : ', val

            for s in val:
                idx = s[0]
                serialx = s[1]
                datax = s[2]

            IDX = str(idx)

            if( len(IDX) < 2):
                IDX = "000" + IDX
            if( len(IDX) < 3 and len(IDX) > 1 ):
                IDX = "00" + IDX
            if( len(IDX) < 4 and len(IDX) > 2 ):
                IDX = "0" + IDX

            print "*************************"
            print "Matched With : " + str(IDX)
            print "*************************"
            print 'Matched File : '
            print Matchfile
            print "Mindist : ", Mindist 
            print 'Original Serial : ', serial, '  Database Serial :  ', serialx

            print "Total Ti me : ", totalTime
            print "Previous Id : ", previousID, " ID : " , IDX

            if ( totalTime < 2 ) :
                print "Total Ti me : ", totalTime
                print "Previous Id : ", previousID, " ID : " , IDX
                if ( previousID != IDX ) :

                    countingTimeStart = time.time()
                    previousID =  IDX       
                    senddata = "101" + str(IDX) + "00"
                    ser.write(senddata)
                    ser.flush()

                    print "Writing data for new data : " + senddata

            else :
                countingTimeStart = time.time()
                previousID =  IDX     
                senddata = "101" + str(IDX) + "00"
                ser.write(senddata)
                ser.flush()
                print "Writing data : " + senddata
                print "Start time : ", countingTimeStart, "End time : ", countingTimeend, "Total time : ", totalTime


    def templateCount(self):
        print "Counting last id from database"
        # Connecting with database 
        db=MySQLdb.connect(host="localhost",user="root",passwd="rumy",db="opencv")
        cursor=db.cursor()

        query = "select count(id) from test"
        cursor.execute(query)
	var = cursor.fetchone ()
        return var[0]

    def setSecureLevel(self, level):

        global blurValue
        global SecurityLevel
        SecurityLevel = level

        if(SecurityLevel == 1):
            blurValue = 300
        if(SecurityLevel == 2):
            blurValue = 500
        if(SecurityLevel == 3):
            blurValue = 700
        if(SecurityLevel == 4):
            blurValue = 1200
        if(SecurityLevel == 5):
            blurValue = 1500
        cursor.execute("delete from security")
        db.commit()  
        cursor.execute("INSERT INTO security (level,blurvalue) values (%s,%s)",(SecurityLevel, blurValue))
        db.commit()
        checKFirstTimeSecurity = True

    def getSecurityLevel(self):
        global SecurityLevel
        global blurValue
        global checKFirstTimeSecurity
 
        if( checKFirstTimeSecurity ):
            print "Getting security data from database"
            # Connecting with database 
            db=MySQLdb.connect(host="localhost",user="root",passwd="rumy",db="opencv")
            cursor=db.cursor()
            query = "select * from security"
            cursor.execute(query)
            var = cursor.fetchall ()

            for s in var:
                SecurityLevel = s[0]
                blurValue = s[1]
            checKFirstTimeSecurity = False

        return SecurityLevel, blurValue




