# Marbles!
# 
# An implementation of the classic marble board game that can be very
# frustrating!
#
from random import randint

# Notes:
#   ASCII doesn't have an orange, so I'm using Cyan instead. (or
#   purple?)

# GLOBALS
BOARDSIZE = 84  # Number of space around the main track
CENTER=98       # "Location" of the center of death.
BASE=99         # "Location" for base spots.  All are 99.
HOME=100        # "Location" for home spots - 100, 101, 102, 103
HOMESIZE=4      # How big is your home?

Colors = [ "Blue", "Red", "Cyan", "Magenta", "Green", "White" ]
Board = ["" for x in range(0,BOARDSIZE)]
CenterSpace = ""
MagicCircle = [ 7, 21, 35, 49, 63, 77 ]     # Locations for the magic circle spaces
Base = {}       # Dict of each color's base status
Home = {}       # Dict of each color's home status
Marbles = {}    # Dict of each color's marble locations
Players = []    # List of active players

# Marbles[color] : { location0, location1, location2, location3 }
# Start[color] : space#
Start = { 
        "Blue": 0,
        "Red": 14,
        "Cyan": 28,
        "Magenta": 42 ,
        "Green": 56 ,
        "White": 70
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
            #      [magic];Attrib;FG;BGm
            "Blue": "\033[1;97;44m",
            "Red": "\033[1;97;41m",
            "Cyan": "\033[1;97;46m",
            "Magenta": "\033[1;97;45m",
            "Green": "\033[1;35;42m",
            "White": "\033[1;31;47m",
            }

    # ANSI color codes for start
    startColor={
            "Blue": "\033[1;34;40m",
            "Red": "\033[1;31;40m",
            "Cyan": "\033[1;36;40m",
            "Magenta": "\033[1;35;40m",
            "Green": "\033[1;32;40m",
            "White": "\033[1;37;40m",
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
                print (ccode[space]+space[0].lower()+creset, end="")

    # Show the center of death
    if CenterSpace:
        print ("\t",ccode[CenterSpace]+CenterSpace[0].lower()+creset)
    else:
        print ("\t","-")

    print()

    for p in Players:
        if len(Base[p]):
            print ("Base of %s:" %p, end="")
            for b in Base[p]:
                if b != "":
                    print (ccode[b]+b[0].lower()+creset, end="")
            print()

    for p in Players:
        print ("Home of %s:" %p, end="")
        for h in Home[p]:
            if h == "":
                print ("-", end="")
            else:
                print (ccode[h]+h[0].lower()+creset, end="")
        print()

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
        Players.append("Blue")
        Players.append("Magenta")
    elif NumPlayers == 3:
        Players.append("Blue")
        Players.append("Cyan")
        Players.append("Green")
    elif NumPlayers == 4:
        Players.append("Blue")
        Players.append("Magenta")
        Players.append("White")
        Players.append("Cyan")
    elif NumPlayers == 5:
        Players.append("Blue")
        Players.append("Magenta")
        Players.append("White")
        Players.append("Cyan")
        Players.append("Red")
    else:
        Players.append("Blue")
        Players.append("Magenta")
        Players.append("White")
        Players.append("Cyan")
        Players.append("Red")
        Players.append("Green")
    return NumPlayers

#
# Bonk!
#
# send a guy back to base
#
def Bonk(space):
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
    moveDesc = color + ": "

    # Remove marble from source
    if source == CENTER:
        assert CenterSpace == color
        CenterSpace = ""
        moveDesc += "[Center] -> "
    elif source == BASE:
        # Remove the marble from the base
        assert Base[color].count(color) > 0
        Base[color].remove(color)

        # The destination is that color's start
        destination = Start[color]
        moveDesc += "Base -> "
    elif source >= HOME:
        Home[color][source-HOME] = ""
        moveDesc += "[Home[" + str(source-HOME+1) + "] -> "
    else:
        assert Board[source] == color
        Board[source] = ""
        moveDesc += "[" + str(source) + "] -> "

    # Deal with possible destinations
    if destination == CENTER:
        assert CenterSpace != color
        moveDesc += "[Center] "
        if CenterSpace:
            print ("Bonk! %s hits %s!" %(color, CenterSpace))
            moveDesc += "Bonk " + CenterSpace + "!"
            Bonk(CENTER)
        CenterSpace = color
    elif destination >= HOME:
        assert Home[color][destination-HOME] != color
        Home[color][destination-HOME] = color
        moveDesc += "[Home" + str(destination-HOME+1) + "]"
    else:   # Board destination is not the center or Home
        assert Board[destination] != color
        moveDesc += "[" + str(destination) + "] "
        # Deal with bonking if destination is not empty
        if Board[destination]:
            moveDesc += "Bonk " + Board[destination] + "!"
            print ("Bonk! %s hits %s!" %(color,Board[destination]))
            Bonk(destination)
        Board[destination] = color

    Marbles[color].remove(source)
    Marbles[color].append(destination)
    return moveDesc


#
# ValidMove (marble, destination, die)
#
# Check if the move from marble to destination via die is valid
# Returns True / False
#
def ValidMove(marble, destination, die, color):
#    print ("[Entering] ValidMove(src=%d, dest=%d, die=%d, color=%s)" %(marble, destination, die, color))
    assert die > 0 and die < 7
    assert color

    # Quick check to see if there's a teammate at the destination
    if destination < BOARDSIZE:
        if Board[destination] == color and marble != destination and die != 6:
            return False

    # If this marble is in Base, see if it can get out
    if marble == BASE:
        assert destination == Start[color]
        if (die == 1 or die == 6) and (Board[Start[color]]!=color):
            return True
        return False
    assert marble != BASE

    # CENTER SPACE HANDLING
    # If my roll can take me to one past the MagicCircle, then I
    # can enter the Center.  marble+die-1 is equal to MagicCircle+1

    # Entering the Center space
    if destination == CENTER:
        assert marble+die-1 in MagicCircle
        if CenterSpace == color:
            return False

        for i in range(1,die+1):
            if Board[(marble+i)%BOARDSIZE] == color:
                return False
        return True

    # Leaving the Center space
    if marble == CENTER:
        if die==1 and Board[destination] != color:
            return True
        else:
            return False
    assert marble != CENTER
    assert destination != CENTER

    # Special case of 6 in the magic circle ending where you start
    if marble == destination and die == 6 and marble in MagicCircle:
        return True

    # MAGIC CIRCLE HANDLING
    if marble in MagicCircle:
        # magicStart is the index of where we are in the magic
        # circle list, so we can bop around by adding die values
        # to the index in that list
        magicStart = MagicCircle.index(marble) 

        for i in range(0,die+1):
            if destination-i in MagicCircle:
                magicDestination = MagicCircle.index(destination-i)
                # Check all the magic spaces between where I entered
                # and where I exited
                for j in range(magicStart, magicDestination+1):
                    if Board[MagicCircle[j]] == color:
                        if marble == destination and die == 6:
                            return False
                return True
            else: 
                # The destination is not in the magic circle, so walk
                # back to the nearest magic circle space, checking
                # that walk.
                if Board[destination-i] == color:
                    return False
        return True
    assert marble not in MagicCircle

    # MOVEMENT INTO HOME
    myStart = Start[color]
    if myStart == 0:    # I have grown to hate Blue in this game
        myStart = BOARDSIZE
    if marble < myStart and marble+die >= myStart:

        # Test the spaces between here and my final location for
        # teammates
        for i in range(1,die+1):
            testloc = marble+i
            if testloc >= myStart:          # testloc is in the Home zone
                testloc -= myStart          # How many spaces into Home?
                if testloc >= HOMESIZE:     # Ran off the end of Home
                    assert False
                    return False
                elif Home[color][testloc]:  # somebody in the way
                    assert False
                    return False
            else:                           # Still on the main board
                if Board[testloc] == color: # Can't pass teammate
                    assert False
                    return False
            # Checked all intermediate spaces, and destination space

        homeloc = destination - HOME        # homeloc is (potential) home space

        # Move into Home
        if homeloc >= 0 and homeloc < HOMESIZE:
            return True
        assert False
        return False    # Something insane happened?
                
    # Movement WITHIN Home
    if marble >= HOME:
        assert marble < HOME+HOMESIZE
        assert destination >= HOME

        hm = Home[color]        # hm means Home[color]
        hp = marble-HOME        # hp means Home Position
        for i in range(1,die+1):
            if(hp+i >= HOMESIZE):
                return False
            if hp+i > HOMESIZE or hm[hp+i] == color:
                return False
        return True

    # "NORMAL" MOVEMENT
    if marble not in MagicCircle and marble < BOARDSIZE and destination < BOARDSIZE:
        for i in range(1,die):
            if Board[(marble+i)%BOARDSIZE] == color:
                return False
        return True

    # Catch all
    assert False
    return False

#
# SortMoves(myList)
#
# Used by .sorted to return lists in order
def SortMoves(sub_li):
    sub_li.sort(reverse=True,key = lambda x: x[0])
    return sub_li

#
# GetMoves (color, die)
#
# Return a list of the valid player options with a die roll
#
def GetMoves(color,die):
    assert die > 0 and die < 7
    assert color in Colors
    assert color in Players
#    print ("[Entering] GetMoves(color=%s die=%d)" %(color,die))

    # List that we'll be returning with ALL valid moves
    response = []

    # For each marble, figure out all possible moves
    firstStart=1    # Only want to add Start once
    for dude in Marbles[color]:
#        print ("[] GetMoves(color=%s die=%d) - Check %d" %(color,die,dude))
        note =""    # Just in case, clear out any previous note

        # If this marble is in Base, see if it can get out
        if dude == BASE:
            if (die == 1 or die == 6) and (Board[Start[color]]!=color) and (1==firstStart):
                note = "[Start"
                if Board[Start[color]]:
                    note += " & Bonk " + Board[Start[color]]
                note += "]"
                if not ValidMove(dude, Start[color], die, color):
                    assert False
                response.append([dude, Start[color], note])
                firstStart=0
                continue
            else:
                continue

        #
        # Handle "regular" motion starting here:
        #

        # CENTER SPACE HANDLING

        # If my roll can take me to one past the MagicCircle, then I
        # can enter the Center.  dude+die-1 is equal to MagicCircle+1
        if dude+die-1 in MagicCircle and CenterSpace != color:
            yep=1
            for i in range(1,die+1):
                if Board[dude+i] == color:
                    yep=0
            if yep:
                note = "[Center"
                if CenterSpace:
                    note += " & Bonk " + CenterSpace
                note += "]"
                if not ValidMove(dude, CENTER, die, color):
                    assert False
                response.append([dude, CENTER, note])

        # If I'm in the center and I got a one, I can roll out to any
        # magic circle space
        if dude == CENTER:
            if die==1:
                for i in MagicCircle:
                    if Board[i] != color:
                        note = "[Magic Circle"
                        if Board[i]:
                            note += " & Bonk " + Board[i]
                        note += "]"
                        if not ValidMove(dude, i, die, color):
                            assert False
                        response.append([dude, i, note])
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
                circleExit = MagicCircle[(circleNum+i)%len(MagicCircle)]
                finalspot = (circleExit + (die-i))%BOARDSIZE

                # Now verify that I didn't pass a teammate between dude
                # and out
                badMove=0
                circleBlock=0

                # Check magic circle spots I traversed
                for mc in range(1,i+1):
                    if Board[MagicCircle[(circleNum+mc)%len(MagicCircle)]] == color:
                        # Passed through teammate
                        badMove = 1

                # Check regular spots after I left circle
                for t in range(0,die-i+1):  # t is number of hops out of circle
                    MoveToCheck = (circleExit + t)%BOARDSIZE
                    if Board[MoveToCheck] == color:
                        # Handle case where I roll a 6 and want to do
                        # a full revolution
                        if dude != MoveToCheck: 
                            # If it is not me, then it is someone else
                            badMove = 1
                            if t==0:
                                # The magic circle is poisoned from
                                # here on out..
                                circleBlock = 1
                            continue
                if circleBlock:
                    continue

                if not badMove:
                    # Add this to the list
                    # Special processing: If the roll is a 6 in magic
                    # circle, that isn't bonking because it is me.
                    special=0
                    if dude == finalspot:   # End where I started
                        special=1
                    note = ""
                    if (finalspot in MagicCircle) or (Board[finalspot]):
                        note += "["
                    if finalspot in MagicCircle:
                        note += "Magic Circle"
                    if finalspot in MagicCircle and Board[finalspot] and not special:
                        note += " & "
                    if Board[finalspot] and not special:
                        note += "Bonk " + Board[finalspot]
                    if finalspot in MagicCircle or Board[finalspot]:
                        note += "]"
                    if not ValidMove(dude, finalspot, die, color):
                        assert False
                    response.append([dude, finalspot, note])

        # MOVEMENT INTO HOME
        # NB: Add special cases for Blue, with start space of 0,
        # because of modulo problems.
        elif (dude < Start[color] and (dude+die)%BOARDSIZE >= Start[color]) or \
                (Start[color] == 0 and dude < Start[color]+BOARDSIZE and dude+die >= Start[color]+BOARDSIZE):
            badMove = 0
            myStart = Start[color]
            if myStart == 0:        # HACK for Blue with start of 0
                myStart = BOARDSIZE
            for i in range(1,die+1):
                testloc = dude+i
                if not badMove and testloc >= myStart: # testloc is in the Home zone
                    testloc -= myStart          # How many spaces into Home?
                    if testloc >= HOMESIZE:     # Ran off the end of Home
                        badMove = 1
                    elif Home[color][testloc]:    # somebody in the way
                        badMove = 1
                else:                           # Still on the main board
                    if Board[testloc%BOARDSIZE] == color: # Can't pass teammate
                        badMove = 1
            # End of for i in range(1,die)

            if not badMove: # Valid moves only
                loc = dude+die          # loc is destination space
                homeloc = loc - myStart # homeloc is home space

                # Move into Home

                if homeloc >= 0 and homeloc < HOMESIZE:
                    if not ValidMove(dude, HOME+homeloc, die, color):
                        assert False
                    response.append([dude, HOME+homeloc, "[Home]"])

                # Still on the Board
                elif loc < myStart:
                    if Board[loc]:
                        note = "[Bonk " + Board[loc] + "]"
                    if not ValidMove(dude, loc, die, color):
                        assert False
                    response.append([dude, loc, note])
                    
        # Movement WITHIN Home

        elif dude >= HOME:
            hm = Home[color]        # hm means Home[color]
            hp = dude-HOME        # hp means Home Position
            valid=1
            for i in range(1,die+1):
                if(hp+i >= HOMESIZE):
                    valid=0
                    continue
                if hp+i > HOMESIZE or hm[hp+i] == color:
                    valid=0
                    continue
            if valid:
                if not ValidMove(dude, dude+die, die, color):
                    assert False
                response.append([dude, dude+die, "[Home]"])

        # "NORMAL" MOVEMENT

        elif Board[(dude+die)%BOARDSIZE] != color: 
            selfPass = 0
            for i in range(1,die):
                if Board[(dude+i)%BOARDSIZE] == color:
                    selfPass = 1
                    continue
            if not selfPass:
                note = ""
                if (dude+die)%BOARDSIZE in MagicCircle or Board[(dude+die)%BOARDSIZE]:
                    note += "["
                if (dude+die)%BOARDSIZE in MagicCircle:
                    note += "Magic Circle"
                if (dude+die)%BOARDSIZE in MagicCircle and Board[(dude+die)%BOARDSIZE]:
                    note += " & "
                if Board[(dude+die)%BOARDSIZE]:
                    note += "Bonk " + Board[(dude+die)%BOARDSIZE]
                if (dude+die)%BOARDSIZE in MagicCircle or Board[(dude+die)%BOARDSIZE]:
                    note += "]"
                if not ValidMove(dude, (dude+die)%BOARDSIZE, die, color):
                    assert False
                response.append([dude, (dude+die)%BOARDSIZE, note])

    # Done!
#    print ("[Leaving] GetMoves(color=%s die=%d) =" %(color,die),response)
    return SortMoves(response)

#
# IsWinner(color)
#
# Determine if color has won.  Returns True/False
#
def IsWinner(color):
    win=1
    for i in range(0, HOMESIZE):
        if Home[color][i] != color:
            win=0
            continue
    return bool(win)

#
# Main
#
def Main():
    GameOver = 0    # Is the game over

    numPlayers = Setup()
    Display()   # Show the initial game board
    while not GameOver:
        for p in range(0,numPlayers):
            again=1 # Flag for when a player rolls a 6
            while again:
                again=0
                pColor = Players[p]
                myRoll = Roll()

                print ("\n%s rolled: %d\n" %(pColor, myRoll))

                moves = GetMoves(pColor, myRoll)

                if not moves:
                    print ("No moves available.")
                    continue

                GotInput = 0

                if pColor != Colors[0]:
                    if pColor == "Magenta":
                        selection = 1
                    else:
                        selection = randint(1,len(moves))
                    GotInput = 1

                while not GotInput:
                    option=1    # Counter for the user input menu
                    for move in moves:
                        strt, finish, note = move

                        if finish >= HOME:
                            if strt >= HOME:
                                print("\t[%d] Home[%d] -> Home[%d] %s" \
                                        %(option, strt-HOME+1, finish-HOME+1, note))
                            else:
                                print("\t[%d] %d -> Home[%d] %s" %(option, strt, finish-HOME+1, note))
                        elif strt == CENTER:
                            print("\t[%d] Center -> %d %s" %(option,finish,note))
                        elif strt == BASE:
                            print ("\t[%d] Base -> Start %s" %(option,note))
                        else:
                            if finish == CENTER:
                                print ("\t[%d] %d -> Center %s" %(option,strt,note))
                            elif finish in MagicCircle:
                                print ("\t[%d] %d -> %d %s" %(option, strt, finish,note))
                            else:
                                print ("\t[%d] %d -> %d %s" %(option, strt, finish, note))
                        option+=1
                    try:
                        selection = int(input(pColor + ": Please select an option: "))
                        GotInput = 1
                        if selection < 1 or selection > len(moves):
                            print ("That's not an option. Try again.")
                            GotInput = 0
                    except ValueError:
                        if len(moves) == 1:
                            selection = 1
                            GotInput = 1
                        else:
                            print ("Bad input")
                            GotInput = 0
                    except TypeError:
                        print ("Bad input")
                        GotInput = 0

                src,dst,note = moves[selection-1]
                if not ValidMove(src,dst,myRoll,pColor):
                    print ("ERROR: ValidMove(%d, %d, %d, %s)" %(src,dst,myRoll,pColor))
                    return False
                response = Move(pColor, src, dst)
                Display()
                print (response)

                if myRoll == 6:
                    print("%s rolled a 6! Take another turn." %pColor)
                    again=1

                if IsWinner(pColor):
                    print ("%s wins!" %(pColor))
                    GameOver = 1
                    return    # We're out of here!

Main()
