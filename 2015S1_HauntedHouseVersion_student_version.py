# -*- coding: utf-8 -*-
# Date: 17 Mar 2015
# Modified by Tony Kuo, David McCurdy

# NOTE: 
# This game was created based on the book: Write Your Own Adventure Programs
# Written by Jenny Tyler, Les Howarth
# Published by Usborne computer books, 1983
# https://books.google.co.nz/books?id=f6BoAAAACAAJ

# Description: Code used for ISCG 5420 Assignment 2015 S1. 


import random
import sys

#############################################################################################################
# GAME DATA                                                                                                 #
#############################################################################################################

# SOME CONSTANTS
SAVE_FILE_NAME = "GAME.SAV"

location = 0

HERO_INVENTORY_POS = 999

DirectionsList = ['SE', 'WE',  'WE',  'SWE', 'WE',   'WE',  'SWE',  'WS', #0-7
                   'NS', 'SE',  'WE',  'NW',  'SE',   'W',   'NE',   'NSW', #8-15
                   'NS', 'NS',  'SE',  'WE',  'NW', 'SE',  'WS', 'NS', #16-23
                   'N',  'NS',  'NSE',  'WE',  'WE',   'NSW', 'NS',   'NS', # 24 - 31
                   'S',  'NSE', 'NSW', 'S',   'NS', 'N',   'N',    'NS', #32 - 39
                   'NE', 'NSW',  'NE',  'W',   'NSE',  'WE',  'W',    'NS', #40 - 47
                   'SE', 'NSW', 'E',   'WE',  'NW',   'SE',   'SWE',   'NW', #48 - 55
                   'NE', 'NWE', 'WE',  'WE',  'WE',   'NWE', 'NWE',  'W'] #56 - 63



# '\' below is a continuation character, it tells Python that the current statement continues to the next line.
LocationsList = \
[ 'DARK CORNER',                  'OVERGROWN GARDEN',       'BY LARGE WOODPILE',         'YARD BY RUBBISH',
  'WEEDPATCH',                    'FOREST',                 'THICK FOREST',              'BLASTED TREE',
  'CORNER OF HOUSE',              'ENTRANCE TO KITCHEN',    'KITCHEN & GRIMY COOKER',    'SCULLERY DOOR',
  'ROOM WITH INCHES OF DUST',     'REAR TURRET ROOM',       'CLEARING BY HOUSE',         'PATH',
  'SIDE OF HOUSE',                'BACK OF HALLWAY',        'DARK ALCOVE',               'SHALL DARK ROOM',
  'BOTTOM OF SPIRAL STAIRCASE',   'WIDE PASSAGE',           'SLIPPERY STEPS',            'CLIFFTOP',
  'NEAR CRUMBLING WALL',          'GLOOMY PASSAGE',         'POOL OF LIGHT',             'IMPRESSIVE VAULTED HALLWAY',
  'HALL BY THICK WOODEN DOOR',    'TROPHY ROOM',            'CELLAR WITH BARRED WINDOW', 'CLIFF PATH',
  'CUPBOARD WITH HANGING COAT',   'FRONT HALL',             'SITTING ROOM',              'SECRET ROOM',
  'STEEP MARBLE STAIRS',          'DINING ROOM',            'DEEP CELLAR WITH COFFIN',   'CLIFF PATH',
  'CLOSET',                       'FRONT LOBBY',            'LIBRARY OF EVIL BOOKS',   'STUDY WITH DESK & HOLE IN WALL',
  'WEIRD COBWEBBY ROOM',          'VERY COLD CHAMBER',      'SPOOKY ROOM',               'CLIFF PATH BY MARSH',
  'RUBBLE-STREWN VERANDAH',       'FRONT PORCH',            'FRONT TOWER',               'SLOPING CORRIDOR',
  'UPPER GALLERY',                'MARSH BY WALL',          'MARSH',                     'SOGGY PATH',
  'BY TWISTED RAILING',           'PATH THROUGH IRON GATE', 'BY RAILINGS',               'BENEATH FRONT TOWER',
  'DEBRIS FROM CRUMBLING FACADE', 'LARGE FALLEN BRICKWORK', 'ROTTING STONE ARCH',        'CRUMBLING CLIFFTOP']

VerbList = ['HELP', 'CARRYING?', 'GO',    'N',       'S',       'W',     'E',   'U',      'D',
            'GET',  'TAKE',      'OPEN',  'EXAMINE', 'READ',    'SAY',
            'DIG',  'SWING',     'CLIMB', 'LIGHT',   'UNLIGHT', 'SPRAY', 'USE', 'UNLOCK', 'DROP', 'SCORE', 'QUIT']
VerbHelpList = ['Display all possible actions you can carry out in this game','Display your inventory', " ",
              'North', 'South', 'West', 'East', 'Up','Down', 'Get an item from the current location', 'Get item', 'Open door', 'Examining an item to find out more about it',
              'read instructions', 'Make a noise','Dig on the ground(Requires Player to have shovel in the inventory)', 'Get across', 'Get up ladder', 'Can see', 'Cannot move',
              'Kill bugs', ' ',' ', 'Drop item', 'Display your current score', 'Quit the game']

# These list may be useful in the future
#NounList = ['NORTH',   'SOUTH',  'WEST',   'EAST',    'UP',   'DOWN',
#            'DOOR',    'BATS',   'GHOSTS', 'X2ANFAR', 'SPELLS', 'WALL']

#PropList = ['DRAWER',  'DESK', 'COAT', 'RUBBISH', 'COFFIN', 'BOOKS']

#PositionOfProps = [43, 43, 32, 3, 38, 35]

ItemList = ['PAINTING', 'RING',      'MAGIC SPELLS', 'GOBLET', 'SCROLL', 'COINS', 'STATUE',  'CANDLESTICK', 'MATCHES',
            'VACUUM',   'BATTERIES', 'SHOVEL',       'AXE',    'ROPE',   'BOAT',  'AEROSOL', 'CANDLE',      'KEY',
            'GRAIL', 'TORCH']

PositionOfItems = [46, 38, 35, 50, 13, 18, 28, 42, 10, 25, 26, 4, 2, 7, 47, 60, 100, 100, 12, 100]

MONSTER_HEAVEN = 888
MonsterList = ["GHOST"]
PositionOfMonster = [12]
is_candle_light = False
is_torch_on = False
has_matches = False
has_candle = False

VisitedLocations =[0]


#############################################################################################################
# HELPER FUNCTIONS                                                                                          #
#############################################################################################################


def isMultiwordStatement(value):
    return value.find(" ") != -1

def isItemAvailableAtLocation(ItemID, currentLocation):
    return PositionOfItems[ItemID] == currentLocation

def isMonsterAtLocation(currentLocation):
    for i in range(0, len(PositionOfMonster), 1):
        if PositionOfMonster[i] == currentLocation:
            return True
        else:
            return False

def isItemInInventory(itemName):
    ItemID = GetItemID(itemName)
    return PositionOfItems[ItemID] == HERO_INVENTORY_POS

def isItemHidden(itemName):
    # 100 is the location for hidden items. 
    ItemID = GetItemID(itemName)
    return PositionOfItems[ItemID] == 100

def GetItemID(item):
    for ItemID in range(0, len(ItemList), 1):
        if item == ItemList[ItemID]:
            return ItemID
    # item not found
    return -1


def contains(validValues, values):
    """
    Function: contains
    validValues: a string containing all the valid characters allowed
    values: a string that need to be checked (to see whether it contains only valid characters)
    """
    validCount = 0
    lengthValues = len(values)
    for letter in validValues:
        for character in values:
           if letter == character:
                validCount=validCount+1
    return validCount == lengthValues


def isAlphabetic(value):
    alphabeticCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return contains(alphabeticCharacters, value)

def isValidName(value):
    alphabeticCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ &-"
    return contains(alphabeticCharacters, value)



#############################################################################################
# GAME LOGIC                                                                                #
#############################################################################################

def GetVerbFromSentence(sentence):
    if not isMultiwordStatement(sentence):
        return sentence
    locationOfSpace=sentence.find(" ")
    return sentence[:locationOfSpace]

def GetNounFromSentence(sentence):
    if not isMultiwordStatement(sentence):
        return ""
    locationOfSpace=sentence.find(" ") + 1
    return sentence[locationOfSpace:]



def isMovementAvailable(directioncharacter, currentLocation):
    """
    isMovementAvailable checks whether it is possible to move in a direction in the current location


    directioncharacter - intended direction to move toward at the currentLocation
    returns True or False - based on whether the directioncharacter can be found in the String from DirectionsList[currentLocation]

    Example: 
    if directioncharacter is 'N' and DirectionsList[currentLocation] is 'NSW', this function returns True
    """
    
    dirString = DirectionsList[currentLocation]
    result = dirString.find(directioncharacter)
    if result >= 0:
        return True
    else:
        return False
    

def isMovementVerb(verb, noun):
    return verb == 'N' or verb == 'S' or verb == 'E' or verb == 'W' or verb == 'U' or verb == 'D' or verb == 'GO'

def GetMovementDirection(statement):
    verb=GetVerbFromSentence(statement)
    noun=GetNounFromSentence(statement)
    if len(verb)==1:
        return verb
    if verb == 'GO':
        return noun[:1]
    return ''

def isEndOfGame(score, currentLocation):
    return score == 5 and currentLocation == 0

def GetScore():
    score = 0
    for name in ItemList:
        if isItemInInventory(name):
            score +=1
    return score
    
#############################################################################################
# END GAME LOGIC                                                                            #
#############################################################################################

#############################################################################################
# BEGIN PRESENTATION LOGIC                                                                  #
#############################################################################################

def DisplayCongratulation():
    print("""
 __     __                    _       
 \ \   / /                   (_)      
  \ \_/ /__  _   _  __      ___ _ __  
   \   / _ \| | | | \ \ /\ / / | '_ \ 
    | | (_) | |_| |  \ V  V /| | | | |
    |_|\___/ \__,_|   \_/\_/ |_|_| |_|
                                      
 """)                                     
def DisplayHelpMessage():
    print("I UNDERSTAND THE FOLLOWING WORDS:")
    for index in range(0, len(VerbList)):
        print(VerbList[index] + '\t\t- ' + VerbHelpList[index])

    
def DisplayInventory():
    strItems=""
    for i in range(len(PositionOfItems)):
        if PositionOfItems[i] == HERO_INVENTORY_POS:
            strItems = strItems + " "+ ItemList[i]
    
    if len(strItems) == 0:
        strItems = "NOTHING"
    print("YOU ARE CARRYING:" + strItems)
    
def DisplayMagicMessage(currentLocation, newLocationID) :
    print ("YOU UTTER WORDS OF DARK MAGIC... X2ANFAR!")
    print ("YOU DISAPPEAR AND REAPPEAR IN ANOTHER LOCATION...")
    print ("YOU WERE IN " + LocationsList[currentLocation])
    print ("YOU ARE NOW IN " + LocationsList[newLocationID])


def printlocation(current_location, print_location):
    if current_location == print_location:
        return "**"
    else:
        return PrintableInts(print_location)



def DisplayMap(current_location):

    """
     Each row of the map is consisted of 3 lines
     The first line - contains exit to North
     The second line - contains exits to West and East plus room no.
     The third line - contains exit to South
     
    """
    Line1 = ""
    Line2 = ""
    Line3 = ""
    # Use a FOR loop to draw every room
    for Index in range (0, 64, 1):
        if Index in VisitedLocations:
            # assign the exits at location 'Index' to currentValues
            # e.g. "NSW" if there are exits to North, South, and West
            currentValues=DirectionsList[Index]

            # if there is exit to the north draw a gap between the blocks
            if "N" in currentValues:
                Line1 += '█  █'
            # otherwise, draw a wall
            else:
                Line1 += "████"
                
            if "W" in currentValues:
                Line2 += (" ") + printlocation(current_location, Index)
            else:
                Line2 += ("█") + printlocation(current_location, Index)
            
                
            if "E" in currentValues:
                Line2 += " "
            else:
                Line2 += "█"

            if "S" in currentValues:
                Line3 += "█  █"
            else:
                Line3 += "████"
        else:
            Line1 += "    "
            Line2 += "    "
            Line3 += "    "
        # Draw the first row of rooms if 8 rooms have been processed.     
        if (Index + 1) % 8 == 0:
            print (Line1)
            print (Line2)
            print (Line3)
            # Emptying the lines for the next row of 8 rooms.
            Line1 = ""
            Line2 = ""
            Line3 = "" 
                                

def ExamineCoat(currentLocation):
    if currentLocation == 32 and isItemHidden("Key"):
        PositionOfItems[GetItemID("KEY")] = 32
        print ("YOU EXAMINE THE COAT AND FIND A KEY IN THE POCKET")
    elif currentLocation == 32 and not isItemHidden("Key"):
        print ("IT\'S A DIRTY OLD COAT")
    else:
        print ("WHAT COAT?")


def ExamineDrawer(currentLocation):
    if currentLocation == 43 and isItemInInventory("KEY") :
        print ("YOU UNLOCK THE DRAWER AND FIND IT IS EMPTY")
    elif currentLocation == 43 and not isItemInInventory("KEY") :
        print ("UNFORTUNATELY THE DRAWER IS LOCKED")
    else:
        print ("WHAT DRAWER?")

    

def ExamineRubbish(currentLocation):
    if currentLocation == 3:
        print ("THE RUBBISH IS FILTHY")
    else:
        print ("WHAT RUBBISH?")

def ExamineWall(currentLocation):
    if currentLocation == 43:
        LocationsList[currentLocation] = "STUDY WITH DESK"
        DirectionsList[currentLocation]="NW"
        print ("YOU LOOK AT THE WALL AND DISCOVER IT IS FALSE!\nYOU DISCOVER A NEW EXIT")
    else:
        print ("NO INTERESTING WALLS HERE")

def ExamineDoor(currentLocation):
    if currentLocation == 28 and  isItemInInventory("KEY"):
        DirectionsList[currentLocation]="SEW"
        print ("YOU UNLOCK THE DOOR AND DISCOVER A NEW LOCATION!")
    elif currentLocation == 28 and  not isItemInInventory("KEY"):
        print ("UNFORTUNATELY THE DOOR IS LOCKED")
    else:
        print ("NO INTERESTING DOOR HERE")
    
def ExamineBooks(currentLocation):
    if currentLocation == 42 and isItemHidden("CANDLE"):
        print ("YOU LOOK AT THE BOOKS AND FOUND A CANDLE IN BETWEEN BOOKS!")
        PositionOfItems[GetItemID("CANDLE")] = 42
    elif currentLocation == 42 and not isItemHidden("CANDLE"):
        print ("THE BOOKS LOOK EVIL")
    else:
        print ("NO BOOKS HERE")

def ExamineTree(currentLocation):
    if currentLocation == 7 and isItemHidden("TORCH"):
        print ("YOU LOOK IN THE TREE AND FIND A TORCH IN THE BRANCHES!")
        PositionOfItems[GetItemID("TORCH")] = 7
    elif currentLocation == 42 and not isItemHidden("TORCH"):
        print ("YOU LOOK AT THE TREE. IT LOOKS NICE.")
    else:
        print ("THERE IS NO TREE HERE")

def DoExamine(currentLocation, noun) :
    if noun == "COAT":
        ExamineCoat(currentLocation)
    elif noun == "DRAWER":
        ExamineDrawer(currentLocation )
    elif noun == "RUBBISH":
        ExamineRubbish(currentLocation)
    elif noun == "WALL":
        ExamineWall(currentLocation)
    elif noun == "DOOR":
        ExamineDoor(currentLocation)
    elif noun == "BOOKS":
        ExamineBooks(currentLocation)
    elif noun == "TREE":
        ExamineTree(currentLocation)
    else:
        print ("WHAT "+noun+"?")
    
          

def PrintableInts(value):
    if(value<10):
        return " "+str(value)
    return str(value)


def Dig(currentLocation):
    if currentLocation == 30 and isItemInInventory("SHOVEL"):
        DirectionsList[currentLocation]="NSE"
        LocationsList[30] = 'HOLE IN WALL'
        print ("YOU DIG AROUND THE ROOM. THE BARS IN THE WINDOW BECOME LOOSE! REVEALLING A NEW EXIT!")
    elif isItemInInventory("SHOVEL"):
        print ("YOU DIG A LITTLE HOLE.")
    else:
        print ("YOU HAVE NOTHING TO DIG WITH")

def vacuum(currentLocation):
    """
    If you are in the same location as a monster then the monster is sent to
    monster heaven
    """
    for i in range(0, len(PositionOfMonster), 1):
        if PositionOfMonster[i] == currentLocation:
            PositionOfMonster[i] = MONSTER_HEAVEN
            print("YOU SUCKED THE", MonsterList[i], "IN TO THE VACUUM. WHO YOU GONNA CALL ;-)")

def light():
    if isItemInInventory("CANDLE") and isItemInInventory("MATCHES"):
        print("YOU LIGHT THE CANDLE")
        global is_candle_light
        is_candle_light = True
    elif  isItemInInventory("TORCH"):
        print("YOU TURN THE TORCH ON")
        global is_torch_on
        is_torch_on = True
    else:
        print("YOU NEED THE CANDLE AND MATCHES OR THE TORCH")


#############################################################################################
# END PRESENTATION LOGIC                                                                    #
#############################################################################################


def ListItemsAtPosition(currentLocation):
    strItems=""
    for i in range(0, len(PositionOfItems), 1):
        if PositionOfItems[i] == currentLocation:
            strItems = strItems + " "+ ItemList[i]
    return strItems

def ListMonsterAtPosition(currentLocation):
    strItems=""
    for i in range(0, len(PositionOfMonster), 1):
        if PositionOfMonster[i] == currentLocation:
            strItems = strItems + " "+ MonsterList[i]
    return strItems

def ItemsAvailableAtPosition(currentLocation):
    for i in range(0, len(PositionOfItems), 1):
        if PositionOfItems[i] == currentLocation:
            return True
    return False

def MonsterAtPosition(currentLocation):
    for i in range(0, len(PositionOfMonster), 1):
        if PositionOfMonster[i] == currentLocation:
            return True
    return False

def GoMagic(currentLocation):
    newLocationID=currentLocation
    while(newLocationID == currentLocation):
           newLocationID = random.randint(0,63)

    return newLocationID;

def Go(statement, currentLocation):
    directioncharacter = ''

    verb=GetVerbFromSentence(statement)
    noun=GetNounFromSentence(statement)

    directioncharacter = verb
    if verb == 'GO':
        directioncharacter = noun[:1]

    # First problem
    if currentLocation == 20 and not(is_candle_light or is_torch_on) and directioncharacter == "N":
        print("IT'S TOO DARK TO SEE WHERE YOU ARE GOING. YOU NEED SOME LIGHT")
        return currentLocation

    if isMovementAvailable(directioncharacter, currentLocation):
        if directioncharacter == 'N':
            currentLocation -= 8
        elif directioncharacter == 'S':
            currentLocation += 8
        elif directioncharacter == 'W':
            currentLocation -= 1
        elif directioncharacter == 'E':
            currentLocation += 1


    return currentLocation

def GetItem(noun, currentLocation):
    ItemID = GetItemID(noun)
    if isMonsterAtLocation(currentLocation):
        print("THE", ListMonsterAtPosition(location), "BLOCKS YOUR WAY.")
    elif isItemAvailableAtLocation(ItemID, currentLocation):
        PositionOfItems[ItemID]=HERO_INVENTORY_POS
        print("YOU ARE NOW CARRYING A",noun)

        if has_candle and noun == "MATCHES":
            print("YOU CAN NOW LIGHT THE CANDLE")
            global has_matches
            has_matches = True
        else:
            print("YOU NEED SOMETHING TO LIGHT")

        if not has_matches and noun == "CANDLE":
            print("ALL YOU NEED NOW IS SOME WAY TO LIGHT IT")
        else:
            print ("THIS WILL BE USEFUL IF YOU FIND YOURSELF IN A DARK PLACE.")

    else:
        print("SORRY YOU CANNOT TAKE A ", noun)
    
        
def DropItem(noun, currentLocation):
    ItemID = GetItemID(noun)
    if isItemAvailableAtLocation(ItemID, HERO_INVENTORY_POS):
        PositionOfItems[ItemID] = currentLocation
        print("YOU HAVE DROPPED THE ", noun)
    else:
        print("YOU CANNOT DROP THAT WHICH YOU DO NOT POSSESS")

def OpenDoor(currentLocation):
    if currentLocation == 28 and isItemInInventory("KEY"):
        DirectionsList[currentLocation]="SEW"
        print("THE DOOR IS NOW OPEN! REVEALLING A NEW EXIT!")
    else:
        print("THE DOOR IS LOCKED")


def GiveItToMe():
    """Allow user to cheat and get any item they want"""
    print("POSSIBLE ITEMS TO GET:")

    str_items = ""
    for i in range(len(PositionOfItems)):
        if i == 0:
            str_items = ItemList[i]
        else:
            str_items = str_items + ", " + ItemList[i]
    print(str_items)

    itemId = -1
    while itemId == -1:
        item = raw_input("NAME THE ITEM YOU NEED:")
        item = item.upper()
        itemId = GetItemID(item)
        if itemId != -1:
            PositionOfItems[itemId] = HERO_INVENTORY_POS

    print(item, "SUDDENLY APPEARED IN YOUR HAND")
    
        
def ProcessStatement(statement, currentLocation):
    '''
      A statement can be either a verb or a verb + a noun
      If a statement is consisted of 1 verb and 1 noun, (separated by a space), it can looks like 'examine desk', 'get axe' ..etc
    '''

    
    verb=GetVerbFromSentence(statement)
    noun=GetNounFromSentence(statement)    

    if verb== "HELP":
        DisplayHelpMessage()

    elif verb=="CLEAR":
        clearLocationHistory()

    elif verb == "SCORE":
        print("YOUR CURRENT SCORE IS:", GetScore())

    elif verb == "CARRYING" or verb == "CARRYING?" or verb == "INVENTORY" or verb == "INV":
        DisplayInventory()

    elif verb == "GET" or verb == "TAKE":
        GetItem(noun,currentLocation)

    elif ((verb == "OPEN" or verb == "UNLOCK") and noun == "DOOR") or (verb =="USE" and noun == "KEY"):
        OpenDoor(currentLocation)
        
    elif verb == "DIG" or (verb =="USE" and noun=="SHOVEL"):
        Dig(currentLocation)

    elif verb == "USE" and noun == "VACUUM":
        vacuum(currentLocation)

    elif verb == "LIGHT" and (noun == "CANDLE" or noun == "TORCH"):
        light()

    elif verb == "DROP":
        DropItem(noun, currentLocation)

    elif verb == "EXAMINE":
        DoExamine(currentLocation, noun)

    elif verb == "SAY" and noun == "X2ANFAR":
        newLocationID = GoMagic(currentLocation)
        DisplayMagicMessage(currentLocation, newLocationID)
        currentLocation = newLocationID

    elif verb == "SHOW" and noun == "MAP" or verb == "SS":
        DisplayMap(currentLocation)
        

    elif isMovementVerb(verb, noun):  
        newLocationID = Go(statement, currentLocation)
        if currentLocation != newLocationID:
            print("YOU MOVED FROM " + LocationsList[currentLocation] + " TO " + LocationsList[newLocationID])
        else:
            print("YOU ARE UNABLE TO MOVE IN THAT DIRECTION")
        currentLocation = newLocationID

    elif verb == "GIVEITTOME":
        GiveItToMe()
    elif verb == "SAVE":
        # Call save game
        save_game(currentLocation)
    elif verb == "LOAD":
        currentLocation = load_game()

    return currentLocation

def list_to_string(list_to_convert):
    string = ""
    for item in list_to_convert:
        if string == "":
            string += str(item)
        else:
            string += "," + str(item)
    return string

def string_to_list(string):
    new_list =[]
    for item in string.split(","):
        new_list.append(int(item))
    return new_list

def save_game(currentLocation):
    """This save the player current progress"""

    file_object = open(SAVE_FILE_NAME, 'w')
    file_object.write(str(currentLocation) + "\n")

    locations = list_to_string(VisitedLocations)
    file_object.write(locations + "\n")

    items = list_to_string(PositionOfItems)
    file_object.write(items + "\n")

    file_object.close()
    print("You have saved your game")
    return

def load_game():
    """Loads the player progress from a file"""
    file_object = open (SAVE_FILE_NAME, 'r')
    curr = file_object.readline()
    been_there = file_object.readline()

    global VisitedLocations
    VisitedLocations = string_to_list(been_there)

    items = file_object.readline()
    global PositionOfItems
    PositionOfItems = string_to_list(items)

    file_object.close()
    print("You have loaded your game")
    return int(curr)

def show_menu():
    """Shows the starting menu"""
    global location
    print("MENU")
    print("NEW GAME")
    print("CONTINUE")
    print("QUIT")
    # validate raw_input
    command = ""

    while command != "NEW GAME" and command != "CONTINUE" and command != "QUIT":
        command = raw_input("PLEASE CHOOSE AN OPTION FROM THE MENU:")
        command = command.rstrip("\r").upper()
        if command != "NEW GAME" and command != "CONTINUE" and command != "QUIT":
            print("YOUR OPTION IS INCORRECT")

    if command == "QUIT":
        return "QUIT"
    elif command == "NEW GAME":
        return ""
    elif command == "CONTINUE":
        location = load_game()
        return ""

def clearLocationHistory():
    global VisitedLocations
    VisitedLocations=[]
    VisitedLocations.append(0)
    

def beenThere():
    global VisitedLocations
    VisitedLocations=[]
    for i in range(0,64):
        VisitedLocations.append(i)

def location_description(location):
    if location == 20 and (not is_candle_light and not is_torch_on):
        return "IT IS TOO DARK TO SEE ANYTHING. YOU NEED SOME LIGHT"
    else:
        return "YOU ARE LOCATED IN A " + LocationsList[location]

def Game():
    global location
    location = 0
    statement = show_menu()
    while (not isEndOfGame(GetScore(),location)) and statement != "QUIT":
    
        print("========Haunted House=========")
        print( location_description(location),"("+str(location)+")")
        if ItemsAvailableAtPosition(location):
            print("YOU CAN SEE THE FOLLOWING ITEMS AT THIS LOCATION: ", ListItemsAtPosition(location))
        if MonsterAtPosition(location):
            print("YIKES THERE IS A", ListMonsterAtPosition(location), "HERE!")
        print("VISIBLE EXITS: ", DirectionsList[location])
        
        statement = raw_input("WHAT DO YOU WANT TO DO NEXT?")
        statement = statement.rstrip("\r").upper()
        location = ProcessStatement(statement, location)
        if not (location in VisitedLocations):
            VisitedLocations.append(location)
        
        DisplayMap(location)

    if statement != "QUIT":
        DisplayCongratulation()
    else:
        print("Exiting game")
Game()

