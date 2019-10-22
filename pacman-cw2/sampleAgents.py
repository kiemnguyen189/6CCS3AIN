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

    return (legality[0], legality)

#TODO: Create a waypoint system / A star
# Returns a direction based on the nearest entity (food / capsule)
def findDirection(tempEntity, legality, l1):
    
    #print "###########################################"
    #print "findDirection entity: ", tempEntity
    #print "findDirection reverse: ", reverse
    #print "findDirection legality: ", legality
    direc = Directions.STOP

    if abs(tempEntity[0]) > abs(tempEntity[1]): # HORIZONTAL
        ##print "IF"
        if tempEntity[0] < 0 and Directions.EAST in legality:
            direc = Directions.EAST
        elif tempEntity[0] >= 0 and Directions.WEST in legality:
            direc = Directions.WEST
        else:
            #print "RANDOM"
            direc = random.choice(legality)
    else:   # VERTICAL
        ##print "ELSE"
        if tempEntity[1] < 0 and Directions.NORTH in legality:
            direc = Directions.NORTH
        elif tempEntity[1] >= 0 and Directions.SOUTH in legality:
            direc = Directions.SOUTH
        else:
            #print "RANDOM"
            direc = random.choice(legality)
    #print "RETURN: ", direc, ", ", legality
    if len(l1) == 1:
        l1.pop(0)
    if len(l1) < 1:
        l1.append(direc)
    return (direc, legality) 

def waypoints():
    

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
        diff = [x for x in whole if x not in set(walls)]
        ##diff = list(set(whole) - set(walls))
        print diff
        return api.makeMove(Directions.STOP, legal)

