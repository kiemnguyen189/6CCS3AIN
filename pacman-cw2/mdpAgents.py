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
        # params
        self.direcProb = 0.8
        self.emptyReward = -0.04
        self.discountFactor = 1
        # init util values
        self.foodReward = 1
        self.capsuleReward = 1
        self.ghostReward = -1
        # init lists
        self.whole = []
        self.walls = []
        self.food = []
        self.capsules = []
        self.ghosts = []
        

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        # print "Running registerInitialState for MDPAgent!"
        # print "I'm at:"
        # print api.whereAmI(state)
        self.walls = api.walls(state)
        self.whole = self.wholeMap(state)
        
    # Returns a list of the whole map
    def wholeMap(self, state):
        last = self.walls[-1]
        ret = []
        for i in range(last[0]+1):
            for j in range(last[1]+1):
                ret.append((i, j))
        return ret

    # Creates a dictionary of coordinate - utility value pairs
    def mapValues(self, state, map):
        dictMap = {}
        for i in map:
            if i in api.food(state): dictMap[i] = self.foodReward
            elif i in api.capsules(state): dictMap[i] = self.capsuleReward
            elif i in api.ghosts(state): dictMap[i] = self.ghostReward
            elif i in self.walls: dictMap[i] = 0
            else: dictMap[i] = 0
        return dictMap

    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like the game just ended!"

    # MDP 
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Updates new list of entities
        self.food = api.food(state)
        self.capsules = api.capsules(state)
        self.ghosts = api.ghosts(state)
        pac = api.whereAmI(state)
        # Updates map with new info e.g. eaten food / capsules / ghosts
        dictMap = self.mapValues(state, self.whole)
        self.valueIteration(state, self.emptyReward, self.discountFactor, dictMap)
        return api.makeMove(self.findMax(state, pac, dictMap)[0], legal)
    
    # Find adjacent coords of current
    # Returns max util of states
    def findMax(self, state, coord, dictMap):

        # Dictionary of utilities in each direction
        utilityDict = {Directions.NORTH: 0.0, Directions.SOUTH: 0.0, Directions.EAST: 0.0, Directions.WEST: 0.0}

        # adjacent coords in directions
        utilityDict[Directions.NORTH] = self.setUtil(state, Directions.NORTH, coord, dictMap)
        utilityDict[Directions.SOUTH] = self.setUtil(state, Directions.SOUTH, coord, dictMap)
        utilityDict[Directions.EAST] = self.setUtil(state, Directions.EAST, coord, dictMap)
        utilityDict[Directions.WEST] = self.setUtil(state, Directions.WEST, coord, dictMap)

        return max(utilityDict.iteritems(), key = lambda x: x[1])
    
    # Called 4 times, 1 for each direction
    def setUtil(self, state, direc, coord, dictMap):
        
        current = (coord[0], coord[1])
        north = (coord[0], coord[1] + 1)
        south = (coord[0], coord[1] - 1)
        east = (coord[0] + 1, coord[1])
        west = (coord[0] - 1, coord[1])

        dirDict = {Directions.NORTH: north, Directions.SOUTH: south, Directions.EAST: east, Directions.WEST: west}

        # If direction (direc) not a wall,
        # multiply direction Prob with utility
        # otherwise stay in place (current)
        if dirDict[direc] not in self.walls:
            util = (self.direcProb * dictMap[dirDict[direc]])
        else:
            util = (self.direcProb * dictMap[current])
        # LEFT 
        if dirDict[Directions.LEFT[direc]] not in self.walls:
            util += (((1 - self.direcProb)/2) * dictMap[dirDict[Directions.LEFT[direc]]])
        else:
            util += (((1 - self.direcProb)/2) * dictMap[current])
        # RIGHT
        if dirDict[Directions.RIGHT[direc]] not in self.walls:
            util += (((1 - self.direcProb)/2) * dictMap[dirDict[Directions.RIGHT[direc]]])
        else:
            util += (((1 - self.direcProb)/2) * dictMap[current])

        return util

    # Converges util values performing Bellman update
    def valueIteration(self, state, reward, discount, dictMap):

        oldMap = None
        while dictMap != oldMap:
            oldMap = dictMap.copy()
            for i in self.wholeMap(state):
                if i not in self.walls + self.food + self.ghosts + self.capsules:
                    dictMap[i] = reward + (discount * self.findMax(state, i, oldMap)[1])
        #print "NEW: ", sorted(dictMap.iteritems())
