import sys
import os
if len(sys.argv) == 3:
#  sys.argv[0] is the executable name, input arguments start at sys.argv[1].
#  sys.argv[1] is the file name prefix (excluding the .F06)
#  sys.argv[2] is the file directory	[[ NOTE: NO SPACES are permitted in the file path supplied ]]
    prefix = sys.argv[1]#NOTE: argument indexing starts at ZERO
	#
    print "\n====================================================================================="
    print "\n\n START OF NxF02 Analysis\n"
    print "supplied input prefix = " + prefix
    print "File directory = " + str(sys.argv[2])
    print "\n====================================================================================="
else:
    print "\n====================================================================================="
    print "                incorrect argumentlist"
    print "sys.argv[0] = " + str(sys.argv[0])
    print "sys.argv[1] = " + str(sys.argv[1])
    print "len(sys.argv) = " + str(len(sys.argv))+"\n"
    print "sys.argv = " + str(sys.argv)+"\n"
    print "\n          Input filename or file path must NOT contain spaces.\n"
    print "                 T E R M I N A T I N G."
    print "\n====================================================================================="
    exit(1)
#    prefix = 'D:/Carlton/SoftwareDevelopment/NxF06/v7g1_000' ##<< Office PC
#    print "len(sys.argv) = " + str(len(sys.argv))
#    print "PREFIX = " + prefix
#    print sys.argv
#
#   Error and WARNING routines are in Cmodel.py
#
#
#prefix = 'H:/Carlton/NxF06/wingb000'                       ##<< Laptop
#prefix = 'H:/Carlton/NxF06/Proce000'                      ##<< Laptop
#prefix = 'C:/Documents and Settings/carlton/My Documents/QinetiQ/Nastran.F06 Files/wingb000'##<< XP home office
#prefix = 'C:/Documents and Settings/carlton/My Documents/QinetiQ/NxF06/wingb000'##<< XP home office
#
# In Crimson Editor run using cntl+4 at work, cntl+1 on Aspire Laptop
#
################################################################################
#                        NxF06.py
################################################################################
# NOTES:-
# Since the User Information will be the same for each FATAL message, it makes
# sense to store this informtation only once. The message section is specific to
# each error occurance, since this contains the useful information such as the
# relevant node or element ID.
# One option would be to store all the data in an external file, this means a lot
# of work up front.
# we can use the CError to store a dictionary of user unformation as and when it
# is found, this way only the relevant user information is return to the user.
#####
# What the user needs is the data elevant to the paticular file being looked at.
# Hence aft each .F06 is analysed, the following information should be given to
# the user;
# 1. Number of different errors located.
# 2. list of all errors located, along with the User Information message for each
# message.
# 3. Recommendations for solving the problem.
# 4. The name of the neutral file created, and the following;
# all nodes & elements listed in error messages.
# The property IDs, material IDs, and associated names (if possible) relating to
# the elements referenced in the error messages.
#####
# How can this be achieved ?
# When a fatal error is located, add the error number to an error number list.
# Extract the relevant node/element ID and add to the node/element list.
#####
# program works as follows;
# first scan the .F06 file;
# No FATAL erors - Exit
# 1. FATAL errors located - rescan, collecting error numbers, and associated
#    node and elememt IDs
# 2. Write the neutral file containing the relevant node & element IDs.
################################################################################
#   Classes
#   CNeutralFile(), CModel(), CNode(), CElement(), CNeutralFile(), CGroup
################################################################################
################################################################################
#
# Attempt to set the directory path correctly
os.chdir(sys.argv[2])
TRUE = 1
FALSE = 0
NL = '\n'   # New LIne charachter
BT = '  -1\n' # Neutral file block terminator
from CNeutralFile   import *  #read, write and process neutral files
from CNeutralGroup  import *  #Read, write and process neutral file groups
from CModel         import *  #CModel contains the saved F06 file information
    #
    #Functions required;
    #1. Open NeutralFile - creates the file, calls NeutralFileHeader
    #2. if len(elementlist) > 0 NeutralFileElements(elementlist)
    #3. if len(nodelist) > 0
#################################################################################
#################################################################################
class CNode():
    # class containing  nodal data
    # contents to reflect datablock 403
    def __init__(self):# class CNode():
        self.opcsys # output coordinate system
        Self.xcord = 0.0 # nodes X coordinate
        self.ycord = 0.0  # nodes Y coordinate $$$$
        self.zcord = 0.0  # nodes Z coordinate
#################################################################################
#################################################################################
class CElement():
    # class containing  element data
    # contents to reflect data block 404
    def __init__(self):# class CElement():
        self.pid=0 # element property ID
        self.mid=0 # element material ID
        self.numnodes=0  # number of element nodes
        nodelist=[] # list of element nodes
#################################################################################
#################################################################################
class CNeutralFileOBSOLETE():
    #read, write and process neutral files
    def __init__(self,filename):# class CNeutralFile():
        self.filename=filename
    def read(self):# class CNeutralFile():
        # read a neutral file
        Lines=openfile(filename)
        return lines

    def write(self,grouplist):# class CNeutralFile():
        # write a neutral file consisting of the supplied list of groups
        #Write file
    #   return "OK" or "ERRROR"
        return "OK"
#################################################################################
#
class CError:
#   # contains Error Number, Description, Solution and possibly the functions required to process the error
    def __init__(self,errornumber,message,userinfo):# class CError:
        self.error_num = erornumber
        self.descriptor = message
        self.info = userinfo
#################################################################################
#################################################################################
def main(prefix):
    #prefix=raw_input('Enter model name prefix -->' )
    # Create the model object
    mymodel=CModel(prefix)
    neutralfilename = prefix + ".neu"
    strversion = '10.2' # current version of FEMAP
    createneutralfile = FALSE # set to TRUE when a neutral file has been generated
    headerwritten = FALSE

    print "F06 file name is " + mymodel.F06
    print "BDF file name is " + mymodel.BDF
    # Count Warnings
    warnings = mymodel.Count_Warnings()
    if warnings  > 0:
        print " Total Warnings Found = " + str(warnings)
        seriouswarnings = mymodel.ProcessWarnings()
    else:
        print "No warnings found."
    # Count Fatal Errors
    fatalerrors = mymodel.Count_Fatals()
    if fatalerrors > 0 or warnings > 0:
        print " Total Fatal Errors Found = " + str(fatalerrors)
        print "\nGenerating error summary report;" + NL
        mymodel.ProcessFatalErrors()
        # Create the Neutral file object if necessary
        title = "Fatal Error Entries from file " + prefix + ".F06" # OK to here so far.
        #==> Create a neutral file if there are nodes and elements relating
        #==> to error messages.
        print NL + "len(mymodel.elementlist) = " + str(len(mymodel.elementlist)) + \
        "  len(mymodel.nodelist)    = " + str(len(mymodel.nodelist)) + NL
        if len(mymodel.elementlist) > 0 or len(mymodel.nodelist) >0:
            print "length of mymodel.elementlist is " + str(len(mymodel.elementlist))
            try:    #error checking for can't open file and alreday exists
                neutralfile = CNeutralFile(neutralfilename,title) # create the neutral file
                createneutralfile=TRUE
                print"Writing Neutral file header"
                neutralfile.WriteNeutralFileHeader() # write the file header
            except IOError:
                print "Failed to open file" + neutralfilename
                print"Program terminating due to error."
                exit(1)

        # errors relating to elements, so write to element IDs to neutral file
        if len(mymodel.elementlist) > 0:
            print "length of mymodel.elementlist is " + str(len(mymodel.elementlist))
            print"Errors associated with the following elements;"
            uniqueelementset=set(mymodel.elementlist) # create a group of unique element IDs
            grouptitle = "Fatal Error Elements"
            groupid = 21123421 #for all errors
            entitytype = 21
            entitylist = mymodel.elementlist
            errorgroup = CNeutralGroup(neutralfile.F_NEU, groupid, grouptitle)
            errorgroup.WriteDefaultHeader(neutralfile.F_NEU)
            headerwritten = TRUE
            errorgroup.WriteDefaultEntityList(entitytype, entitylist)
            errorgroup.WriteGroupTerminator
##          neutralfile.WriteNeutralFileGroup(groupid, grouptitle, entitytype, entitylist)
            print uniqueelementset
        else:
            print"\nNo elements with FATAL errors\n"

        # Nodes relating to errors, so write node IDs to neutral file.
        if len(mymodel.nodelist) > 0:
            print"\nErrors associated with the following nodes;\n"
            uniquenodeset = set(mymodel.nodelist) # create a group of unique node IDs
            grouptitle = "Fatal Error Nodes"
            groupid = 17123417 #for all errors
            entitytype = 17
            entitylist = mymodel.nodelist
            errorgroup = CNeutralGroup(neutralfile.F_NEU, groupid, grouptitle)
            if headerwritten == FALSE:# If group header not already written, write it.
                errorgroup.WriteDefaultHeader(neutralfile.F_NEU)
            errorgroup.WriteDefaultEntityList(entitytype, entitylist)
            errorgroup.WriteGroupTerminator
#           neutralfile.WriteNeutralFileGroup(groupid, grouptitle, entitytype, entitylist)
            print uniquenodeset
        else:
            print"\nNo nodes with FATAL errors.\n"
    else:
        print "No Fatal errors found. Program Complete.\n"
        print "No Fatal errors found. Program Complete.\n"
    if createneutralfile == TRUE:
        neutralfile.WriteNeutralFileTerminator()
        print "Read file " + neutralfilename + " into FEMAP for error correction."
        exit(0)
#################################################################################

#prefix = 'v5b4u038'##<< XP home office
#positional arguments:
#inputfile
### somewhere here,
# if filename not supplied, use above prefix, else extract the prefix from the file, and
# set the local directory as applicable
#prefix = '/mnt/WinXPSP2/Documents and Settings/carlton/My Documents/QinetiQ/NxF06/AllErrors' ##<< Office Ubuntu PC
print"Attempting to run with " + prefix
main(prefix)# OK to here so far.




