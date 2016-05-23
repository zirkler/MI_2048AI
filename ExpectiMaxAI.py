# 2048 5x5 ExpectiMaxi AI

from game import Game, Direction
import numpy
import copy
import time


class MaxNode:
    def __init__(self, game, depth):
        self.game = copy.deepcopy(game)
        self.depth = depth
        self.action = 0
        self.successors = []
        self.actionList = []
        self.action = 0
        self.value = self.getValue()


    def __str__(self):
        printStr =  "MaxNode:\n"
        printStr +=  str(self.game.state.astype(numpy.uint32))
        printStr += "\nMaxNodeValue: " + str(self.value)
        return printStr

    def getValue(self):
        if self.depth == 0:
            value = self.maxNodeTerminalValue()
        else:
            self.branch()
            possibleValueSuccessors = []
            for chanceNode in self.successors:
                possibleValueSuccessors.append(chanceNode.value)
            possibleValueSuccessors = numpy.array(possibleValueSuccessors)
            value = max(possibleValueSuccessors)
            self.action = numpy.argmax(possibleValueSuccessors) + 1
            self.actionList = possibleValueSuccessors

        return value

    def branch(self):
        for i in xrange(4):
            #Generate Chance Node for all possible moves
            succGame = copy.deepcopy(self.game)
            if(succGame.move(i+1)):
                succ = ChanceNode(succGame, i+1, depth= self.depth)
                self.successors.append(succ)

    def maxNodeTerminalValue(self):
        weightMatrix = numpy.array(
                      [[0.15, 0.135759, 0.121925, 0.102812, 0.099937],
                      [0.135759, 0.0997992, 0.0888405, 0.076711, 0.0724143],
                      [0.0724143, 0.060654 , 0.0562579 , 0.037116 , 0.0161889],
                      [0.0161889, 0.0125498 , 0.00992495 , 0.00575871 , 0.00335193],
                      [0.0125498 , 0.00992495 , 0.00575871 , 0.00335193, 0.0002]])

        possibleValues = []
        for i in range(0,4):
            currentWeight = numpy.rot90(weightMatrix, i)
            possibleValues.append((currentWeight * self.game.state).sum())
            possibleValues.append((currentWeight.transpose() * self.game.state).sum())
        value = max(possibleValues)
        return value





class ChanceNode:
    def __init__(self, game, direction, depth):
        self.depth = depth
        self.value = 0
        self.game = game
        self.branchNodes = []
        self.value = self.getChanceNodeValue()


    # Generate successors
    def branch(self):
        availableCells = self.game.get_available_cells()
        self.branchWeights = []
        self.branchNodes = []

        for cell in availableCells:
            branchGame = copy.deepcopy(self.game)

            for value in [2,4]:
                if value == 2:
                    probability = 0.9
                else:
                    probability = 0.1

                branchWeight = 1.0 / (len(availableCells)) * probability
                self.branchWeights.append(branchWeight)
                branchGame.set(cell, value)

                branchedMaxNode = MaxNode(branchGame, depth=(self.depth-1))
                self.branchNodes.append(branchedMaxNode)

        self.branchWeights = numpy.array(self.branchWeights)


    def getChanceNodeValue(self):
        self.branch()
        branchValues = []
        for node in self.branchNodes:
            branchValues.append(node.value)

        successorValues = numpy.array(branchValues)
        value = sum(successorValues * self.branchWeights)
        return value


    def __str__(self):
        printStr =  "ChanceNode \n"
        printStr += str(self.game.state.astype(numpy.uint32))
        printStr += "\nChanceNodeValue:" + str(self.value)
        return printStr


# start
initialGame = Game(testing = False)
for i in range(0,100):
    initialGame.testing = True
    startNode = MaxNode(initialGame, 2)
    initialGame.testing = False
    print initialGame.state.astype(numpy.uint32)
    initialGame.move(startNode.action)
    if startNode.action == 1:
        print "left"
    elif startNode.action == 2:
        print "right"
    elif startNode.action == 3:
        print "up"
    elif startNode.action == 4:
        print "down"
    print initialGame.state.astype(numpy.uint32)
    print "****************************************************************"
print startNode.action
print startNode.value
print startNode.actionList
