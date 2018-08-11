TRUE = 1
FALSE = 0
NL = '\n'   # New Line charachter
class CModel:
    # class contains information for the whole model
#   errorlist=('NO Errors') # start the list of located error messages
################################################################################# 
    def __init__(self,modelname):# class CModel:
        # modelname is the model name. or file prefix
        self.BDF=modelname+".dat"  # Bulk data file name
        self.F06=modelname+".f06"  # .F06 printed output file name
        self.Log=modelname+".log" # .log output log file name
        self.F04=modelname+".F04" # .F04 log file name
        self.errorlist = [] # list of located error numbers
        self.elementlist = [] # list of elements referenced in error messages
        self.nodelist = [] # list of nodes referenced in error messages
################################################################################# 
    def Count_F06_Strings(self,strfindme):# class CModel:
        # count the total number of errors in the files
        filename = self.F06
        print "Atempting to open file :"+filename
        F_F06=open(filename,'r')
        line=F_F06.readline()
        findcount=0
        linecount=0
        for line in F_F06:
            linecount=linecount+1
            if line.find(strfindme)>0:
                findcount=findcount+1
#               if line.find('5289')>0:
#                   print ProcessE5289()
#               print line
        print "string '" + strfindme + "' found = "+ str(findcount)+" time(s)"
        print "Number of lines read = "+ str(linecount)
        F_F06.close()# ensure file is closed before re-use
        return findcount
################################################################################# 
    def Count_Fatals(self):# class CModel:
        # count  the total number of Fatal error in the .F06 file
        NumberOfFatals = self.Count_F06_Strings('FATAL')
        return NumberOfFatals
################################################################################# 
    def Count_Warnings(self):# class CModel:
        # count  the total number of Warnings in the .F06 file
        NumberOfWarnings = self.Count_F06_Strings('WARNING')
        return NumberOfWarnings
################################################################################# 
#   Error Processing Functions
################################################################################# 
    def ProcessError316(self,F_F06):# class CModel:
        # Function to proces error 316
## *** USER FATAL MESSAGE 316 (IFPDRV)
##     ILLEGAL DATA ON BULK DATA ENTRY CQUAD4  
##     User information:
##     See Bulk Data entry description in Section 5 of the NX NASTRAN
##     Quick Reference Guide. If you are using the large field format make
##     sure the number of entries is even.
## CQUAD4     80970      11   82698   82361   82361   82420  
        # Read the next line to get to the Bulk data card tyoe with the problem.
        #extract the BulkData card type
        nextline=F_F06.next() # read the next line
        BulkCardType = nextline.split()[6]
        if BulkCardType=="CQUAD4" or BulkCardType=="CTRIA3":
            nextline=F_F06.next() # read the next line
            nextline=F_F06.next() # read the next line
            nextline=F_F06.next() # read the next line
            nextline=F_F06.next() # read the next line
            nextline=F_F06.next() # read the next line
            #extract the element number
            elemType = nextline.split()[0]
            elemid = nextline.split()[1]
            # Add the element to the list error related elements
            self.elementlist.append(elemid)
#           print "Grid ID " + str(nodeid) + " Associated with error no 350"
            errorflag = "Error 316 located - Element ID "+ elemid +" type "+elemType
        elif BulkCardType=="BSURF":
            errorflag = "Error 316 located - processing error in Bulk Data Type " + BulkCardType
        else:
            errorflag = "Error 316 located - Unable to process error in Bulk Data Type " + BulkCardType
        print errorflag
        return errorflag
################################################################################# 
    def ProcessError350(self,F_F06):# class CModel:
        # Function to proces error 350
## *** USER FATAL MESSAGE 350 (IFS350)
##     THE FOLLOWING GRID OR SCALAR POINTS ARE SPECIFIED MORE THAN ONCE ON THE BULK DATA ENTRY SHOWN BELOW:
##      82361
        nextline=F_F06.next() # read the next line
        nextline=F_F06.next() # read the next line
        #extract the grid number
        nodeid = nextline.split()[0]
###>    print "MPC or Rigid Link error for Node " + nodeid + " DOF " + dofid + " Error Number 5289"
        self.nodelist.append(nodeid)
#        print "Grid ID " + str(nodeid) + " Associated with error no 350"
        errorflag = "Error 350 located"
        return errorflag
################################################################################# 
    def ProcessError1250(self,F_F06):# class CModel:
        # Function to proces error 1250
## *** USER FATAL MESSAGE 1250 (BIOWRT)
##     STATUS =          112, FILX =    5, LOGNAME = SCR300  , NSBUF3 =     8192
##     FILE = f:/femapscratch/lowma053.T2724_36.SCR300
##     BLKNBR =       7843
##     ERROR MESSAGE IS --
##     There is not enough space on the disk.
##     BIOMSG: ERROR    923 HAS OCCURRED IN ROUTINE IONAST  , FILE INDEX =            5.
##     LOGICAL NAME IS SCR300  
##     FILENAME IS f:/femapscratch/lowma053.T2724_36.SCR300
        nextline=F_F06.next() # read the next line (STATUS line)
        nextline=F_F06.next() # read the next line (Filename)
        #extract the grid number
        filename = nextline.split()[2]
        print "File Read/Write Error - check disk space " + filename
        errorflag = "Error 1250 located"
        return errorflag
################################################################################# 
    def ProcessError5289(self,F_F06):# class CModel:
        # Function to proces error 5289
## *** USER FATAL MESSAGE 5289 (WRGMTD)
##     DEPENDENT DEGREE-OF-FREEDOM GRID ID =     56740 AND COMPONENT = 1 APPEARS ON MORE THAN ONE MPC OR RIGID ELEMENT ENTRY.
##     User information:
##     An MPC entry or rigid element entry lists the same dependent grid point more than once.
#        print "Calling function ProcessError5289()"
        nextline=F_F06.next() # read the next line
        #extract the grid number
#        print " -->" + nextline + "<--"
        nodeid = nextline.split()[5]
        dofid =  nextline.split()[9]
###>    print "MPC or Rigid Link error for Node " + nodeid + " DOF " + dofid + " Error Number 5289"
        self.nodelist.append(nodeid)
#        print "Grid ID " + str(nodeid) + " Associated with error no 5289"
        errorflag = "Error 5289 located"
        return errorflag
################################################################################# 
    def ProcessError4282(self,F_F06):# class CModel:
    #
    # TODO   TODO   TODO   TODO
    # NOTE: The elememt ID has a full stop at the end which needs to be removed.
    # TODO   TODO   TODO   TODO
    #
    # Function to proces error 4282
# *** USER FATAL MESSAGE 4282 (RBSRHD)
#     UNDEFINED GRID POINT      36592 RIGID ELEMENT       24
#     User information:
#     The rigid element references a grid point that does not exist
#     in the model, or is disjoint from the superelement being
#     processed.  Check the Bulk Data Section and the superelement
#     SEMAP table for the existence of the grid point referenced.
##        print "Calling function ProcessError4282()"
        nextline=F_F06.next() # read the next line
        #extract the grid number
#        print " -->" + nextline + "<--"
        nodeid =  nextline.split()[3]
        elemid = nextline.split()[6]
        print "UNDEFINED GRID POINT " +nodeid+ " FOR ELEMENT WITH ID = " + elemid + " Error Number 4282"
        self.elementlist.append(elemid)
#        print "Grid ID " + str(nodeid) + " Associated with error no 5289"
        errorflag = "Error 4282 located"
        return errorflag
################################################################################# 
    def ProcessError4288(self,F_F06):# class CModel:
    #
    #
    # Function to proces error 4288
# *** USER FATAL MESSAGE 4288 (EQD8D)
#     ILLEGAL GEOMETRY FOR QUAD8 ELEMENT WITH ID =     54295.  CODE PATH =    21
#     User information:
#     The code paths refer to the reason.  Reasons 1 through 5 mean
#     that the program was unable to find an element coordinate system.
#     Reasons 6 through 12 imply the program cannot find a local
#     corrdinate system at a Gauss point.  Reason 13 may be due to
#     a negative 12I/T3 (PSHELL).  Reason 14 is due to zero transverse
#     shear thickness (PSHELL).  Reason 21 occurs if the isoparametric
#     mapping is unreasonable, which can occur if the midside nodes
#     are too close to the corners.
##        print "Calling function ProcessError5289()"
        nextline=F_F06.next() # read the next line
        nextline=nextline.replace("."," ")
        #extract the grid number
#        print " -->" + nextline + "<--"
        elemid = nextline.split()[8]
        codepath =  nextline.split()[12]
        print "ILLEGAL GEOMETRY FOR QUAD8 ELEMENT WITH ID = " + elemid + " CODE PATH = " + codepath + " Error Number 4288"
        self.elementlist.append(elemid)
#        print "Grid ID " + str(nodeid) + " Associated with error no 5289"
        errorflag = "Error 4288 located"
        return errorflag
################################################################################# 
    def ProcessError4298(self,F_F06):# class CModel:
    #
    #
    # Function to proces error 4298
## *** USER FATAL MESSAGE 4298 (EQD4D)
##     A CORNER POINT MEMBRANE THICKNESS HAS NOT BEEN SPECIFIED FOR ELEMENT WITH ID =       622
##     AND THERE IS NO DEFAULT VALUE ON THE ASSOCIATED PROPERTY CARD.
##     User information:
##        print "Calling function ProcessError5289()"
        nextline=F_F06.next() # read the next line
        nextline=nextline.replace("."," ")
        #extract the grid number
#        print " -->" + nextline + "<--"
        elemid = nextline.split()[14]
        print "A CORNER POINT MEMBRANE THICKNESS HAS NOT BEEN SPECIFIED FOR ELEMENT WITH ID = " + elemid + " Error Number 4288"
        self.elementlist.append(elemid)
#        print "Grid ID " + str(nodeid) + " Associated with error no 5289"
        errorflag = "Error 4288 located"
        return errorflag
################################################################################# 
    def ProcessError4306(self,F_F06):# class CModel
        errorID=4306
# *** USER FATAL MESSAGE 4306 (ETR6D)
#     DEGENERATE GEOMETRY OR INADEQUATE MATERIAL
#     DATA SPECIFIED FOR TRIA6 ELEMENT WITH ID =     56571    REASON NUMBER = 28
#     User iformation:
#     See UFM 4288 for an explanation of reason numbers, except
#     that Reason 28 corresponds to CODE 21.
        nextline=F_F06.next() # read the next line - no useful data on this line
        nextline=F_F06.next() # read the next line
        #extract the grid number
#        print " -->" + nextline + "<--"
        elemid = nextline.split()[8]
        codepath =  nextline.split()[12]
        print "DEFENERATE GEOMETRY OR INADEUATE MATERIAL DATA ELEMENT WITH ID = " + elemid + " CODE PATH = " + codepath + " Error Number 4306"
        self.elementlist.append(elemid)
#        print "Grid ID " + str(nodeid) + " Associated with error no 5289"
        errorflag = "Error 4306 located"
        return errorflag
################################################################################# 
    def ProcessMessage2101(self,F_F06,errorID):# class CModel:
#'    errorID=2101
    # Function to proces message 2101
# *** USER FATAL MESSAGE 2101 (GP4)
#     GRID POINT         10 COMPONENT  1 ILLEGALLY DEFINED IN SETS   UM   US   
##        print "Calling function ProcessMessage2101()"
        nextline=F_F06.next() # read the next line
        #extract the grid number
#        print " -->" + nextline + "<--"
        nodeid = nextline.split()[2]
        dofid = nextline.split()[4]
        print "NODE WITH ID = " + nodeid + " DOF " + dofid + " Error Number 2101"
        self.nodelist.append(nodeid)
#        print "Grid ID " + str(nodeid) + " Associated with error no 5289"
        errorflag = "Error 2101 located"
        return errorflag
#################################################################################   
    def ProcessMessage4551(self,F_F06):# class CModel:
        errorID=4551
    # Function to proces message 4551
# *** USER FATAL MESSAGE 4551 (NCONVG)
#     *** STOPPED PROBLEM DUE TO FAILED CONVERGENCE
#     User information:
#     A solution is not possible.  Review NLPARM requests and modify
#     to select a better solution approach.
##        print "Calling function ProcessError4551()"
        print "Message 4551 A solution is not possible.  Review NLPARM requests and modify."
        errorflag = "Error 4551 located"
        return errorflag
################################################################################# 
    def ProcessError4558(self,F_F06):# class CModel:
        errorID=4558
    #
    # Function to proces error 4558
## *** USER FATAL MESSAGE 4558 (ETR3D)
##     INAPPROPRIATE GEOMETRY OR INCORRECT MATERIAL DATA
##     SPECIFIED FOR ELEMENT WITH ID =     91518.  SUBROUTINE REASON IS NUMBER   2.
##     User information:
#       Reason codes are;
#       1,2,3,4,5,16    inappropriate TRIA3 Geometry
#       6,7,13,14,15    MID2 Material G-3X3 matrix insifficient, material ID = xxx
#       8               Zero moment of inertia computed
#       9,10            MID3 Material -G-2x2 Matrix Insufficient Material ID = xxx
#       12              Singluar Transverse Shear Matrix
##
##        print "Calling function ProcessError5289()"
        nextline=F_F06.next() # read the next line
        nextline=F_F06.next() # read the next line
        nextline=nextline.replace("."," ")
        print "Post . strip line is \n"+nextline
        #extract the grid number
#        print " -->" + nextline + "<--"
        elemid = nextline.split()[6]
        reasoncode =  int(nextline.split()[11])
        print "ILLEGAL GEOMETRY FOR QUAD8 ELEMENT WITH ID = " + elemid + " REASON CODE PATH = " + str(reasoncode) + " Error Number 4558"
        if reasoncode <=5 or reasoncode == 16:
            print"ERROR = inappropriate TRIA3 Geometry"
        elif reasoncode ==6 or reasoncode == 7 or reasoncode == 13 or reasoncode == 14 or reasoncode == 15:
            print "ERROR = MID2 Material G-3X3 matrix insifficient, material ID = " + materialID
            print nextline
        elif reasoncode ==8 :
            print "ERROR = Zero moment of inertia computed"
        elif reasoncode ==9 or reasoncode == 10:
            print"ERROR = MID3 Material -G-2x2 Matrix Insufficient"
            print nextline
        elif reasoncode ==12 :
            print "ERROR = Singluar Transverse Shear Matrix"
        else:
            print "ERROR-->Unrecognised reason code " + str(reasoncode) + "Reffer to FEMAP documentation.<--"
        self.elementlist.append(elemid)
#        print "Grid ID " + str(nodeid) + " Associated with error no 5289"
        errorflag = "Error 4558 located"
        return errorflag
#################################################################################   
    def ProcessMessage5276(self,F_F06):# class CModel:
        errorID=5276
    # Function to proces message 5276
# *** USER WARNING MESSAGE 5276 (EQD8D)
#     ELEMENT      53361 HAS TOO MUCH CURVATURE AND MAY YIELD POOR ANSWERS.
#     User information:
#     The element listed has an angle greater than 30 degrees between normals
#     to some corner grid points.
#     This can lead to excessively low stiffness.
#     Use a finer mesh size to reduce the angles between the normals.
##        print "Calling function ProcessError5289()"
        nextline=F_F06.next() # read the next line
        #extract the grid number
#        print " -->" + nextline + "<--"
        elemid = nextline.split()[2]
        print "Message 5276 Excessive curvature for ELEMENT ID = " + elemid
        self.elementlist.append(elemid)
        errorflag = "Warning 5276 located"
        return errorflag
################################################################################# 
    def ProcessMessage9002(self,F_F06):# class CModel:
        errorID=9002
    # Function to proces message 9002
# ^^^ USER   FATAL   MESSAGE 9002 (IFPS)  
# ^^^ ERROR(S) ENCOUNTERED IN THE    MAIN BULK DATA SECTION   
# ^^^ SEE MESSAGES ABOVE. ERROR ENCOUNTERED IN MODULE    IFP,                                     
##        print "Calling function ProcessError9002()"
        print "Message 9002 FATAL Errors located - see previous messages"
        errorflag = "Error 9002 located"
        return errorflag
################################################################################# 
    def ProcessFatalErrors(self):# class CModel:
        # This process re-reads the file, adding all the errors and associated nodes
        # and elements to lists, then creates the neutral file.
        # count the total number of errors in the files
        filename = self.F06
        strlist = []
        cantprocesslist = [] # list or errors not currently processed
        F_F06=open(filename,'r')
#       line=F _F06.readline()
        findcount = 0
        linecount = 0
        #####
        ##### The for .. in method needs to be changed to allow functions to continue to read the file.
        ##### perhaps I could read the complete file, then pass only the following say, x lines for 
        ##### further processing, depending on how many are reqired for each error message.
        #####
        ####        for line in F_F06:
        line = F_F06.readline()
        while len(line) > 0:
            linecount = linecount + 1
            if line.find('FATAL') > 0:
                findcount = findcount + 1
                try:
##                    print "-->Just before error message<--"
                    if len(line.split()) >= 4:
                        messagenumber = int( line.split()[4] )# extract the error number.
                    else:
                        print "can't extract the error number from following line;"
                        print line
                except ValueError:
#                   print"ERROR LINE FOLLOWS\n"+ line
                    if line.find('ONE OR MORE FATAL ERRORS') > 0:
                        print"Last error located"
                        break
#                        exit(0) # End of the file
                    exit(1)
                self.errorlist.append(messagenumber)
                ########################################
                #
                # Process the known errors
                #
                ########################################
                if messagenumber == 316:
                    print"Processing Error 316"
                    self.ProcessError316(F_F06)

                elif messagenumber == 350:
                    print"Processing Error 350"
                    self.ProcessError350(F_F06)
                    
                elif messagenumber == 1250:
                    print"Processing Error 1250"
                    self.ProcessError1250(F_F06)
                    
                elif messagenumber == 2101:
                    self.ProcessMessage2101(F_F06,messagenumber)
                    
                elif messagenumber == 5289:
                    self.ProcessError5289(F_F06)
                    
                elif messagenumber == 4282:
                    self.ProcessError4282(F_F06)
                    
                elif messagenumber == 4288:
                    self.ProcessError4288(F_F06)
                    
                elif messagenumber == 4298:
                    self.ProcessError4298(F_F06)
                    
                elif messagenumber == 4306:
                    self.ProcessError4306(F_F06)
                    
                elif messagenumber == 4551:
                    self.ProcessMessage4551(F_F06)
                    
                elif messagenumber == 4558:
                    self.ProcessError4558(F_F06)
                    
                elif messagenumber == 9002:
                    self.ProcessMessage9002(F_F06)
                    
                else:
                    print "Unable to process FATAL Message number " + str(messagenumber)
                    cantprocesslist.append(messagenumber)
            try:
                line = F_F06.next() # read the next line
            except StopIteration:
                print "Process Fatal Error: EOF reached"
                break
        uniqueerrorset = set(self.errorlist)# placing the list in a set reduces the list to a set of unique numbers
        print "Number of lines read = "+ str(linecount)
        print "Number of errors in the list = " + str(len(self.errorlist)) + " Number of unique errors = " + str(len(uniqueerrorset))
        print "The located error numbers are;"
        loop = 0
        for x in uniqueerrorset:
            loop = loop + 1
            print "Error type " + str(loop) + " is " + str(x)
        if len(cantprocesslist) > 0:
            print "Currently unable to process the following errors"
            print set(cantprocesslist)
        else:
            print "\nAll FATAL errors processed."
        F_F06.close()# ensure file is closed before re-use
        return findcount
################################################################################# 
    def ProcessWarnings(self):# class CModel:
        # This process re-reads the file, adding all the nodes and elements associated
        # with serious warnings to the entity lists.
        filename = self.F06
        strlist = []
        F_F06=open(filename,'r')
#       line=F _F06.readline()
        findcount = 0
        linecount = 0
        #####
        ##### The for .. in method needs to be changed to allow functions to continue to read the file.
        ##### perhaps I could read the complete file, then pass only the following say, x lines for 
        ##### further processing, depending on how many are reqired for each error message.
        #####
        ####        for line in F_F06:
        line = F_F06.readline()
        while len(line) > 0:
            linecount = linecount + 1
            if line.find('WARNING') > 0:
                findcount = findcount + 1
                try:
                    messagenumber = int( line.split()[4] )# extract the warning number.
                except (ValueError, IndexError):
                    print"Warning LINE FOLLOWS\n"+ line
                    if line.find('WARNING MESSAGE IS') > 0:
                        print F_F06.next()
                    break
#                        exit(0) # End of the file
                    exit(1)
                self.errorlist.append(messagenumber)
                ########################################
                #
                # Process the known warnings
                # (Not all warning messages are associated with nodes or elements.)
                #
                ########################################
                if messagenumber == 5289:
                    self.ProcessMessage5276(F_F06)
                else:
                    print "Unable to process WARNING message number " + str(messagenumber)
                    print"Line = " + NL + line
            try:
                line = F_F06.next() # read the next line
            except StopIteration:
                print "Process Fatal Error: EOF reached"
                break
        uniqueerrorset = set(self.errorlist)# placing the list in a set reduces the list to a set of unique numbers
        print "Number of lines read = "+ str(linecount)
        print "Number of errors in the list = " + str(len(self.errorlist)) + " Number of unique errors = " + str(len(uniqueerrorset))
        print "The located error numbers are;"
        loop = 0
        for x in uniqueerrorset:
            loop = loop + 1
            print "Error type " + str(loop) + " is " + str(x)
        F_F06.close()# ensure file is closed before re-use
        return findcount
################################################################################# 
### end of class CModel
################################################################################# 
