import math
import sys
import timeit
import csv
import os # testing purposes

class game:
    def __init__(self):
        self.state = [ ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '', ''] ]

        self.debug = False


    def testColumn(self, column):
        # Set to see if 1: Not Complete or 2: Reused Number
        # 3: All numbers 1-9 used
        tempSet = set()
        for i in range(0,9):
            spot = self.state[i][column-1]
            if spot == '':
                if self.debug: print("Error: Column not Filled Out")
                return False
            if int(spot) in tempSet:
                self.debug: print("Column Error")
                return False
            else:
                tempSet.add(int(spot))
        checkNumSet = set(range(1, 10))
        for k in range(1, 10):
            if not k in checkNumSet:
                if self.debug: print("Column Error: not all numbers")
                return False
        return True

    def testRow(self, row):
        # Same as testColumn but for rows
        tempSet = set()
        for i in range(0, 9):
            spot =self.state[row-1][i]
            if spot == '':
                if self.debug: print("Error: Row not Filled Out")
                return False
            if int(spot) in tempSet:
                if self.debug: print("Row Error")
                return False
            else:
                tempSet.add(int(spot))
        checkNumSet = set(range(1,10))
        for k in range(1,10):
            if not k in checkNumSet:
                if self.debug: print("Row Error: not all numbers")
                return False
        return True

    def validSquares(self):
        # This is for the subsquares, but who follow the same logic of not repeating, not empty, used all 1-9
        for i in range(0,3): # supersquare row
            for j in range(0,3): # supersquare column
                usedNums = set()
                for k in range(0,3): # subsquare row
                    for n in range(0,3): # subsquare column
                        r = i*3 + k
                        c = j*3 + n
                        spot = self.state[r][c]
                        if spot == '':
                            if self.debug: print("Subsquare not full")
                            return False
                        if(int(spot)) in usedNums:
                            if self.debug: print("Resued Number in Square")
                            return False
                        usedNums.add(int(spot))
                for x in range(1,10):
                    if x not in usedNums:
                        if self.debug: print("Not all numbers used in square")
                        return False
        return True

    def testWinner(self):
        #test rows
        for i in range(1,10):
            if not self.testRow(i):
                return False
        #test columns
        for i in range(1,10):
            if not self.testColumn(i):
                return False
        #test squares
        if not self.validSquares():
            return False
        return True

    def place(self, r, c, num):
        # places at row anc column (1-9) as numbers that are converted to 0-index
        self.state[r-1][c-1] = str(num)
        return self

    def check3Square(self, r, c, num):
        # similar to valid squares but seeing what's in square actively
        # returns false if number already inside
        # Converts to square start 0-2=0, 3-5=3, 6-8=6
        sRow = (r-1) - ((r-1)%3)
        sCol = (c-1) - ((c-1)%3)
        tempSet = set()
        for i in range(sRow,sRow+3):
            for j in range(sCol,sCol+3):
                spot = self.state[i][j]
                if spot != '':
                    if(num in tempSet):
                        print("Error: Already in Square")
                        return False
                    tempSet.add(int(spot))
        return True # number not already in respective square

    def LegalMovesget(self, r, c):
        # return possible moves in place
        # start with full set, remove as you go
        fullSet = set(range(1,10))

        # check column for existing numbers
        for i in range(0,9):
            spot = self.state[i][c - 1]
            if spot != '':
                if int(spot) in fullSet:
                    fullSet.remove(int(spot))

        # check row for existing numbers
        for i in range(0,9):
            spot = self.state[r-1][i]
            if spot != '':
                if int(spot) in fullSet:
                    fullSet.remove(int(spot))

        # check squares for existing numbers
        sRow = (r - 1) - ((r - 1) % 3)
        sCol = (c - 1) - ((c - 1) % 3)
        for i in range(sRow, sRow + 3):
            for j in range(sCol, sCol + 3):
                spot = self.state[i][j]
                if spot != '':
                    if int(spot) in fullSet:
                        fullSet.remove(int(spot))

        return fullSet

    def carefulPlace(self, r, c, num):
        # same as place, but a lot more careful, reports errors more
        attemptedMove = "R:" + str(r) + " C:" + str(c) + " N:" + str(num)  # add str to avoid actually combining the numbers
        if self.state[r-1][c-1] != '':
            print("Error: Overiding non Empty Square, " + attemptedMove)
        elif num not in self.LegalMovesget(r,c):
            print("Error: Placing Illegal Num, " + attemptedMove)
        else:
            self.state[r-1][c-1] = str(num)
        return self

    def tryFull(self):
        # alternative to tryWinner that also tests if every spot is filled out
        self.testWinner()
        # unused, as only test winner when full

    def display(self):
        # d is the var for the final display
        d = ''
        for i in range(0, 9): # rows
            for j in range(0,9): # columns
                # setup add in normal cases
                add = self.state[i][j]
                if add == '': add = '  '
                else: add = ' ' + add

                # edge of square cases
                if j%3 == 2 and j < 8: add += " | "
                if j == 8:
                    add += "\n"
                    if i % 3 == 2 and i < 8: add += "--------------------------- \n"
                d += add
        print(d)

    def copy(self):
        # copies a game since normally only shallow copy
        newGame = game()
        newState = []
        for i in range(0, 9):
            newState.append(self.state[i].copy())
        newGame.state = newState
        return newGame


class gameHandler:
    def __init__(self, fileName, modeInput):
        # set up, takes file to be used and mode of program
        # domain list is key to everything, contains domain for variables
        # creates a list of lists of sets, where coordinates line up
        self.domainList = []
        for i in range(0,9):
            subListRow = []
            for j in range(0,9):
                subListRow.append(set())
            self.domainList.append((subListRow))
        self.file = fileName

        self.debug = False
        self.mode = modeInput

        # track number of nodes
        self.numNodes = 0
        self.savedSolution = None

        self.setDomains()

    def setDomains(self):
        # Initializes the domain based on the file given
        # X is all while specified is just self
        searchText = readFile(self.file) # don't have to worry about new lines
        for i in range(0,81):
            c = i % 9
            r = math.floor(i / 9)
            spot = searchText[(i*2)]
            # print(r,c)
            # print(searchText)
            if spot == 'X':
                self.domainList[r][c] = set(range(1,10))
            else:
                self.domainList[r][c].add(int(spot))
        # if self.debug: self.printDomains()

    def printDomains(self):
        # for debugging, check domains of each coordinate
        for i in range(0,9):
            for j in range(0,9):
                print("r: " + str(i + 1) + " c:" + str(j + 1) + " = " + str(self.domainList[i][j]))

    def getIndex(self, num):
        # return a tuple with the coordinates for the number position, valid 1-81, will be 0-indexed
        if num < 1 or num > 81: print("Index Error: Range gone back: " + str(num))
        r = math.floor((num-1) / 9)
        c = ((num-1) % 9)
        return (r,c)

    def bruteForce(self):
        # root of tree is the first, keep in mind that it has all 80 other squares
        self.numNodes += len(self.domainList[0][0])
        for x in self.domainList[0][0]:
            gameTracker = game()
            gameTracker.place(1,1,x)
            self.bruteForceInner(2, gameTracker)


    def bruteForceInner(self, n, gameState):
        i = self.getIndex(n)
        r=i[0]
        c=i[1]
        # if self.debug: print(n)
        self.numNodes += len(self.domainList[r][c])
        for x in self.domainList[r][c]:
            gameTracker = gameState.copy()
            gameTracker.place(r+1, c+1, x)
            # gameTracker.display()
            # os.system("cls")
            # if n == 81: gameTracker.display()
            if n == 81: # game is full
                # gameTracker.display()
                if gameTracker.testWinner():
                    self.savedSolution = gameTracker
            else:
                self.bruteForceInner(n+1, gameTracker)

    def backTrack(self):
        # backtrack method checks if errors exist in current state
        self.numNodes += len(self.domainList[0][0])
        for x in self.domainList[0][0]:
            # no need to check legal moves here, since not filled yet
            gameTracker = game()
            gameTracker.place(1, 1, x)
            self.backTrackInner(2, gameTracker)

    def backTrackInner(self, n, gameState: game):
        # Inside for recursion
        i = self.getIndex(n)
        r = i[0]
        c = i[1]
        self.numNodes += len(self.domainList[r][c])
        if self.debug: print(n)
        possibleMoves = gameState.LegalMovesget(r + 1,c + 1)
        for x in self.domainList[r][c]:
            if x in possibleMoves: # backtracking, if x fails (illegal sudoku placement), go back to parent, which will then use sibling
                gameTracker = gameState.copy()
                gameTracker.place(r + 1, c + 1, x)
                if n == 81:  # game is full
                    if gameTracker.testWinner():
                        self.savedSolution = gameTracker
                else:
                    self.backTrackInner(n + 1, gameTracker)
            # not in legal moves = backtrack

    def forwardAndMRV(self):
        # Forward Checking and MRV method
        variables = set(range(1,82))
        # Grabbing the Minimum Remaining Variable
        nextVar = self.getMRV(self.domainList, variables)
        index = self.getIndex(nextVar)
        r = index[0]
        c = index[1]
        # Removing so not repeated in variable list
        variables.remove(nextVar)
        self.numNodes += len(self.domainList[r][c])
        for x in self.domainList[r][c]:
            gameTracker = game()
            gameTracker.place(r+1,c+1,x)
            if len(variables) == 0:
                if gameTracker.testWinner():
                    return gameTracker
            domains = self.copyDomainList(self.domainList)
            if self.updateDomains(domains, nextVar, x):
                self.forwardAndMRVInner(domains, variables, gameTracker)

    def forwardAndMRVInner(self, domainSets, variables, gameArg):
        varList = variables.copy()
        nextVar = self.getMRV(domainSets, variables)
        index = self.getIndex(nextVar)
        r = index[0]
        c = index[1]
        # print(nextVar)
        # print(varList)
        varList.remove(nextVar)
        self.numNodes += len(self.domainList[r][c])
        for x in domainSets[r][c]:
            gameTracker = gameArg.copy()
            gameTracker.place(r+1, c+1, x)
            if len(varList) == 0:
                if gameTracker.testWinner():
                    self.savedSolution = gameTracker
            else:
                domainList = self.copyDomainList(domainSets)
                # This is the forward checking. It will check if any domain's length is 0 (no domain)
                # if so, then no point in continuing on tree path as you will eventually come across error
                if self.updateDomains(domainList, nextVar, x):
                    self.forwardAndMRVInner(domainList, varList, gameTracker)

    def getMRV(self, domainSets, variableList):
        # get minimum remaining values variable
        min = 11  # highest number would be 11, so this is
        minRemaining = -1  # The minimum remaining values (mrv) variable
        for x in variableList:
            ind = self.getIndex(x)  # get the index for domain list of variable
            r = ind[0]
            c = ind[1]
            remainingValues = len(domainSets[r][c])
            if self.debug:
                if remainingValues == 0: print("Overlooked Error: get MRV 0")
            if remainingValues < min:
                min = remainingValues
                minRemaining = x
        return minRemaining

    def copyDomainList(self, domains):
        # Deep copy of domain list for passing down
        newList = []
        # print(domains)
        for i in range(0,9):
            innerList = []
            # print(domains[i])
            for j in range(0,9):
                #print(domains[i][j])
                innerList.append(domains[i][j].copy())
            newList.append(innerList)
        # print(newList)
        return newList

    def updateDomains(self, domains, n, placeNum):
        # returns true if no domains made 0 and false if domain made 0 (foward checking)
        ind = self.getIndex(n)
        r = ind[0]
        c = ind[1]
        domains[r][c] = {placeNum}  # update domain list given
        # shared row (go through columns)
        for j in range(0,9):
            if j != c:
                domains[r][j].discard(placeNum)  # use discard because no error if not in set
                if len(domains[r][j]) < 1:
                    if self.debug: print("Domain Made 0, forward-checked, row")
                    return False

        # shared column (go through rows)
        for i in range(0,9):
            if i != r:
                domains[i][c].discard(placeNum)
                if len(domains[i][c]) < 1:
                    if self.debug: print("Domain Made 0, forward-checked, col")
                    return False

        # update subsquare
        BigsquareR = math.floor(r/3)
        BigsquareC = math.floor(c/3)
        for i in range(BigsquareR*3, BigsquareR + 3):
            for j in range(BigsquareC*3, BigsquareC + 3):
                if not (i == r and j == c):
                    domains[i][j].discard(placeNum)
                    if len(domains[i][j]) < 1:
                        # print(i, j)
                        if self.debug: print("Domain Made 0, forward-checked, sqr")
                        return False
        return True  # no domains set to 0

    def fileToGameTest(self):
        # test solution if is mode 4, number of nodes should be 0 for this, same with time
        testGame = game()
        searchText = readFile(self.file)
        for i in range(0, 81):
            c = (i % 9) + 1
            r = (math.floor(i / 9)) + 1
            spot = searchText[(i * 2)]
            if spot == 'X':
                return False
            else:
                testGame.place(r,c,int(spot))
        return testGame.testWinner()

    def search(self):
        if self.mode == 1: return self.bruteForce()
        if self.mode == 2: return self.backTrack()
        if self.mode == 3: return self.forwardAndMRV()
        if self.mode == 4:
            print("Testing Solution... \n")
            print("Number of tree nodes generated: 0")
            print("Search time: 0 seconds \n")
            if self.fileToGameTest():
                print("This is a valid, solved, Sudoku puzzle")
            else:
                print("Error: This is NOT a solved Sudoku puzzle")


    def exec(self):
        algoName = "NoNameInput"
        if self.mode == 1: algoName = "Brute Force"
        elif self.mode == 2: algoName = "Back-tracking"
        elif self.mode == 3: algoName = "Forward-Checking & MRV"
        elif self.mode == 4: algoName = "Test Solution"
        print("Diaz, Daniel, A20480127 solution:")
        print("Input File: " + self.file)
        print("Algorithm: " + algoName + "\n")
        print("Input Puzzle: \n" + readFile(self.file))
        print("Beginning Search...")
        timeStart = timeit.default_timer()
        self.search()
        solutionGame = self.savedSolution
        timeEnd = timeit.default_timer()
        timeElapsed = timeEnd - timeStart
        if self.mode != 4:
            print("Number of search tree Nodes Generated: " + str(self.numNodes))
            print("Search Time: " + str(timeElapsed) + " seconds \n")
        if self.savedSolution is not None:
            print("Solved Puzzle: " + "\n")
            print(self.altDisplay(solutionGame))
            gameToFile(self.file, solutionGame)
        else:
            if self.mode != 4:
                print("No Solution Found")

    def altDisplay(self, gameToShow):
        # This is the display but in the form that the .csv files are writen
        representation = ''  # string representation to be written
        for i in range(0, 9):  # rows
            for j in range(0, 9):  # columns
                # setup add in normal cases
                add = gameToShow.state[i][j]
                if add == '':
                    add = 'X'
                if not (j == 8):  # When the line file is ending, do not add new comma
                    add += ','
                else:
                    add += '\n'
                representation += add
        return representation


def gameToFile(fileName, gameInput):
    # create new file
    solName = fileName[:-4] + "_solution.csv"
    output = open(solName, 'w')
    representation = ''  # string representation to be written
    for i in range(0, 9):  # rows
        for j in range(0, 9):  # columns
            # setup add in normal cases
            add = gameInput.state[i][j]
            if add == '':
                add = 'X'
            if not (j == 8):  # When the line file is ending, do not add new comma
                add += ','
            else:
                add += '\n'
            representation += add
    output.write(representation)
    output.close()

def readFile(fileName):
    # Turn the file into string in program
    # check for errors in case file doesn't exist
    try:
        file = open(fileName)
    except:
        # print("ERROR: Not enough/too many/illegal input arguments.")
        exit()
    fileText = file.read()
    # Debug: print(fileText)
    return fileText


# Actual Start of the program
# Handle command line arguments
try:
    mode = sys.argv[1]
    fileArg = sys.argv[2]
except:
    pass

# Checking validity of mode
try:
    mode = int(mode)
    if 0 < mode < 5:
        system = gameHandler(fileArg, int(mode))
        system.exec()
    else:
        print("ERROR: Not enough/too many/illegal input arguments.")
except:
    print("ERROR: Not enough/too many/illegal input arguments.")




