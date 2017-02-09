# noinspection PyPEP8Naming
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 05 18:58:50 2017

@author: Sriram Yarlagadda
"""
import os
import numpy as np
from sys import maxsize

os.chdir('C:/Users/SYARLAG1/Desktop/AI-ConnectFour-Go')
#os.chdir('/Users/Sriram/Desktop/DePaul/Q5/CSC 480/AI-ConnectFour-Go')

## RULES:
# 9 x 9 board
# 2 points for pair next to each other
# 1 point for every piece diagnol to each other

# Note: 'max' refers to player and 'min' refers to ai
###############################################################################
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
            #print 'Selected Column is full'
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
            #print 'Selected Column is full'
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

    # returns a list of successors    
    def successors(self, kind):
        
        childBoards = []
                
        if kind == 'max':
            
            for col_pos in range(self.boardArr.shape[1]):
                
                newBoardObj = self.aiMove(col_pos)
                
                if not newBoardObj: continue # if col is full
                
                childBoards.append(newBoardObj)
        
        if kind == 'min':

            for col_pos in range(self.boardArr.shape[1]):
                
                newBoardObj = self.aiMove(col_pos)

                if not newBoardObj: continue# if col is full              
                
                childBoards.append(newBoardObj)         
        
        return childBoards        
        
            
    # checks if board is full (hence is goal)
    def isGoal(self): # goal reached when all dots filled
        
        return len(np.where(self.boardArr == '.')[0]) == 0
        
    
###############################################################################
def minMaxSearch(currentNode, depth, kind, maxDepth, alphaBeta=False, alpha = -maxsize, beta=maxsize):
    '''
    returns the best next board move based on minimax search
    '''
    
    if depth == maxDepth: # terminal node
        
        return currentNode.evaluate()[2] 
        
    if kind == 'max':
        
        if depth == 0: # if we are looking at root --> capture best board in next layer
            
            depth1Vals = []
            depth1Nodes = []
        
        childNodes = currentNode.successors('min')
        currVal = alpha # initialize a lowest possible value (only changes when alphaBeta is True)
        
        for childNode in childNodes:
            
            if alphaBeta:
                
                childVal = minMaxSearch(childNode, depth+1, 'min', maxDepth, True, currVal, beta) 
                currVal = max(currVal, childVal)
                #alpha = max(currVal, alpha)
                
                if depth == 0: # if rootnode, then we need to return next move node
                
                    depth1Vals.append(childVal) 
                    depth1Nodes.append(childNode)       
                   
                if beta <= currVal: # if true, this cannot be the shortest path, so dont consider
                    break 
            else: 
                childVal = minMaxSearch(childNode, depth+1, 'min', maxDepth) 
                currVal = max(currVal, childVal)
            
                if depth == 0: # if rootnode, then we need to return next move node
                
                    depth1Vals.append(childVal) 
                    depth1Nodes.append(childNode)                  
                        
        if depth == 0: # return the node that corresponds to next move 
        
            return depth1Nodes[depth1Vals.index(max(depth1Vals))]
    
        else:        
            return currVal
            
    if kind == 'min':
        
        childNodes = currentNode.successors('max')
        currVal = beta # initialize a largest possible value
            
        for childNode in childNodes:
            
            if alphaBeta:
                
                childVal = minMaxSearch(childNode, depth+1, 'max', maxDepth, True, alpha, currVal) 
                currVal = min(currVal, childVal)
                #beta = min(beta, currVal)
                
                if depth == 0: # if rootnode, then we need to return next move node
                
                    depth1Vals.append(childVal) 
                    depth1Nodes.append(childNode)    
            
                if currVal <= alpha:
                    break
            
            else:
                
                childVal = minMaxSearch(childNode, depth+1, 'max', maxDepth) 
                currVal = min(currVal, childVal)
            
        return currVal            

###############################################################################
    
def playGame(maxDepth, boardShape = [9,9], alphaBeta=False):
    
    charArr = np.chararray(boardShape)
    charArr[:] = '.'
    
    initBoard = board(charArr)
    
    print 'Here is the initial board:'
    
    print initBoard.printBoard()

    currBoard = initBoard # all dots
    
    while True:
        
        # Player Turn
        playerMoveCol = int(input('Please enter a column number (0 to 8) to drop checkers in: ')) 
        
        nextBoard_afterPlayer = currBoard.playerMove(playerMoveCol) # board with player move
        
        while not nextBoard_afterPlayer: # selected column in full
        
            playerMoveCol = int(input('Selected column is full, please select another column: ')) 
            
            nextBoard_afterPlayer = currBoard.playerMove(playerMoveCol)
            
        
        print nextBoard_afterPlayer.printBoard()
        print 'player score: ', nextBoard_afterPlayer.evaluate()[0]
        print 'computer score: ', nextBoard_afterPlayer.evaluate()[1], '\n'
        
        goalReached_player = nextBoard_afterPlayer.isGoal()
        
        if goalReached_player: break           
        
        # AI Turn       
        if alphaBeta:
            nextBoard_afterAI = minMaxSearch(nextBoard_afterPlayer, 0, 'max', maxDepth, True)
        else:            
            nextBoard_afterAI = minMaxSearch(nextBoard_afterPlayer, 0, 'max', maxDepth)     
        
        print 'Computer has played. Here is the board: \n'
        print nextBoard_afterAI.printBoard()        
        print 'player score: ', nextBoard_afterAI.evaluate()[0]
        print 'computer score: ', nextBoard_afterAI.evaluate()[1], '\n'
        
        goalReached_ai = nextBoard_afterAI.isGoal()   
        
        if goalReached_ai: break   

        currBoard = nextBoard_afterAI
    
    if goalReached_ai: finalBoard = nextBoard_afterAI
    if goalReached_player: finalBoard = nextBoard_afterPlayer
    
    playerScore, aiScore, finalScore = finalBoard.evaluate() # extract only max - min
    
    print 'Computer\'s Score: ', aiScore
    print 'Your Score: ', playerScore
            
    if finalScore > 0:
        print 'You win! Congrats!'
        
    if finalScore < 0:
        print 'Computer Wins!'
        
        
###############################################################################

 
# calc cost for each successor function
# create successor function which lists out possible moves for opponent
# add alpha beta pruning
# goal test function -- tells if state is terminal
playGame(7, boardShape = [9,9], alphaBeta=True)


