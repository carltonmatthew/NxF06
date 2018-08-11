TRUE = 1
FALSE = 0
NL = '\n'   # New LIne charachter
BT = '   -1\n' # Neutral file block terminator
class CNeutralFile:
    #Since neutral file data packets can be in any order, have a function for each 
    #block type. The blocks we are interested in are those for nodes and elememnts only
    #at the current time. 
    #ID=100, WriteNeutralFileHeader(self,filename)
    #ID=402, WriteNeutralFileProperties(self,propertylist)
    #ID=403, WriteNeutralFileNodes(self,nodelist)
    #ID=404, WriteNeutralFileElements(self,elementlist)
    #ID=408, WriteNeutralFileGroup(self,entitytype,entitylist)
    #ID=999, WriteNeutralFileTerminator(self)
    def __init__(self, filename, strtitle): # class CNeutralFile:
        self.filenaame = filename
        self.strtitle = strtitle
        print "Creating neutral file " + filename
        try:
            self.F_NEU = open(filename,'w')
        except IOError: 
            print "Failed to open file" + neutralfilename
            print "Program terminating in CNeutral.__init__(self,filename) due to error."
            exit(1)
        self.title = strtitle # Neutral file tile
        self.strversion='10.2'
        return
#################################################################################
##    def WriteNeutralFileHeader(self,title,strversion):# class CNeutralFile:
    def WriteNFH(self):# class CNeutralFile:
        #filename = name of the file to open, defaults to NxF06Errors.neu
        #title, defaults to errors from filename prefix.F06
        #strversion, version string of FEMAP - check start with '10.2'
        blockID = 100
#       srtversion='10.2,'
        self.F_NEU.write(BT)#start of block
        self.F_NEU.write( str(blockID) ) #block identifier
        self.F_NEU.write(self.title) #block data
        self.F_NEU.write(self.strversion) #block data
        self.F_NEU.write(BT)#terminate block
        return
################################################################################
    def WriteNeutralFileGroup(self,grouptitle,entitytype,entitylist):# class CNeutralFile:
        #Write the neutral file group
        Node_ID = 17
        Elem_ID = 21
        blockID = 408
        self.F_NEU.write('-1')#start of block
        self.F_NEU.write( '   ' + str(blockID) )#block identifier
        self.F_NEU.write(grouptitle) #block data
#       self.F_NEU.write(strversion)#block data
        if entitytype == Node_ID:
            print" Would write the following nodes when the code exists"
            print set(mymodel.nodelist)
            pass
            #write the node list to the group
        if entitytype == Elem_ID:
            print" Would write the following elements when the code exists"
            print set(mymodel.elementlist)
            pass
            #write the node list to the group
        self.F_NEU.write(BT)#terminate block
        return
#   def WriteEntityList():
#       return
################################################################################   
    def WriteNeutralFileHeader(self): # class CNeutralFile:
        #filename = name of the file to open, defaults to NxF06Errors.neu
        #title, defaults to errors from filename prefix.F06
        #strversion, version string of FEMAP - check start with '10.2'
        blockID = 100
#       strversion='10.2'
        self.F_NEU.write(BT)#start of block
        self.F_NEU.write('   ' + str(blockID) + NL)#block identifier
        self.F_NEU.write(self.title + NL)#block data
        self.F_NEU.write(self.strversion+ NL)#block data
        self.F_NEU.write(BT)#terminate block
        return
#################################################################################
    def WriteNeutralFileProperties(self,propertylist):# class CNeutralFile:
        return
#################################################################################
    def WriteNeutralFileNodes(self,nodelist):# class CNeutralFile:
        #Write a node list to the Neutral file
        blockID = 403
        return
#################################################################################
    def WriteNeutralFileElements(self,elementlist):# class CNeutralFile:
        #Write an element list to the neutral file
        blockID = 404
        return
#################################################################################
    def WriteNeutralFileTerminator(self):# class CNeutralFile:
        #Write the file terminator
        blockID = 999
        self.F_NEU.write('-1' + NL)#start of block
        self.F_NEU.write( str(blockID) + NL)#block identifier
        self.F_NEU.write(BT + NL)#terminate block
        self.F_NEU.close() # close the file
        return
#################################################################################
    def WriteNeutralFileCreateGroup(self,groupID,grouptitle):# class CNeutralFile:
        # create the neutral file group data block
        blockID = 408
        self.F_NEU.write(BT)#start of block
        self.F_NEU.write( str(blockID) +NL)#block identifier
        self.F_NEU.write(grouptitle[0:80] + NL) #Group title limited to 80 characters
        return
################################################################################
    def WriteNeutralFileGroup(self,grouptitle,entitytype,entitylist):# class CNeutralFile:
        #Write the neutral file group
        Node_ID = 17
        Elem_ID = 21
        blockID = 408
        self.F_NEU.write(BT)#start of block
        self.F_NEU.write( str(blockID) )#block identifier
        self.F_NEU.write(grouptitle) #block data
#       self.F_NEU.write(strversion)#block data
        if entitytype == Node_ID:
            print" Would write the following nodes when the code exists"
            print set(mymodel.nodelist)
            pass
            #write the node list to the group
        if entitytype == Elem_ID:
            print" Would write the following elements when the code exists"
            print set(mymodel.elementlist)
            pass
            #write the node list to the group
        self.F_NEU.write('-1')#terminate block
        return
#################################################################################   
### end of class CNeutralFile
