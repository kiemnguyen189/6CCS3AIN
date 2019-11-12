# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

class MDPAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        # print "Starting up MDPAgent!"
        name = "Pacman"
        self.direcProb = 0.8
        self.emptyReward = -0.04
        self.foodReward = 1
        self.capsuleReward = 1
        self.ghostReward = -1
        self.discountFactor = 1

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        # print "Running registerInitialState for MDPAgent!"
        # print "I'm at:"
        # print api.whereAmI(state)

        map = self.pathMap(state)
        ## print map
        map1 = self.wholeMap(state)
        ## print map1
        dictMap = self.mapValues(state, map1)
        # print "INIT dictMap: ", dictMap
        

    # Returns a dictionary mapping of the whole map
    def wholeMap(self, state):
        walls = api.walls(state)
        last = walls[-1]
        ## print last
        whole = []
        for i in range(last[0]+1):
            for j in range(last[1]+1):
                whole.append((i, j))
        print len(whole)
        return whole
        

    # Find all non-wall spaces
    def pathMap(self, state):
        walls = api.walls(state)
        ## print walls
        finalCell = walls[-1]
        whole = []
        for i in range(finalCell[0]+1):
            for j in range(finalCell[1]+1):
                whole.append((i, j))
        diff = [x for x in whole if x not in set(walls)]
        return diff

    # Creates a dictionary of coordinate - utility value pairs
    # 1 if food
    # -1 if capsule
    # -1 if ghost
    # 0 if wall
    # 0 if empty
    #TODO: replace capsule with ghost when finished
    def mapValues(self, state, map):
        dictMap = {}
        for i in map:
            if i in api.food(state): dictMap[i] = 1
            elif i in api.capsules(state): dictMap[i] = -1
            elif i in api.ghosts(state): dictMap[i] = -1
            elif i in api.walls(state): dictMap[i] = 0
            else: dictMap[i] = 0
        return dictMap

    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like the game just ended!"

    # For now I just move randomly
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        map1 = self.wholeMap(state)
        #map1 = self.pathMap(state)
        ## print map1
        dictMap = self.mapValues(state, map1)
        # print "NEW dictMap: ", dictMap
        self.valueIteration(state, -0.04, 1, dictMap)
        #print sorted(dictMap.iteritems())
        direc = self.getPolicy(self, state, dictMap)
        # Random choice between the legal options.
        print "TEST"
        return api.makeMove(direc, legal)

    
    # find adjacent coords of current
    # returns list of 3 adjacent coords
    def findAdjacent(self, state, coord, dictMap):
        # print "findAdjacent" + "-" * 100
        # print "coord: ", coord
        # print "dictMap: ", dictMap

        walls = api.walls(state)
        # Dictionary of utilities in each direction
        self.utilityDict = {Directions.NORTH: 0.0, Directions.SOUTH: 0.0, Directions.EAST: 0.0, Directions.WEST: 0.0}
        #self.dictMap = dictMap
        #self.coord = coord

        # adjacent coords in directions
        self.utilityDict[Directions.NORTH] = self.setUtil(state, Directions.NORTH, coord, walls, dictMap)
        self.utilityDict[Directions.SOUTH] = self.setUtil(state, Directions.SOUTH, coord, walls, dictMap)
        self.utilityDict[Directions.EAST] = self.setUtil(state, Directions.EAST, coord, walls, dictMap)
        self.utilityDict[Directions.WEST] = self.setUtil(state, Directions.WEST, coord, walls, dictMap)

        dictMap[coord] = max(self.utilityDict.values())

        # print self.utilityDict
        return dictMap[coord]
    
    # Called 4 times, 1 for each direction
    def setUtil(self, state, direc, coord, walls, dictMap):
        # print "setUtil" + "-" * 100
        # print "direc: ", direc
        # print "coord: ", coord
        ## print "walls: ", walls
        # print "dictMap: ", dictMap

        current = (coord[0], coord[1])
        north = (coord[0], coord[1] + 1)
        south = (coord[0], coord[1] - 1)
        east = (coord[0] + 1, coord[1])
        west = (coord[0] - 1, coord[1])

        dirDict = {Directions.NORTH: north, Directions.SOUTH: south, Directions.EAST: east, Directions.WEST: west}

        #util = 0.0

        # If direction (direc) not a wall,
        # multiply direction Prob with utility
        # otherwise stay in place (current)
        if dictMap[dirDict[direc]] not in walls:
            # print "if 1: ", dictMap[dirDict[direc]]
            util = (self.direcProb * dictMap[dirDict[direc]])
            # print "if util 1: ", util
        else:
            # print "else 1: ", dictMap[dirDict[current]]
            util = (self.direcProb * dictMap[dirDict[current]])
            # print "else util 1: ", util

        # LEFT 
        if dictMap[dirDict[Directions.LEFT[direc]]] not in walls:
            # print "if 2: ", dictMap[dirDict[Directions.LEFT[direc]]]
            util += (((1 - self.direcProb)/2) * dictMap[dirDict[Directions.LEFT[direc]]])
            # print "util 2: ", util
        else:
            # print "else 2: ", dictMap[dirDict[current]]
            util += (((1 - self.direcProb)/2) * dictMap[dirDict[current]])
            # print "else util 1: ", util

        # RIGHT
        if dictMap[dirDict[Directions.RIGHT[direc]]] not in walls:
            # print "if 3: ", dictMap[dirDict[Directions.RIGHT[direc]]]
            util += (((1 - self.direcProb)/2) * dictMap[dirDict[Directions.LEFT[direc]]])
            # print "util 3: ", util
        else:
            # print "else 3: ", dictMap[dirDict[current]]
            util += (((1 - self.direcProb)/2) * dictMap[dirDict[current]])
            # print "else util 3: ", util

        return util

    #
    def valueIteration(self, state, reward, discount, dictMap):
        pacman = api.whereAmI(state)
        ghosts = api.ghosts(state)
        food = api.food(state)
        capsules = api.capsules(state)
        walls = api.walls(state)
        last = walls[-1]

        oldMap = None
        while dictMap != oldMap:
            oldMap = dictMap.copy()
            for i in self.wholeMap(state):
                if i not in walls + food + ghosts + capsules:
                    # print i, "FUCKFUCKFUCKFUCK"
                    dictMap[i] = reward + (discount * self.findAdjacent(state, i, oldMap))
                    """
                    tempDict1 = {}
                    tempDict2 = {}
                    for i, j in oldMap:
                        if i not in walls:
                            tempDict1[i] = j
                    for i, j in dictMap:
                        if i not in walls:
                            tempDict2[i] = j
                    print "OLD: ", sorted(tempDict1.iteritems())
                    print "NEW: ", sorted(tempDict2.iteritems())
                    """
                    print "OLD: ", sorted(oldMap.iteritems())
                    print "NEW: ", sorted(dictMap.iteritems())

    #TODO: POSSIBLE to create:
    #TODO: Instead of dictionary with key: coords and value: util, can create
    #TODO: list of 3-item lists. Outer list = the whole map
    #TODO: each inner list has 3 items: 1) coord 2) utility 3) optimum policy direction
    # Utility = map with utils in each state
    # Policy = map with directions in each state

    # Finds the best direction to move based on the surrounding utilities
    # Returns a direction
    def getPolicy(self, state, dictMap):
        pacman = api.whereAmI(state)
        walls = api.walls(state)

        x = pacman[0]
        y = pacman[1]
        coord = (x, y)

        self.utilityDict = {Directions.NORTH: 0.0, Directions.SOUTH: 0.0, Directions.EAST: 0.0, Directions.WEST: 0.0}
        self.returnDirec = {}

        self.utilityDict[Directions.NORTH] = self.setUtil(state, Directions.NORTH, coord, walls, dictMap)
        self.utilityDict[Directions.SOUTH] = self.setUtil(state, Directions.SOUTH, coord, walls, dictMap)
        self.utilityDict[Directions.EAST] = self.setUtil(state, Directions.EAST, coord, walls, dictMap)
        self.utilityDict[Directions.WEST] = self.setUtil(state, Directions.WEST, coord, walls, dictMap)

        #direc = None
        """
        high = max(self.utilityDict.values())
        for dir, util in self.utilityDict:
            if util == high:
                direc = dir
        """

        return max(self.utilityDict)
