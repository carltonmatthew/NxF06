#class CNeutral:
#   #read, write and process neutral files
#   #Since neural file data packets can be in any order, have a function for each 
#   #block type. The blocks we are interested in are those for nodes and elememnts only
#   #at the current time. 
#   #ID=100, WriteNeutralFileHeader(self,filename)
#   #ID=402, WriteNeutralFileProperties(self,propertylist)
#   #ID=403, WriteNeutralFileNodes(self,nodelist)
#   #ID=404, WriteNeutralFileElements(self,elementlist)
#   #ID=408, WriteNeutralFileGroup(self,entitytype,entitylist)
#   #ID=999, WriteNeutralFileTerminator(self)
#################################################################################
#   def __init__(self,filename):# class CNeutral:
#        self.filename='NxF06Errors.neu'
#       print "CNeutral:Creating neutral file " + filename
#       try:
#           self.F_NEU = open(filename,'w')
#       except IOError: 
#           print "Failed to open file" + neutralfilename
#           print "Program terminating in CNeutral.__init__(self,filename) due to error."
#           exit(1)
#       self.strversion = '10.2' # set the default file standard to version 10.2
#       return
#################################################################################
#   def WriteNeutralFileHeader(self,title):# class CNeutral:
#       #filename = name of the file to open, defaults to NxF06Errors.neu
#       #title, defaults to errors from filename prefix.F06
#       #strversion, version string of FEMAP - check start with '10.2'
#       blockID = 100
#       self.F_NEU.write(BT)           #start of block
#       self.F_NEU.write( str(blockID) + NL ) #block identifier
#       self.F_NEU.write(title + NL)          #block data
#       print "\n\nNeutral file title = " + title
#       self.F_NEU.write(self.strversion + NL)#block data
#       self.F_NEU.write('-1' + NL)           #terminate block
#       return
################################################################################
#   def WriteNeutralFileGroup(self, groupID, grouptitle, entitytype, entitylist):# class CNeutral:
#       #Write the neutral file group
#       Node_ID = 17
#       Elem_ID = 21
#       blockID = 408
#       ### Create theNeutral file group object
#       groupdata=CNeutralGroup(self.F_NEU,groupID,grouptitle)
#       groupdata.WriteDefaultHeader(self.F_NEU)# Write the default block header, no clipping planes etc.
#       groupdata.WriteDefaultEntityList(entitytype, entitylist)
#       self.F_NEU.write('-1\n')#start of block
#       self.F_NEU.write( str(blockID) + NL)#block identifier
#       self.F_NEU.write(grouptitle + NL) #block data
#       if entitytype == Node_ID:
#           print" Would write the following nodes when the code exists"
#           print set(entitylist)
#           linelength = 0
#           self.F_NEU.write("\n The following nodes relate to errors")
#           self.F_NEU.write(NL)
#           for index in set(entitylist):
#               linelength=linelength+len(str(index)+ " ")
#               self.F_NEU.write(str(index)+ " ")
#               print "WriteNeutralFileGroup: linelength = " + str(linelength)
#               if linelength+len(str(index)+ " ") > 80:
#                   self.F_NEU.write('\n')
#                   linelength = 0
#           #write the node list to the group
#           self.F_NEU.write(NL + BT)
#
#       if entitytype == Elem_ID:
#           print" Would write the following elements when the code exists"
#           linelength = 0
#           print set(entitylist)
#           self_F_NEU.write("\n The following elements relate to errors")
#           for index in entitylist:
#               linelength=linelength+len(str(index)+ " ")
#               self.F_NEU.write(str(index)+ " ")
#               if linelength > 80:
#                   self.F_NEU.write(NL)
#                   linelength = 0
#           pass
#           #write the node list to the group
#       self.F_NEU.write(BT) #terminate block
#       return
################################################################################
#   def WriteNeutralFileTerminator(self):# class CNeutral:
#       #Write the file terminator
#       blockID = 999
#       self.F_NEU.write(BT)#start of block
#       self.F_NEU.write( str(blockID) + NL)#block identifier
#       self.F_NEU.write(BT)#terminate block
#       self.F_NEU.close() # close the file
#       print"\n\nNeutral file CLOSED"
#       return
#################################################################################   
###==> End of class CNeutral()
#################################################################################   
