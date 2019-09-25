# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
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

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP
    
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)

# GoWestAgent
#
# Always tries to go West. If it cannot, it will choose a random direction
class GoWestAgent(Agent):

    def __init__(self):
        self.last = Directions.STOP

    def getAction(self, state):
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        if Directions.WEST in legal:
            return api.makeMove(Directions.WEST, legal)
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            self.last = pick
            return api.makeMove(pick, legal)

# HungryAgent
#
# Tries to move to the nearest food location
class HungryAgent(Agent):

    # Constructor
    #
    #
    #def __init__(self):
    #    self.last = Directions.STOP

    def getAction(self, state):

        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        nearest = theFood[0]
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        for i in range(len(theFood)):
            if util.manhattanDistance(pacman, theFood[i]) <= util.manhattanDistance(pacman, nearest):
                nearest = theFood[i]

        # Calculate coords of pacman and food to determine Direction
        xDiff = pacman[0] - nearest[0]
        yDiff = pacman[1] - nearest[1]
        temp = (xDiff, yDiff)
        pick = random.choice(legal)

        # Uses difference in coords to determine Direction to travel
        if abs(temp[0]) > abs(temp[1]):
            if temp[0] < 0 and Directions.EAST in legal:
                print "EAST: ", legal
                return api.makeMove(Directions.EAST, legal)
            elif temp[0] >= 0 and Directions.WEST in legal:
                print "WEST: ", legal
                return api.makeMove(Directions.WEST, legal)
            else:
                print "RAND: ", legal
                return api.makeMove(pick, legal)

        elif abs(temp[0]) <= abs(temp[1]):
            if temp[1] < 0 and Directions.NORTH in legal:
                print "NORTH: ", legal
                return api.makeMove(Directions.NORTH, legal)
            elif temp[1] >= 0 and Directions.SOUTH in legal:
                print "SOUTH: ", legal
                return api.makeMove(Directions.SOUTH, legal)
            else:
                print "RAND: ", legal
                return api.makeMove(pick, legal)
        else:
            print "RAND: ", legal
            return api.makeMove(pick, legal)

# SurvivalAgent
#
# Tries to survive as long as possible by avoiding the ghosts
class SurvivalAgent(Agent):

    # Constructor
    #
    #
    def __init__(self):
        self.last = Directions.STOP

    def getAction(self, state):

        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theGhosts = api.ghosts(state)
        nearest = theGhosts[0]
        for i in range(len(theGhosts)):
            if util.manhattanDistance(pacman, theGhosts[i]) <= util.manhattanDistance(pacman, nearest):
                nearest = theGhosts[i]

        # Calculate coords of pacman and ghosts to determine Direction
        xDiff = pacman[0] - nearest[0]
        yDiff = pacman[1] - nearest[1]
        temp = (xDiff, yDiff)
        #print "PAC: ", pacman
        #print "NEAR: ", nearest
        #print "DIFF ", temp 

        pick = random.choice(legal)
        

        # Uses difference in coords to determine Direction to travel
        if abs(temp[0]) > abs(temp[1]):
            if temp[0] < 0 and Directions.WEST in legal:
                return api.makeMove(Directions.WEST, legal)
            elif Directions.EAST in legal:
                return api.makeMove(Directions.EAST, legal)
        elif abs(temp[0]) > abs(temp[1]):
            if temp[1] < 0 and Directions.SOUTH in legal:
                return api.makeMove(Directions.SOUTH, legal)
            elif Directions.NORTH in legal:
                return api.makeMove(Directions.NORTH, legal)
        else:
            print "RAND", pick
            print legal
            return api.makeMove(pick, legal)