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

    direcProb = 0.8
    emptyReward = -0.04
    foodReward = 1
    capsuleReward = 1
    ghostReward = -1
    discountFactor = 1
    diff = []
    dictMap = {}

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up MDPAgent!"
        name = "Pacman"

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        print "Running registerInitialState for MDPAgent!"
        print "I'm at:"
        print api.whereAmI(state)
        walls = api.walls(state)
        finalCell = walls[len(walls) - 1]
        whole = []
        for i in range(finalCell[0]+1):
            for j in range(finalCell[1]+1):
                whole.append((i, j))
        diff = [x for x in whole if x not in set(walls)]
        print diff
        dictMap = { i : 0 for i in diff }
        print dictMap
        # find all food and capsules to set rewards 1 and -1 respectively
        wallGrid = state.getWalls()
        foodGrid = state.getFood()
        #for j in range(diff):
          #  if j = 
        #print Directions.LEFT[Directions.NORTH]

        
    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like the game just ended!"

    # For now I just move randomly
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        # use bellman equation for utilities to calculate util of each square
        #for i, j in dictMap.items():
         #   tempUtil = 0

            


        
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

    # find adjacent coords or current using LEFT and RIGHT
    # returns list of 3 adjacent coords
    def findAdjacent(coord, curDir):
        coordDir = {UP:(1,0), RIGHT:(0,1), LEFT(0,-1)}
        up = coord[0] + coordDir[UP][0]
        right = coord[1] + coordDir[RIGHT][1]
        left = coord[1] + coordDir[LEFT][1]
        actionSum = (0.8*up)+(0.1*right)+(0.1*left)

        coords = []
        coords.insert(coord)
        return coords

    # takes in reward, discount factor and dictionary of utilities
    def bellman(reward, discount, dict):
        actionProbs = []
        for i, j in dict.items():

        # TODO: finish direction utilities (up, left, down, right) and
        # TODO: times probs (0.8, 0.1, 0.1) for each [12 total]
        maxSum = max()
        ret = reward + (discount * maxSum)



    #def MDP():



    #def valueIteration(self, state):

        #for 
