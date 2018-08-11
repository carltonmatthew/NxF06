TRUE = 1
FALSE = 0
NL = '\n'   # New LIne charachter
BT = '   -1\n' # Neutral file block terminator
class CNeutralGroup:
    #This is a class to improve the mangement of groups.
    #The class needs to be able to add a range of items to its self, to enable items such as the following;
    #Nodes, Elements, NodesOnElements, ElementByNodes... etc.
    #Initially concentrate on producing groups with only a single entity type.
    #There is normaly only 1 Group daata block written when a model is output.
    #This contains all the groups in 1 large block.
    #However, for our purposes, we will assume only a single group per datablock, and use
    #multiple data blocks as required.
    def __init__(self,fp, groupNumber, grouptitle): ##>class CNeutralGroup:
        self.F_NEU = fp
        self.groupNumber = groupNumber
        self.grouptitle = grouptitle
        ### RECORD 1, Default = 99906, 0, 0
        self.groupID = groupNumber # This needs to be set to the groupp ID number (4byte long int)
        self.need_eval = 1   # Evaluation flag
        self.pre_enum = 1    # Flag to prevent group number remaining (2 byte boolean)
        ### RECORD 2
        self.title = grouptitle  # set deafult NULL title ( 79 characters max )
        ### RECORD 3, Default = 0,0
        self.layer = 0      # min & max layers in group
        self.layermin = 0
        self.layermax = 0
        self.layermethod = 0 # typical layer usage
        # (0=off, 1=greater, 2=less, 3=between, 4=outside, 5=single layer)
        ### RECORD 4, Defaut = 0,0,0,0,0,0
        self.colip_on = 0    #1 if coordinate clipping on, else 0
        self.coclip_dof = 0  #Coordinate Clipping DOF (0=X, 1=Y, 2=Z)
        self.coclip_meth = 0 #Coordinate Clipping method (0=Greater, 1=Less, 2=Between, 3=Outside)
        self.coclip_csys = 0 #Clippig cooordinate system ID
        self.coclip_min = 0  #Lower limit for coord clipping (8 byte real)
        self.coclip_max = 0  #Upper limit for coord clipping (8 byte real)
        ### RECORD 5, Default = 0,0
        self.plclip_meth = 0 #Plane clipping method (0=Off, 1=Screen, 2=Plane, 3=Volume)
        self.plclip_in = 0   #If 1 clip inside planes, if 0 clip outside planes
        ###RECORD 6 - 1 entry per plane, Repeat with next 2 records
        self.pclip_on = 0    # 1 if respective plane is on
        self.pclip_neg = -0 #=1 if clipping is on -ve side of plane
        ### 6 records
        self.pclip_base = 0 #Coordinates of plane base (8byte double precision)
        self.pclip_norm = 0 #Coordinates of plane normal
        ### RECORD 7, Default = 116, this appears to be the correct value for FEMAP 10.2
        self.max_rules = 116 #Max number of types of rules (4 byte long int)
#######################
        ### RECORD 8 - This block repeated for each rule type
        self.rule_type = 0   #Type of rule, taken from the table of Group Rule Types (114 listed in neutral.pdf)
        self.startID = -1    # minimum entity ID in rule, -1 to end rule
        self.stopID = -1     # maximum entity ID in rule
        self.incID = 0       # ID increment
        self.include = 1     # Include flag ( 0=Remove, 1=Add, -1=Exclude )
#######################
        self.maxlists = 27    # Maximum number of entity lists, -1 for last record
        self.entityID = 0    # ID of entity included in the group. Must be -1 to end the rule
#######################
    def WriteGroupTerminator(self,F_NEU): #>class CNeutralGroup:
        ##
        ## This writes a group terminator.
        ##
        self.F_NEU.write(BT+"Group Terminator")#end of block
#######################
    def WriteDefaultHeader(self,F_NEU): #>class CNeutralGroup:
        ##
        ## This writes a default block header, assuming no clipping planes etc.
        ##
        # create the neutral file group data block
        blockID = 408
        self.F_NEU.write(BT)#start of block
        self.F_NEU.write( "   " + str(blockID) +NL)#block identifier
###        self.F_NEU.write(self.grouptitle[0:80] +"#"+NL) #Group title limited to 80 characters
        ### RECORD 1
#        print "RECORD 1 = " + str(self.groupID) + ", " + str(self.need_eval) + ", " + str(self.pre_enum) + NL
        self.F_NEU.write(str(self.groupID) + ", " + str(self.need_eval) + ", " + str(self.pre_enum) + NL )
        ### RECORD 2
        self.F_NEU.write(self.title + NL )
        ### RECORD 3
        self.F_NEU.write(str(self.layer) + ", " + str(self.layermin) + ", " + str(self.layermax) + NL )
        ### RECORD 4
        self.F_NEU.write(str(self.colip_on) + ", " + str(self.coclip_dof) + ", " + str(self.coclip_meth) + ", " + str(self.coclip_csys) + ", " + str(self.coclip_min) + ", " + str(self.coclip_max) + NL)
        ### RECORD 5
        self.F_NEU.write(str(self.plclip_meth) + ", " + str(self.plclip_in) + NL )
        ### RECORD 6
        ### All zero lines for the default header
		### This assumes NO clipping planes in use.
        self.F_NEU.write("0, 0," + NL + "0.,0.,0.," + NL + "0.,0.,0.," + NL)
        self.F_NEU.write("0, 0," + NL + "0.,0.,0.," + NL + "0.,0.,0.," + NL)
        self.F_NEU.write("0, 0," + NL + "0.,0.,0.," + NL + "0.,0.,0.," + NL)
        self.F_NEU.write("0, 0," + NL + "0.,0.,0.," + NL + "0.,0.,0.," + NL)
        self.F_NEU.write("0, 0," + NL + "0.,0.,0.," + NL + "0.,0.,0.," + NL)
        self.F_NEU.write("0, 0," + NL + "0.,0.,0.," + NL + "0.,0.,0.," + NL)
        self.F_NEU.write(str(self.max_rules) + NL)
        return
################################################################################
    def WriteDefaultEntityList(self,entitytype, entitylist):#>class CNeutralGroup:
    ## write a simple entity list to the neutral file - one entry per line
        self.F_NEU.write(str(entitytype) + NL)
        for index in set(entitylist):
            self.F_NEU.write(str(index) + "," + str(index) + ",1,1," + NL)
        #write the rule list terminator
        self.F_NEU.write("-1,-1,-1,-1,\n-1\n")
        self.F_NEU.write(str(self.maxlists) + ","+NL)
        #write the entity list
        if entitytype == 17: ## Nodes
            grouplisttype = 7
        elif entitytype == 21:
            grouplisttype = 8 ## Elements
        else:
            print "WriteDefaultEntityList(self,"+str(entitytype) + "entitylist) has invalid type"
            exit(1)
        self.F_NEU.write(str(grouplisttype) + NL)
        for index in set(entitylist):
            self.F_NEU.write(str(index)+","+NL)
        self.F_NEU.write("-1" + NL) ## end list
################################################################################
###==> End of class CNeutralGroup()
################################################################################
