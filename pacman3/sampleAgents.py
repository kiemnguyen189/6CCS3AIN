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
    def __init__(self):
        self.last = Directions.STOP

    def getAction(self, state):

        # Get the actions we can try
        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        nearest = theFood[0]
        # remove "STOP" action from legal actions
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it
        if self.last in legal:
            return api.makeMove(self.last, legal)
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
                print "EAST: ", legal, " ", pacman, " ", nearest, " ", util.manhattanDistance(pacman, nearest)
                return api.makeMove(Directions.EAST, legal)
            elif temp[0] >= 0 and Directions.WEST in legal:
                print "WEST: ", legal, " ", pacman, " ", nearest, " ", util.manhattanDistance(pacman, nearest)
                return api.makeMove(Directions.WEST, legal)
            else:
                print "### RAND: ", legal, " ", pacman, " ", nearest, " ", util.manhattanDistance(pacman, nearest)
                return api.makeMove(pick, legal)
        else:
            if temp[1] < 0 and Directions.NORTH in legal:
                print "NORTH: ", legal, " ", pacman, " ", nearest, " ", util.manhattanDistance(pacman, nearest)
                return api.makeMove(Directions.NORTH, legal)
            elif temp[1] >= 0 and Directions.SOUTH in legal:
                print "SOUTH: ", legal, " ", pacman, " ", nearest, " ", util.manhattanDistance(pacman, nearest)
                return api.makeMove(Directions.SOUTH, legal)
            else:
                print "### RAND: ", legal, " ", pacman, " ", nearest, " ", util.manhattanDistance(pacman, nearest)
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

        pick = random.choice(legal)
        
        if util.manhattanDistance(pacman, nearest) < 4:
            # Uses difference in coords to determine Direction to travel
            if abs(temp[0]) > abs(temp[1]):
                if temp[0] < 0 and Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                elif temp[0] >= 0 and Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                else:
                    return api.makeMove(pick, legal)
            else:
                if temp[1] < 0 and Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                elif temp[1] >= 0 and Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    return api.makeMove(pick, legal)
        else:
            return api.makeMove(pick, legal)

# CornerSeekingAgent
#
# Tries to find the corners of the map
class CornerSeekingAgent(Agent):

    # Constructor
    #
    #
    def __init__(self):
        self.last = Directions.STOP
        self.visited = []

    def getAction(self, state):

        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        theGhosts = api.ghosts(state)
        corners = api.corners(state)
        unvisited = list(set(corners) - set(self.visited))
        print "###############################"
        print pacman
        print corners[0]
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        for i in range(len(corners)):
            elem = corners[i]
            print "ELEM ", i, ": ", elem
            #print abs(pacman[0] - elem[0]) - abs(pacman[1] - elem[1])
            print util.manhattanDistance(pacman, elem)
            # check if pacman is close enough to a corner
            if util.manhattanDistance(pacman, elem) == 2:
                print self.visited
                print unvisited
                if elem not in self.visited:
                    self.visited.append(elem)
                if elem in unvisited:
                    unvisited.remove(elem)
        print "CORNERS: ", len(corners), corners
        print "VISITED: ", len(self.visited), self.visited
        print "UNVISITED: ", len(unvisited), unvisited
        
        nearestCorner = (9999, 9999)
        for i in range(len(unvisited)):
            if util.manhattanDistance(pacman, unvisited[i]) <= util.manhattanDistance(pacman, nearestCorner):
                nearestCorner = unvisited[i]
        tempCorner = (pacman[0] - nearestCorner[0], pacman[1] - nearestCorner[1])

        # If list of food is empty, nearest food is at not in range
        if len(theFood) == 0:
            nearestFood = (9999, 9999)
        else:
            nearestFood = theFood[0]
        # Calculates the Manhattan distances of food and ghosts and assigns nearest
        for i in range(len(theFood)):
            if util.manhattanDistance(pacman, theFood[i]) <= util.manhattanDistance(pacman, nearestFood):
                nearestFood = theFood[i]
        # Calculate coords of pacman and food to determine Direction
        tempFood = (pacman[0] - nearestFood[0], pacman[1] - nearestFood[1])
        
        pick = random.choice(legal)
        #first = unvisited[0]
        #print "CLOSEST: ", first
        #tempCorner = (pacman[0] - first[0], pacman[1], first[1])
        if len(theFood) != 0:
            print "FINDFOOD"
            # FIND FOOD: Uses difference in coords of food to determine Direction to travel
            if abs(tempFood[0]) > abs(tempFood[1]):
                if tempFood[0] < 0 and Directions.EAST in legal:
                    print "EAST: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.EAST, legal)
                elif tempFood[0] >= 0 and Directions.WEST in legal:
                    print "WEST: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.WEST, legal)
                else:
                    print "### RAND: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(pick, legal)
            else:
                if tempFood[1] < 0 and Directions.NORTH in legal:
                    print "NORTH: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.NORTH, legal)
                elif tempFood[1] >= 0 and Directions.SOUTH in legal:
                    print "SOUTH: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    print "### RAND: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(pick, legal)
        else: 
            if abs(tempCorner[0]) > abs(tempCorner[1]):
                if tempCorner[0] < 0 and Directions.EAST in legal:
                    print "    EAST"
                    return api.makeMove(Directions.EAST, legal)
                elif tempCorner[0] >= 0 and Directions.WEST in legal:
                    print "    WEST"
                    return api.makeMove(Directions.WEST, legal)
                else:
                    print "    RAND"
                    return api.makeMove(pick, legal)
            else:
                if tempCorner[1] < 0 and Directions.NORTH in legal:
                    print "    NORTH"
                    return api.makeMove(Directions.NORTH, legal)
                elif tempCorner[1] >= 0 and Directions.SOUTH in legal:
                    print "    SOUTH"
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    print "    RAND"
                    return api.makeMove(pick, legal)
        

        



# BothAgent
#
# Combines both HungryAgent and SurvivalAgent to create a semi-intelligent pacman
class BothAgent(Agent):

    # Constructor
    #
    #
    def __init__(self):
        self.last = Directions.STOP

    def getAction(self, state):

        # Get the actions we can try
        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        theGhosts = api.ghosts(state)
        # If list of ghosts is empty, nearest ghost is not in range
        if len(theGhosts) == 0:
            nearestGhost = (9999, 9999)
        else:
            nearestGhost = theGhosts[0]
        # If list of food is empty, nearest food is at not in range
        if len(theFood) == 0:
            nearestFood = (9999, 9999)
        else:
            nearestFood = theFood[0]
        # remove "STOP" action from legal actions
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Calculates the Manhattan distances of food and ghosts and assigns nearest
        for i in range(len(theFood)):
            if util.manhattanDistance(pacman, theFood[i]) <= util.manhattanDistance(pacman, nearestFood):
                nearestFood = theFood[i]
        for i in range(len(theGhosts)):
            if util.manhattanDistance(pacman, theGhosts[i]) <= util.manhattanDistance(pacman, nearestGhost):
                nearestGhost = theGhosts[i]

        # Calculate coords of pacman and food to determine Direction
        tempFood = (pacman[0] - nearestFood[0], pacman[1] - nearestFood[1])
        # Calculate coords of pacman and ghosts to determine Direction
        tempGhost = (pacman[0] - nearestGhost[0], pacman[1] - nearestGhost[1])

        pick = random.choice(legal)
        detectionDist = 5
        
        # If we can repeat the last action, do it
        if self.last in legal:
            return api.makeMove(self.last, legal)
        # DETECT CLOSE GHOSTS
        if util.manhattanDistance(pacman, nearestGhost) < detectionDist:
            print "AVOID"
            # Uses difference in coords to determine Direction to travel
            if abs(tempGhost[0]) > abs(tempGhost[1]):
                if tempGhost[0] < 0 and Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                elif tempGhost[0] >= 0 and Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                else:
                    return api.makeMove(pick, legal)
            else:
                if tempGhost[1] < 0 and Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                elif tempGhost[1] >= 0 and Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    return api.makeMove(pick, legal)
        else:
            print "FINDFOOD"
            # FIND FOOD: Uses difference in coords of food to determine Direction to travel
            if abs(tempFood[0]) > abs(tempFood[1]):
                if tempFood[0] < 0 and Directions.EAST in legal:
                    print "EAST: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.EAST, legal)
                elif tempFood[0] >= 0 and Directions.WEST in legal:
                    print "WEST: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.WEST, legal)
                else:
                    print "### RAND: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(pick, legal)
            else:
                if tempFood[1] < 0 and Directions.NORTH in legal:
                    print "NORTH: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.NORTH, legal)
                elif tempFood[1] >= 0 and Directions.SOUTH in legal:
                    print "SOUTH: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    print "### RAND: ", legal, " ", pacman, " ", nearestFood, " ", util.manhattanDistance(pacman, nearestFood)
                    return api.makeMove(pick, legal)


# TriAgent
#
# Combines: Ghost avoidance, food finding, corner seeking
class TriAgent(Agent):

    def __init__(self):
        self.last = Directions.STOP
        self.visited = []

    def getAction(self, state):

        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        theGhosts = api.ghosts(state)
        corners = api.corners(state)
        unvisited = list(set(corners) - set(self.visited))

        # Stops pacman from standing still
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If list of ghosts is empty, nearest ghost is not in range
        if len(theGhosts) == 0:
            nearestGhost = (9999, 9999)
        else:
            nearestGhost = theGhosts[0]
        # If list of food is empty, nearest food is at not in range
        if len(theFood) == 0:
            nearestFood = (9999, 9999)
        else:
            nearestFood = theFood[0]
        # Adds corners to be stored persistently
        for i in range(len(corners)):
            elem = corners[i]
            # check if pacman is close enough to a corner
            if util.manhattanDistance(pacman, elem) == 2:
                if elem not in self.visited:
                    self.visited.append(elem)
                if elem in unvisited:
                    unvisited.remove(elem)
        # Calculates the Manhattan distances of ghosts and assigns nearest
        for i in range(len(theGhosts)):
            if util.manhattanDistance(pacman, theGhosts[i]) <= util.manhattanDistance(pacman, nearestGhost):
                nearestGhost = theGhosts[i]
        # Calculates the Manhattan distances of food and assigns nearest
        for i in range(len(theFood)):
            if util.manhattanDistance(pacman, theFood[i]) <= util.manhattanDistance(pacman, nearestFood):
                nearestFood = theFood[i]
        # Calculates the Manhattan distances of corners 
        nearestCorner = (9999, 9999)
        for i in range(len(unvisited)):
            if util.manhattanDistance(pacman, unvisited[i]) <= util.manhattanDistance(pacman, nearestCorner):
                nearestCorner = unvisited[i]

        # Calculate coords of pacman and ghosts to determine Direction
        tempGhost = (pacman[0] - nearestGhost[0], pacman[1] - nearestGhost[1])
        # Calculate coords of pacman and food to determine Direction
        tempFood = (pacman[0] - nearestFood[0], pacman[1] - nearestFood[1])
        # Calculate coords of pacman and corners to determine Direction
        tempCorner = (pacman[0] - nearestCorner[0], pacman[1] - nearestCorner[1])
        # Random direction from legal directions
        pick = random.choice(legal)
        detectionDist = 5
        # DETECT GHOSTS: detects ghosts that are in manhattan range
        if util.manhattanDistance(pacman, nearestGhost) < detectionDist:
            print "AVOID"
            # Uses difference in coords to determine Direction to travel
            if abs(tempGhost[0]) > abs(tempGhost[1]):
                if tempGhost[0] < 0 and Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                elif tempGhost[0] >= 0 and Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                else:
                    return api.makeMove(pick, legal)
            else:
                if tempGhost[1] < 0 and Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                elif tempGhost[1] >= 0 and Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    return api.makeMove(pick, legal)
        # FIND FOOD: Uses difference in coords of food to determine Direction to travel
        elif len(theFood) != 0:
            print "FIND FOOD"
            if abs(tempFood[0]) > abs(tempFood[1]):
                if tempFood[0] < 0 and Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                elif tempFood[0] >= 0 and Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    return api.makeMove(pick, legal)
            else:
                if tempFood[1] < 0 and Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                elif tempFood[1] >= 0 and Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    return api.makeMove(pick, legal)
        # FIND CORNER: finds the corners of no food is in range
        else: 
            print "FIND CORNER"
            if abs(tempCorner[0]) > abs(tempCorner[1]):
                if tempCorner[0] < 0 and Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                elif tempCorner[0] >= 0 and Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    return api.makeMove(pick, legal)
            else:
                if tempCorner[1] < 0 and Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                elif tempCorner[1] >= 0 and Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    return api.makeMove(pick, legal)

# Finds the nearest entity
def nearFind(pac, theList, nearestEntity):

    ##print "##################"
    ##print "nearFind list: ", theList
    ##print "nearFind entity: ", nearestEntity
    for i in range(len(theList)):
        if util.manhattanDistance(pac, theList[i]) <= util.manhattanDistance(pac, nearestEntity):
            nearestEntity = theList[i]
    return nearestEntity

# Returns a direction of an entity relative to pacman
def pairBearing(pac, entity):

    print pac
    print entity
    direc = Directions.STOP
    x = pac[0] - entity[0]
    y = pac[1] - entity[1]
    if abs(x) > abs(y):
        if x < 0:
            direc = Directions.EAST
            print "REV east: ", Directions.REVERSE[direc]
        else:
            direc = Directions.WEST
            print "REV west: ", Directions.REVERSE[direc]
    else:
        if y < 0:
            direc = Directions.NORTH
            print "REV north: ", Directions.REVERSE[direc]
        else:
            direc = Directions.SOUTH
            print "REV south: ", Directions.REVERSE[direc]
    return direc

# Makes pacman run away from the nearest ghost
def runAway(pac, ghost, legality, l1):

    direc = Directions.STOP
    ghostDirec = pairBearing(pac, ghost)
    print "GHOST: ", ghostDirec
    print "LEGAL: ", legality
    if ghostDirec in legality:
        print "removed: ", ghostDirec
        legality.remove(ghostDirec)

    """
    if abs(ghost[0]) > abs(ghost[1]):  # HORIZONTAL
        if ghost[0] < 0 and Directions.WEST in legality:
            direc = Directions.WEST
        elif ghost[0] <= 0 and Directions.EAST in legality:
            direc = Directions.EAST
    else:   # VERTICAL
        if ghost[1] < 0 and Directions.SOUTH in legality:
            direc = Directions.SOUTH
        elif ghost[1] <= 0 and Directions.NORTH in legality:
            direc = Directions.NORTH
    """

    return (legality[0], legality)

# Returns a direction based on the nearest entity (food / capsule)
def findDirection(tempEntity, legality, l1):
    
    #print "###########################################"
    #print "findDirection entity: ", tempEntity
    #print "findDirection reverse: ", reverse
    #print "findDirection legality: ", legality
    direc = Directions.STOP
    #pick = random.choice(legality)
    #print "L1: ", l1
    ##TODO: Fix reverse pick
    asDir = l1[0]
    if Directions.REVERSE[asDir] in legality:
        pick = Directions.REVERSE[asDir]
        #print "PICK 1: ", pick
    else:
        pick = random.choice(legality)
        #print "PICK 2: ", pick
    #pick = Directions.REVERSE[asDir] in legality
    #s = set(l1)
    #pick = [x for x in legality if x not in s]

    if abs(tempEntity[0]) > abs(tempEntity[1]): # HORIZONTAL
        ##print "IF"
        if tempEntity[0] < 0 and Directions.EAST in legality:
            direc = Directions.EAST
        elif tempEntity[0] >= 0 and Directions.WEST in legality:
            direc = Directions.WEST
        else:
            #print "RANDOM"
            direc = pick
    else:   # VERTICAL
        ##print "ELSE"
        if tempEntity[1] < 0 and Directions.NORTH in legality:
            direc = Directions.NORTH
        elif tempEntity[1] >= 0 and Directions.SOUTH in legality:
            direc = Directions.SOUTH
        else:
            #print "RANDOM"
            direc = pick
    #print "RETURN: ", direc, ", ", legality
    if len(l1) == 1:
        l1.pop(0)
    if len(l1) < 1:
        l1.append(direc)
    return (direc, legality) 

# TestAgent
#
# A cleaner version of TriAgent
class TestAgent(Agent):

    def __init__(self):
        self.last = Directions.STOP
        self.last3 = [Directions.STOP]
        self.visited = []

    def getAction(self, state):

        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        theGhosts = api.ghosts(state)
        corners = api.corners(state)
        unvisited = list(set(corners) - set(self.visited))

        # Stops pacman from standing still
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If list of ghosts is empty, nearest ghost is not in range
        if len(theGhosts) == 0:
            nearestGhost = (9999, 9999)
        else:
            nearestGhost = theGhosts[0]
        # If list of food is empty, nearest food is at not in range
        if len(theFood) == 0:
            nearestFood = (9999, 9999)
        else:
            nearestFood = theFood[0]
        # If list of unvisited corners is empty
        if len(unvisited) == 0:
            nearestCorner = (9999, 9999)
        else:
            nearestCorner = unvisited[0]
        # Adds corners to be stored persistently
        for i in range(len(corners)):
            elem = corners[i]
            # check if pacman is close enough to a corner
            if util.manhattanDistance(pacman, elem) == 2:
                if elem not in self.visited:
                    self.visited.append(elem)
                if elem in unvisited:
                    unvisited.remove(elem)
        ##print "nG"
        nG = nearFind(pacman, theGhosts, nearestGhost)
        ##print "nF"
        nF = nearFind(pacman, theFood, nearestFood)
        ##print "nC"
        nC = nearFind(pacman, unvisited, nearestCorner)
        
        # TODO: Change to use pairBearing method
        # Calculate coords of pacman and ghosts to determine Direction
        tempGhost = (pacman[0] - nG[0], pacman[1] - nG[1])
        # Calculate coords of pacman and food to determine Direction
        tempFood = (pacman[0] - nF[0], pacman[1] - nF[1])
        # Calculate coords of pacman and corners to determine Direction
        tempCorner = (pacman[0] - nC[0], pacman[1] - nC[1])
        # Random direction from legal directions
        pick = random.choice(legal)
        detectionDist = 5
        l1 = self.last3
        #test

        # TODO: Change to relative positioning of ghosts to pac instead of absolute coords
        if util.manhattanDistance(pacman, nearestGhost) < detectionDist:
            print "AVOID"
            direc = runAway(pacman, nG, legal, l1)
            (d, l) = direc
            #print "LAST 3: ", self.last3
            return api.makeMove(d, l)
        elif len(theFood) != 0:
            print "FIND FOOD"
            direc = findDirection(tempFood, legal, l1)
            (d, l) = direc
            #print "LAST 3: ", self.last3
            return api.makeMove(d, l)
        elif len(theFood) == 0:
            print "FIND CORNERS"
            direc = findDirection(tempCorner, legal, l1)
            (d, l) = direc
            #print "LAST 3: ", self.last3
            return api.makeMove(d, l)
        



class MapBuildingAgent(Agent):

    def __init__(self):
        self.last = Directions.STOP


    def getAction(self, state):
        legal = api.legalActions(state)
        walls = api.walls(state)
        finalCell = walls[len(walls) - 1]
        ##print "FINAL: ", finalCell
        whole = []
        for i in range(finalCell[0]+1):
            for j in range(finalCell[1]+1):
                whole.append((i, j))
                ##print i, j
        ##print whole
        s = set(walls)
        diff = [x for x in whole if x not in s]
        ##diff = list(set(whole) - set(walls))
        print diff
        return api.makeMove(Directions.STOP, legal)

    

"""
# QuadAgent
#
# Combines: Ghost avoidance, food finding, corner seeking, capsule usage
class QuadAgent(Agent):

    def __init__(self):
        self.last = Directions.STOP

    def getAction(self, state):
"""