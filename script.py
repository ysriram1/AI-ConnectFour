# noinspection PyPEP8Naming
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 05 18:58:50 2017

@author: Sriram Yarlagadda
"""
import os
import numpy as np

#os.chdir('C:/Users/SYARLAG1/Desktop/AI-ConnectFour-Go')
os.chdir('/Users/Sriram/Desktop/DePaul/Q5/CSC 480/AI-ConnectFour-Go')

# 9 x 9 board
# 2 points for pair next to each other
# 1 point for every piece diagnol to each other

#self.shape = shape
#charArr = np.chararray(shape)
#charArr[:] = '.'

# in this program, 'max' refers to player and 'min' refers to ai

class board(object):
    
    def __init__(self, boardArr):

        self.boardArr = np.copy(boardArr) # returns the array of the board
        
    # prints the board with the positions filled    
    def printBoard(self):

        printStr = 'Current Board: \n\n'

        for row in self.boardArr:
            printStr += '|' + ' '.join(row) + '| \n'

        return printStr
    
    # updates board by adding '0' at appropriate pos in selected col    
    def playerMove(self, colNum):

        newBoardArr = np.copy(self.boardArr)

        colFull = False        
        targetCol = newBoardArr[:,colNum]

        try:
            targetColLst = list(targetCol)
            highestDot = len(targetColLst) - targetColLst[::-1].index('.') - 1 # location of highest empty space   
        except:
            colFull = True
            
        if colFull:
            print 'Selected Column is full'
            return False
               
        newBoardArr[highestDot, colNum] = 'O'
        
        return board(newBoardArr)
        
    # updates board by adding 'X' at appropriate pos in selected col   
    def aiMove(self, colNum):

        newBoardArr = np.copy(self.boardArr)
                
        colFull = False        
        targetCol = newBoardArr[:,colNum]

        try:
            targetColLst = list(targetCol)
            highestDot = len(targetColLst) - targetColLst[::-1].index('.') - 1 # location of highest empty space   
        except:
            colFull = True
                
        if colFull:
            print 'Selected Column is full'
            return False
               
        newBoardArr[highestDot, colNum] = 'X'

        return board(newBoardArr)
     
    # evaluates the total score = score(max) - score(min)
    # returns maxScore, minScore, and max-min
    def evaluate(self):
        
        maxScore = 0 # aka the player's score 
        indices_0 = np.where(self.boardArr == 'O') # location of '0'. ([rows],[cols])
        indices_0_zip = zip(indices_0[0], indices_0[1]) # (row_i,col_i)        
        
        for i in range(len(indices_0_zip)):
            for j in range(i,len(indices_0_zip)):

                if indices_0_zip[i][0] == indices_0_zip[j][0] and \
                indices_0_zip[i][1] + 1 == indices_0_zip[j][1]: # same row, consecutive col
                    maxScore += 2
                
                if indices_0_zip[i][1] == indices_0_zip[j][1] and \
                indices_0_zip[i][0] + 1 == indices_0_zip[j][0]: # same col, consecutive row
                    maxScore += 2
                
                if indices_0_zip[i][1] + 1 == indices_0_zip[j][1] and \
                indices_0_zip[i][0] + 1 == indices_0_zip[j][0]: # diagnol \ dir
                    maxScore += 1
                
                if indices_0_zip[i][1] == indices_0_zip[j][1] + 1 and \
                indices_0_zip[i][0] + 1 == indices_0_zip[j][0]: # diagnol / dir
                    maxScore += 1

        minScore = 0 # aka the ai score
        indices_X = np.where(self.boardArr == 'X') # location of '0'. ([rows],[cols])
        indices_X_zip = zip(indices_X[0], indices_X[1]) # (row_i,col_i)        
        
        for i in range(len(indices_X_zip)):
            for j in range(i,len(indices_X_zip)):

                if indices_X_zip[i][0] == indices_X_zip[j][0] and \
                indices_X_zip[i][1] + 1 == indices_X_zip[j][1]: # same row, consecutive col
                    minScore += 2
                
                if indices_X_zip[i][1] == indices_X_zip[j][1] and \
                indices_X_zip[i][0] + 1 == indices_X_zip[j][0]: # same col, consecutive row
                    minScore += 2
                
                if indices_X_zip[i][1] + 1 == indices_X_zip[j][1] and \
                indices_X_zip[i][0] + 1 == indices_X_zip[j][0]: # diagnol
                    minScore += 1
                    
                if indices_X_zip[i][1] == indices_X_zip[j][1] + 1 and \
                indices_X_zip[i][0] + 1 == indices_X_zip[j][0]: # diagnol / dir
                    minScore += 1
                    
        
        return maxScore, minScore, maxScore - minScore
            
            

    def isGoal(self): # goal reached when all dots filled
        
        return len(np.where(self.boardArr == '.')[0]) == 0
        
        
###############################################################################
class node(object):
    
    def __init__(self, boardObj):
        
        self.boardObj = boardObj

    
    # generate the successors    

    def genSuccessors(self, who):
                
        if who == 'max':
            
            for col_pos in range(self.boardObj.boardArr.shape[0]):
                
                yield self.boardObj.playerMove(col_pos)
        
        if who == 'min':

            for col_pos in range(self.boardObj.boardArr.shape[0]):
                
                yield self.boardObj.AImove(col_pos)



###############################################################################
    
def minimax(boardShape = [9,9], maxDepth):
    
    charArr = np.chararray(boardShape)
    charArr[:] = '.'
    
    initBoard = board(charArr)
    
    print 'Here is the initial board:'
    
    print initBoard.printBoard()
    
    
    node.add(initBoard.playerMove(firstMove))
    
    goalReached = False
    
    currBoard = initBoard # all dots

    
    while not goalReached:
                
        playerMoveCol = int(input('Please enter a column number to drop checkers in: ')) 
        
        nextBoard = currBoard.playerMove(playerMoveCol) # board with first player move
        
        # adding attributes to current node
        currNode = node(nextBoard)
        currNode.parent = False
        currNode.type = 'max' # we start with player (max) as root node
        currNode.depth = 0 # start with depth of 0
        currNode.childGen = currNode.genSuccessors('max')
        
        # queue to hold nodes that have already been calculated for performance enhancement
        visitedAndCalculated = [] 
        #nodeGenStore = [currNode.genSuccessors('min')]
        depthQ = [currNode] # queue to hold nodes
        visited = [currNode] # previously visited nodes
           
        while currNode.depth < maxDepth:
            
            childNode = next(currNode.childGen)
            childNode.depth = currNode.depth + 1
            childNode.parent = currNode
            childNode.type = 'min' if currNode.type == 'max' else 'max'
            
            nextType = 'min' if nextNode.type == 'max' else 'max'
            
            childNode.childGen = childNode.genSuccessors(nextType)
            
            currNode = childNode
        
        # currNodethis is the node at the last depth level
        
        # now that we reached the final depth, we start moving\
        # back up and calculating cost
        
        while not currNode.parent:
            
            prevNode = currNode.parent            
            prevNode.eval = currentNode.evaluate()[2] # only want diff

            moreChildren = True

            while moreChildren:            
                try:
                                        
                    
                except:
                    moreChildren = False
                
                
            
            
            
        
            
            
                        
            
        currBoard = nextBoard

        goalReached = currBoard.isGoal()        
    
    
    playerScore, aiScore, finalScore = currBoard.evaluate() # extract only max - min
    
    print 'Computer\'s Score: ', aiScore
    print 'Your Score: ', playerScore
            
    if finalScore > 0:
        print 'You win! Congrates!'
        
    if finalScore < 0 :
        print 'Computer Wins!'
    
        
    
    
# calc cost for each successor function
# create successor function which lists out possible moves for opponent
# add alpha beta pruning
# goal test function -- tells if state is terminal

    
def gen(i):
    for x in range(i): yield 5


