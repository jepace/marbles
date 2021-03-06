# Marbles!
# 
# An implementation of the classic marble board game that can be very
# frustrating!
#
from random import randint
#import tkinter

# GLOBALS
BOARDSIZE = 84  # Number of space around the main track
CENTER=98       # "Location" of the center of death.
BASE=99         # "Location" for base spots.  All are 99.
HOME=100        # "Location" for home spots - 100, 101, 102, 103
HOMESIZE=4      # How big is your home?

Colors = [ "Blue", "Red", "Cyan", "Purple", "Green", "White" ]
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
        "Purple": 42,
        "Green": 56,
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
            "Purple": "\033[1;97;45m",
            "Green": "\033[1;35;42m",
            "White": "\033[1;31;47m",
            }

    # ANSI color codes for start
    startColor={
            "Blue": "\033[1;34;40m",
            "Red": "\033[1;31;40m",
            "Cyan": "\033[1;36;40m",
            "Purple": "\033[1;35;40m",
            "Green": "\033[1;32;40m",
            "White": "\033[1;37;40m",
            }

    # Reset the color to default
    creset="\033[m"

    output = ["-" for x in range(0,BOARDSIZE)]
    for i in range(0,BOARDSIZE):
        space = Board[i]
        if space == "":
            # Use a * to indicate magic circle
            if i in MagicCircle:
                #output[i] = "*"
                #print ("*", end="")
                output[i] = chr(0x00A4) # cool circle thing
            # Use a # to indicate start spaces
            elif i in Start.values():
                # What's this? I need to get the color given the
                # value.  So here's a bunch of casting black magic to
                # do that.
                thiscolor = list(Start.keys())[list(Start.values()).index(i)]
                #output[i] = startColor[thiscolor]+"#"+creset
                output[i] = startColor[thiscolor]+chr(0x00BB)+creset
                output[i] = startColor[thiscolor]+chr(0x033F)+creset
                #print (startColor[thiscolor]+"#"+creset, end="")
            elif i % 10 == 0:
                output[i] = str(i // 10)
            else:
                #output[i] = ("-")
                output[i] = chr(0x00B7) # A nice dot
                #print ("-", end="")

        # Occupied space
        else:
            # If you're on the magic circle, you get an upper case
            # letter
            if i in MagicCircle:
                output[i] = ccode[space]+space[0].upper()+creset
                #print (ccode[space]+space[0].upper()+creset, end="")
            else:
                output[i] = ccode[space]+space[0].lower()+creset
                #print (ccode[space]+space[0].lower()+creset, end="")

    for i in range(0,BOARDSIZE):
        if i >=0 and i < 21:
            if i == 0: print ("\t", end="")
            print(output[i], end="")
            if i == 20:
                print()
        elif i >= 21 and i < 42:
            if i == 31:
                if CenterSpace:
                    cen = ccode[CenterSpace]+CenterSpace[0].upper()+creset
                else:
                    #cen = "-"
                    #cen = chr(216)
                    cen = chr(0x00A7)    # Hurricane
                print("\t%s\t  %s\t    %s" %(output[104-i],cen,output[i]))
            else:
                print("\t"+output[104-i],"\t\t   ",output[i])
        elif i >= 42 and i < 63:
            if i == 42: print ("\t", end="")
            print (output[104-i], end="")   # Print it backwards
    print("\n")

    for p in Players:
        print ("%s\t" %p, end="")
        print ("Base:\t", end="")
        for b in Base[p]:
            if b == "":
                #print ("-", end="")
                print (chr(0x00B7), end="")
            else:
                print (ccode[b]+b[0].lower()+creset, end="")

        print ("\tHome:\t", end="")
        for h in Home[p]:
            if h == "":
                #print ("-", end="")
                print (chr(0x00B7), end="")
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
        # Where are my marbles? All your base are belong to us.
        Marbles[c] = [BASE, BASE, BASE, BASE ]      

    robotMode = 0
    Setup = 0       # Has the game been setup?
    while not Setup:
        try:
            Setup=1
            NumPlayers = int(input("How many players? "))
            if NumPlayers == 0:
                print ("The only way to win is not to play.")
                NumPlayers = -6
                robotMode = 1
            elif NumPlayers >= -6 and NumPlayers <= -2:
                print ("Like tears in rain.")
                robotMode = 1
            elif NumPlayers < 2 or NumPlayers > 6:
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
    if NumPlayers == 2 or NumPlayers == -2:
        Players.append("Blue")
        Players.append("Purple")
    elif NumPlayers == 3 or NumPlayers == -3:
        Players.append("Blue")
        Players.append("Cyan")
        Players.append("Green")
    elif NumPlayers == 4 or NumPlayers == -4:
        Players.append("Blue")
        Players.append("Purple")
        Players.append("White")
        Players.append("Cyan")
    elif NumPlayers == 5 or NumPlayers == -5:
        Players.append("Blue")
        Players.append("Purple")
        Players.append("White")
        Players.append("Cyan")
        Players.append("Red")
    else:
        Players.append("Blue")
        Players.append("Purple")
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
        moveDesc += "[Base] -> "
    elif source >= HOME:
        Home[color][source-HOME] = ""
        moveDesc += "Home[" + str(source-HOME+1) + "] -> "
    else:
        assert Board[source] == color
        Board[source] = ""
        moveDesc += "" + str(source) + " -> "

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
        moveDesc += "Home[" + str(destination-HOME+1) + "]"
    else:   # Board destination is not the center or Home
        assert Board[destination] != color
        moveDesc += "" + str(destination) + " "
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
# This is pretty much a duplicate of GetMoves() but it serves as a
# check because I was having problems. :)  I should probably remove
# most of thie duplicate logic from GetMoves and have it here only.
# But, you know, this is working.
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
                    return False
                elif Home[color][testloc]:  # somebody in the way
                    return False
            else:                           # Still on the main board
                if Board[testloc] == color: # Can't pass teammate
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
    sub_li.sort(key = lambda x: x[3])
    #sub_li.sort(reverse=True,key = lambda x: x[0])
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
                response.append([dude, Start[color], note, BOARDSIZE])
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
                distance = BOARDSIZE - 8
                response.append([dude, CENTER, note, distance])

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
                        distance = BOARDSIZE - (i - Start[color]) % BOARDSIZE
                        response.append([dude, i, note, distance])
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
                        # 6 in magic circle means I can land on myself
                        if mc == 6:
                            pass
                        else:
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
                    distance = BOARDSIZE - (finalspot - Start[color]) % BOARDSIZE
                    response.append([dude, finalspot, note, distance])

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
                    response.append([dude, HOME+homeloc, "[Home]", 0])

                # Still on the Board
                elif loc < myStart:
                    if Board[loc]:
                        note = "[Bonk " + Board[loc] + "]"
                    if not ValidMove(dude, loc, die, color):
                        assert False
                    distance = BOARDSIZE - (loc - Start[color]) % BOARDSIZE
                    response.append([dude, loc, note, distance])
                    
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
                response.append([dude, dude+die, "[Home]", 0])

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
                distance = BOARDSIZE - ((dude+die)%BOARDSIZE - Start[color]) % BOARDSIZE
                response.append([dude, (dude+die)%BOARDSIZE, note, distance])

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
            break
    return bool(win)


def TkSetup():
    root = tkinter.Tk()
    root.title("Marbles!")
    canvas = tk.Canvas(root, width=200, height=200, borderwidth=0,
            bg="black")
    canvas.grid()
    canvas.create_oval(100,100,200,200,fill="blue",outline="#DDD",width=4)
    root.mainloop()

#
# Main
#
def Main():
    GameOver = 0    # Is the game over
    turnNum = 0
    robotMode = 0       # A human is needed

    numPlayers = Setup()
    if numPlayers <= 0:
        robotMode = 1
        numPlayers *= -1

#    TkSetup()
    Display()   # Show the initial game board
    while not GameOver:     # Main game loop
        turnNum += 1
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
                selection = 0

                # Red always goes for the kill
                # White tried to be optimal, but sucked so now takes 1
                # Cyan takes option 1
                # Purple kills
                # Green picks randomly from choices
                # Blue is the player .. or she chooses 1

                # Deckard is a replicant!
                if robotMode and pColor == "Blue":
                    selection = 1
                    GotInput = 1

                if pColor == "Red" or pColor == "Purple":      # Blood shall flow
                    GotInput = 1
                    for i in range(0,len(moves)):
                        if "Bonk" in moves[i][2]:
                            selection = i+1
                            print ("Kill!", moves[i])
                            break
                    if not selection:
                        selection = 1
                elif pColor == "Cyan" or pColor == "Purple" or pColor == "White":
                    # Always take the first option
                    selection = 1
                    GotInput = 1
                elif pColor == "Green":
                    # Take a random option
                    selection = randint(1,len(moves))
                    GotInput = 1

                while not GotInput:
                    option=1    # Counter for the user input menu
                    for move in moves:
                        strt, finish, note, distance = move

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

                src,dst,note,distance = moves[selection-1]
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
                    print ("%s wins in %d turns!" %(pColor, turnNum))
                    GameOver = 1
                    return    # We're out of here!

Main()
