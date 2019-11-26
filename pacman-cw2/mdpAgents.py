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
        # params
        self.direcProb = 0.8
        self.emptyReward = -0.04
        self.discountFactor = 0.5
        self.avoidRadius = 1
        # init util values
        self.foodReward = 1
        self.capsuleReward = 1
        self.ghostReward = -8
        # Init lists
        # FIXED
        self.whole = []
        self.walls = []
        # UPDATED
        self.food = []
        self.capsules = []
        self.ghosts = []
        self.radiusList = []
        

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        # Lists that stay constant throughout program initialised once
        self.walls = api.walls(state)
        self.whole = self.wholeMap(state)
    
    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like the game just ended!"

    # Gets pacman to make a move
    # Updates values of states at every call
    # Calls value iteration after mapping
    # Returns: A direction to move in (with 80% success) 
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Updates new list of entities with new game state
        self.food = api.food(state)
        self.capsules = api.capsules(state)
        self.ghosts = api.ghosts(state)
        self.ghostRadius(state)
        pac = api.whereAmI(state)
        # Updates map with new info e.g. eaten food / capsules / ghosts
        dictMap = self.mapValues(state, self.whole)
        # Converges the mapped values from mapValues
        self.valueIteration(state, dictMap)
        # Makes a move by calling findMax function that returns the best direction to move
        """
        print "Pac: ", pac
        gTimes = api.ghostStatesWithTimes(state)
        for i in gTimes:
            if i[0] in dictMap:
                print i[0], ": ", dictMap[i[0]]
        print "-" * 20
        """
        #print api.legalActions(state)
        #print self.utilityDict
        #print self.findMax(state, pac, dictMap), "\n"
        return api.makeMove(self.findMax(state, pac, dictMap)[0], legal)

    # Returns a list of tuples that are coordinates of the whole map 
    # Called once at init
    def wholeMap(self, state):
        ret = []
        for i in range(self.walls[-1][0] + 1):
            for j in range(self.walls[-1][1] + 1):
                ret.append((i, j))
        return ret

    # Creates a list of all locations within a certain radius of all ghosts
    def ghostRadius(self, state):
        self.radiusList = []
        for ghost in self.ghosts:
            for i in range(int(ghost[0]-self.avoidRadius), int(ghost[0]+self.avoidRadius+1)):
                for j in range(int(ghost[1]-self.avoidRadius), int(ghost[1]+self.avoidRadius+1)):
                    if (i, j) not in self.walls or not ghost: self.radiusList.append((i, j))
        #print self.radiusList

    # Updates the utility values of all the ghosts depending on their states
    def ghostValue(self, state, coord):
        stateTimes = api.ghostStatesWithTimes(state)
        util = 0
        for pair in stateTimes:
            if pair[1] == 0: util = self.ghostReward
            else: util = (pair[1] - 20) / 2.5
        return util

    # Creates a dictionary of coordinate - utility value pairs
    def mapValues(self, state, map1):
        dictMap = {}
        for i in map1:
            if i in self.ghosts: dictMap[i] = self.ghostValue(state, i) # TODO: use ghostValues here
            elif i in self.radiusList: dictMap[i] = self.ghostValue(state, i) / 2
            elif i in self.food: dictMap[i] = self.foodReward
            elif i in self.capsules: dictMap[i] = self.capsuleReward
            elif i in self.walls: dictMap[i] = 0
            else: dictMap[i] = self.emptyReward
        #for j in self.radiusList:
        #    dictMap[j] = self.ghostReward / 2
        return dictMap
    
    # Find adjacent coords of current
    # Returns max util of states using the Bellman equation
    def findMax(self, state, coord, dictMap):
        # Dictionary of utilities in each direction
        self.utilityDict = {Directions.NORTH: 0.0, Directions.SOUTH: 0.0, Directions.EAST: 0.0, Directions.WEST: 0.0}
        # adjacent coords in directions
        self.utilityDict[Directions.NORTH] = self.setUtil(state, Directions.NORTH, coord, dictMap)
        self.utilityDict[Directions.SOUTH] = self.setUtil(state, Directions.SOUTH, coord, dictMap)
        self.utilityDict[Directions.EAST] = self.setUtil(state, Directions.EAST, coord, dictMap)
        self.utilityDict[Directions.WEST] = self.setUtil(state, Directions.WEST, coord, dictMap)

        return max(self.utilityDict.iteritems(), key = lambda x: x[1])
    
    # Called 4 times in findMax, 1 for each direction
    # Sums up the utility of each of the 4 directions by calculating
    # front, left and right probabilities
    def setUtil(self, state, direc, coord, dictMap):
        # Dictionary mapping direction parameter to actual coordinate locations around it
        dirDict = {
            Directions.NORTH: (coord[0], coord[1] + 1), 
            Directions.SOUTH: (coord[0], coord[1] - 1), 
            Directions.EAST: (coord[0] + 1, coord[1]), 
            Directions.WEST: (coord[0] - 1, coord[1]), 
        }

        # If direction (direc) not a wall,
        # multiply direction probability with utility
        # otherwise stay in place (coord)
        if dirDict[direc] not in self.walls:
            util = (self.direcProb * dictMap[dirDict[direc]])
        else:
            util = (self.direcProb * dictMap[coord])
        # LEFT 
        if dirDict[Directions.LEFT[direc]] not in self.walls:
            util += (((1 - self.direcProb)/2) * dictMap[dirDict[Directions.LEFT[direc]]])
        else:
            util += (((1 - self.direcProb)/2) * dictMap[coord])
        # RIGHT
        if dirDict[Directions.RIGHT[direc]] not in self.walls:
            util += (((1 - self.direcProb)/2) * dictMap[dirDict[Directions.RIGHT[direc]]])
        else:
            util += (((1 - self.direcProb)/2) * dictMap[coord])

        return util

    # Converges util values performing Bellman update
    def valueIteration(self, state, dictMap):
        oldMap = None
        while dictMap != oldMap:
            oldMap = dictMap.copy()
            for i in self.whole:
                if i not in self.walls + self.food + self.ghosts + self.capsules:
                    dictMap[i] = self.emptyReward + (self.discountFactor * self.findMax(state, i, oldMap)[1])
        #self.gridPrint(state, dictMap)

    # Prints the map in the terminal with utility values in empty spaces
    def gridPrint(self, state, map):
        out = ""
        for row in reversed(range(self.walls[-1][1]+1)):
            for col in range(self.walls[-1][0]+1):
                if (row == 0 and col == 0): out += "[001]"
                elif (row == 0 and col == 19): out += "[002]"
                elif (row == 10 and col == 0): out += "[003]"
                elif (row == 10 and col == 19): out += "[004]"
                elif (col, row) in self.walls: out += "[###]"
                elif (col, row) in api.ghosts(state): out += "  X  "
                elif (col, row) in api.food(state): out += "  .  "
                elif (col, row) in api.capsules(state): out += "  o  "
                elif (col, row) == api.whereAmI(state): out += "  @  "
                else: out += "{: 5.2f}".format(map[(col, row)])
            out += "\n"
        print out
            
