# Aggrevation!
from random import randint
import sys

# FIXME: If I'm in the magic circle, and I roll a 6, it is
# theoretically possible to move back to where I am. However, the
# check to see if the destination has one of my dudes in it will fail
# because I am there (but I'd move to move).

# Notes:
#   ASCII doesn't have an cyan, so I'm using cyan instead. (or
#   purple?)

# GLOBALS
BOARDSIZE = 84  # Number of space around the main track
CENTER=98       # "Location" of the center of death.
BASE=99         # "Location" for base spots.  All are 99.
HOME=100        # "Location" for home spots - 100, 101, 102, 103
HOMESIZE=4      # How big is your home?

Colors = [ "blue", "pink", "cyan", "yellow", "green", "white" ]
Board = ["" for x in range(0,BOARDSIZE)]
CenterSpace = ""
MagicCircle = [ 7, 21, 35, 49, 63, 77 ]     # Locations for the magic circle spaces
Base = {}       # Dict of each color's base status
Home = {}       # Dict of each color's home status
Marbles = {}    # Dict of each color's marble locations
Players = []    # List of active players

## What is space 0??
# Marbles[color] : { location0, location1, location2, location3 }
# Start[color] : space#
Start = { 
        "blue": 0,
        "pink": 14,
        "cyan": 28,
        "yellow": 42 ,
        "green": 56 ,
        "white": 70
        }


#
# Roll():
#
# Roll a die.
# Returns an int between 1 and 6
#
def Roll():
    return randint(1,6)

#
# Display():
#
# Prints out the state of the board.
# XXX: This could be replaced with Tk or something else.
#
def Display():
    # Color!
    # ANSI color codes for the marbles
    ccode={
            "blue": "\033[1;37;44m",
            "pink": "\033[1;37;41m",
            "cyan": "\033[1;37;46m",
            "yellow": "\033[1;37;43m",
            "green": "\033[1;37;42m",
            "white": "\033[1;34;47m",
            }

    # ANSI color codes for start
    startColor={
            "blue": "\033[1;34;40m",
            "pink": "\033[1;31;40m",
            "cyan": "\033[1;36;40m",
            "yellow": "\033[1;33;40m",
            "green": "\033[1;32;40m",
            "white": "\033[1;30;47m",
            }

    # Reset the color to default
    creset="\033[m"

    for i in range(0,BOARDSIZE):
        space = Board[i]
        if space == "":
            # Use a * to indicate magic circle
            if i in MagicCircle:
                print ("*", end="")
                continue
            # Use a # to indicate start spaces
            elif i in Start.values():
                # What's this? I need to get the color given the
                # value.  So here's a bunch of casting black magic to
                # do that.
                thiscolor = list(Start.keys())[list(Start.values()).index(i)]
                print (startColor[thiscolor]+"#"+creset, end="")
            else:
                print ("-", end="")

        # Occupied space
        else:
            # If you're on the magic circle, you get an upper case
            # letter
            if i in MagicCircle:
                print (ccode[space]+space[0].upper()+creset, end="")
            else:
                print (ccode[space]+space[0]+creset, end="")

    # Show the center of death
    if CenterSpace:
        print ("\t",ccode[CenterSpace]+CenterSpace[0]+creset)
    else:
        print ("\t","-")

    print()

    for p in Players:
        if len(Base[p]):
            print ("Base of %s:" %p, end="")
            for b in Base[p]:
                if b != "":
                    print (ccode[b]+b[0]+creset, end="")
            print()

    for p in Players:
        print ("Home of %s:" %p, end="")
        for h in Home[p]:
            if h == "":
                print ("-", end="")
            else:
                print (ccode[h]+h[0]+creset, end="")
        print()

#
# Bonk!
#
# send a guy back to base
#
def Bonk(space):
    # FIXME: Problem removing the dead guy.  ListMoves still includes
    # him. FIXED elsewhere (I think)
    if space == CENTER:
        deadGuy = CenterSpace
    else:
        deadGuy = Board[space]
        Board[space] = ""

    Marbles[deadGuy].append(BASE)
    Marbles[deadGuy].remove(space)
    Base[deadGuy].append(deadGuy)

#
# Move(color, source, destination):
#
# Move marble of color color from source to destination.
#
def Move(color, source, destination):
    global CenterSpace

    # Remove marble from source
    #print ("CenterSpace = %s" %CenterSpace)
    if source == CENTER:
        assert CenterSpace == color
        CenterSpace = ""
    elif source == BASE:
        # Remove the marble from the base
        assert Base[color].count(color) > 0
        Base[color].remove(color)

        # The destination is that color's start
        destination = Start[color]
    elif source >= HOME:
        Home[color][source-HOME] = ""
    else:
        assert Board[source] == color
        Board[source] = ""

    # Deal with possible destinations
    if destination == CENTER:
        assert CenterSpace != color
        if CenterSpace:
            Bonk(CENTER)
            print ("Bonk! %s hits %s!" %(color, CenterSpace))
        CenterSpace = color
    elif destination >= HOME:
        assert Home[color][destination-HOME] != color
        Home[color][destination-HOME] = color
    else:   # Board destination is not the center or Home
        assert Board[destination] != color
        # Deal with bonking if destination is not empty
        if Board[destination]:
            Bonk(destination)
            print ("Bonk! %s hits %s!" %(color,Board[destination]))
        Board[destination] = color

    Marbles[color].remove(source)
    Marbles[color].append(destination)

#
# Setup():
#
# Gets the board ready for a new game, and assigns player colors.
# Returns: Number of Players
#
def Setup():
    # Initialize the bases and colors
    for c in Colors:
        Base[c] = [ c, c, c, c]
        Home[c] = [ "", "", "", ""]
        Marbles[c] = [BASE, BASE, BASE, BASE ]      # Where are my marbles? BASE
    #print ("Base:", Base)
    #print ("Home:", Home)
    #print ("Marbles:", Marbles)

    Setup = 0       # Has the game been setup?
    while not Setup:
        try:
            Setup=1
            NumPlayers = int(input("How many players? "))
            if NumPlayers < 2 or NumPlayers > 6:
                print ("Please enter a number between 2 and 6.")
                Setup=0
        except KeyError:
            print ("Please enter a number between 2 and 6.")
            Setup = 0
        except TypeError:
            print ("Please enter a number between 2 and 6.")
            Setup = 0
        except ValueError:
            print ("Please enter a number between 2 and 6.")
            Setup = 0
    print ("Preparing a %d player game." %NumPlayers)
    if NumPlayers == 2:
        Players.append("blue")
        Players.append("yellow")
    elif NumPlayers == 3:
        Players.append("blue")
        Players.append("cyan")
        Players.append("green")
    elif NumPlayers == 4:
        Players.append("blue")
        Players.append("yellow")
        Players.append("white")
        Players.append("cyan")
    elif NumPlayers == 5:
        Players.append("blue")
        Players.append("yellow")
        Players.append("white")
        Players.append("cyan")
        Players.append("pink")
    else:
        Players.append("blue")
        Players.append("yellow")
        Players.append("white")
        Players.append("cyan")
        Players.append("pink")
        Players.append("green")
    print ("Players = ", Players)
    return NumPlayers

#
# GetMoves (color, die)
#
# Return a list of the valid player options with a die roll
#


# FIXME: Roll 1, dude in Home[0] .. don't offer option of leaving Home

def GetMoves(color,die):
    assert die > 0 and die < 7
    assert color in Colors
    assert color in Players

    # List that we'll be returning with ALL valid moves
    response = []

    # For each marble, figure out all possible moves
    firstStart=1    # Only want to add Start once
    for dude in Marbles[color]:
        # If this marble is in Base, see if it can get out
        if dude == BASE:
            if (die == 1 or die == 6) and (Board[Start[color]]!=color) and (1==firstStart):
                response.append([dude, Start[color]])
                firstStart=0
                continue
                # print ("Can start a dude")
            else:
                # print ("Can't start a dude")
                continue

        #
        # Handle "regular" motion starting here:
        #

        # CENTER SPACE HANDLING

        # If my roll can take me to one past the MagicCircle, then I
        # can enter the Center.  dude+die-1 is equal to MagicCircle+1
        if dude+die-1 in MagicCircle and CenterSpace != color:
            response.append([dude, CENTER])

        # If I'm in the center and I got a one, I can roll out to any
        # magic circle space
        if dude == CENTER:
            if die==1:
                for i in MagicCircle:
                    if Board[i] != color:
                        response.append([dude, i])
            else:
                print ("Stuck in the middle with you...")
            continue
        assert dude != CENTER

        # MAGIC CIRCLE HANDLING

        # If I'm in the magic circle, I can continue normal track, or
        # hop one magic circle space and then continue the normal
        # track, or hope 2 magic circle space and then continue the
        # normal track, or ...
        if dude in MagicCircle:
            # circleNum is the index of where we are in the magic
            # circle list, so we can bop around by adding die values
            # to the index in that list
            circleNum = MagicCircle.index(dude) 

            # Lots of permutations for magic circle...
            for i in range(0, die+1):
                out = MagicCircle[(circleNum+i)%len(MagicCircle)] + (die-i)%BOARDSIZE

                # Now verify that I didn't pass myself between dude
                # and out
                selfPass=0
                for t in range(0,1+die-i):  # t is number of hops out of circle
                    MoveToCheck = (MagicCircle[(circleNum+i)%len(MagicCircle)] + t)%BOARDSIZE
                    if dude == MoveToCheck:
                        continue
                    #print("SELF CHECK: dude=%d die=%d i=%d t=%d MoveToCheck=%d Board[MoveToCheck] = '%s'"
                    #        %(dude,die,i,t,MoveToCheck,Board[MoveToCheck]))
                    if Board[MoveToCheck] == color:
                        # Handle case where I roll a 6 and want to do
                        # a full revolution
                        if dude != MoveToCheck:
                            print ("You can't pass yourself!")
                            selfPass = 1
                            continue

                if not selfPass:
                    # Add this to the list
                    response.append([dude, out])
                    #print ("Magic circle: %d -> %d" %(circleNum, out))

        # MOVEMENT INTO HOME
        elif dude < Start[color] and (dude+die)%BOARDSIZE >= Start[color]: 
            #print ("This might be able to move into Home")
            #print (Home[color])
            passMe = 0
            loc = dude
            for roll in range(1,die+1):
                loc = dude + roll
                #print ("Loc raw:", loc)
                if loc >= Start[color]:
                    loc -= Start[color]
                    #print ("Loc:", loc)
                    if loc >= HOMESIZE:
                        continue
                    if Home[color][loc] == color:
                        #print ("Can't pass your own guy")
                        passMe = 1
                        continue
            if loc>=HOMESIZE and loc == dude+roll:
                response.append([dude, loc])

            if not passMe and loc < 4:
                #print ("Adding dude to Home[%d] = %d" %(loc,HOME+loc))
                response.append([dude, HOME+loc])
                    
        # Special case, since blue start is 0 (modulo problem)
        # Between 78 and 83 are the potentials
        # XXX: Could this code be consolidated with above?
        elif (color=="blue") and (dude >= (Start["white"]+8)) and (dude <= (BOARDSIZE-1)):
            #print ("This might be able to move into Blue Home")
            #print (color, dude, dude-BOARDSIZE, Start[color], dude+die, (dude+die)%BOARDSIZE)
            #print (Home[color])
            passMe = 0
            loc = dude
            for roll in range(1,die+1):
                loc = dude + roll
                #print ("Loc raw:", loc)
                if loc >= BOARDSIZE:
                    loc -= BOARDSIZE
                    #print ("Loc:", loc)
                    if Home[color][loc] == color:
                        #print ("Can't pass your own guy")
                        passMe = 1
            # XXX: Not sure if this is right
            if (loc == dude+roll):
                response.append([dude, loc])

            if not passMe and loc < 4:
                #print ("Adding dude to Home[%s][%d]" %(color,loc))
                response.append([dude, HOME+loc])
                    
        # Movement WITHIN Home
        elif dude >= HOME:
            hm = Home[color]        # hm means Home[color]
            hp = dude-HOME        # hp means Home Position
            valid=1
            #print ("Home Position: %d" %(hp))
            #print (Home[color])
            for i in range(1,die+1):
                if(hp+i >= HOMESIZE):
                    valid=0
                    continue
                #print ("Home Position + %d: %s" %(i,hm[hp+i]))
                if hp+i > HOMESIZE or hm[hp+i] == color:
                    #print("Cannot progress in home")
                    valid=0
                    continue
            if valid:
                response.append([dude, dude+die])

        # "NORMAL" MOVEMENT

        # XXX: For the end game, we'll want to make sure you don't
        # have to keep going around if your roll doesn't take you into
        # home.

        elif Board[(dude+die)%BOARDSIZE] != color: 
            selfPass = 0
            for i in range(1,die):
                if Board[(dude+i)%BOARDSIZE] == color:
                    #print ("You can't pass yourself!")
                    selfPass = 1
                    continue
            if not selfPass:
                response.append([dude, (dude+die)%BOARDSIZE])

    # Done!
    return response


def IsWinner(color):
    win=1
    for i in range(0, HOMESIZE):
        if Home[color][i] != color:
            win=0
            continue
    return bool(win)
#
# main
#
GameOver = 0    # Is the game over

numPlayers = Setup()
#print ("Players = %d" %numPlayers)
#print ("Players = ", Players)
while not GameOver:
    for p in range(0,numPlayers):
        again=1 # Flag for when a player rolls a 6
        while again:
            again=0
            pColor = Players[p]
            #print ("%s's turn" %pColor)
            myRoll = Roll()
            #Display()

            moves = GetMoves(pColor, myRoll)
            #print ("Moves:",moves)

            if not moves:
                print ("\n%s rolled %d" %(pColor, myRoll))
                print ("No moves available. Skipping to next player.")
                continue

            GetInput = 0
            while not GetInput:
                print ("\n%s rolled %d" %(pColor, myRoll))

                option=1    # Counter for the user input menu
                for move in moves:
                    strt, finish = move

                    if finish >= HOME:
                        if strt >= HOME:
                            print("\t[%d] Home[%d] -> Home[%d] #" %(option, strt-HOME, finish-HOME))
                        else:
                            print("\t[%d] %d -> Home[%d] #" %(option, strt, finish-HOME))
                    elif strt == CENTER:
                        print("\t[%d] Center -> %d *" %(option,finish))
                    elif strt == BASE:
                        print ("\t[%d] Base -> Start " %option)
                    else:
                        if finish == CENTER:
                            print ("\t[%d] %d to Center" %(option,strt))
                        elif finish in MagicCircle:
                            print ("\t[%d] %d -> %d *" %(option, strt, finish))
                        else:
                            print ("\t[%d] %d -> %d" %(option, strt, finish))
                    option+=1
                try:
                    selection = int(input(pColor + ": Please select an option: "))
                    GetInput = 1
                    if selection <1 or selection > len(moves):
                        print ("That's not an option. Try again.")
                        GetInput = 0
                except ValueError:
                    print ("Bad input")
                    GetInput = 0
                except TypeError:
                    print ("Bad input")
                    GetInput = 0

            src,dst = moves[selection-1]
            #print (pColor,opt, src,dst)
            Move(pColor, src, dst)
            Display()
            if IsWinner(pColor):
                print ("You win!")
                GameOver = 1

            if myRoll == 6:
                print("%s rolled a 6! Take another turn." %pColor)
                again=1


