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
# 9 x 9 board (default)
# 2 points for pair next to each other
# 1 point for every piece diagnol to each other

# Note: 'min' refers to player and 'max' refers to ai
###############################################################################
class board(object):
    
    def __init__(self, boardArr):

        self.boardArr = np.copy(boardArr) # returns the array of the board
        
    # prints the board with the positions filled    
    def printBoard(self):
        '''
        prints out the current board
        '''

        printStr = 'Current Board: \n\n'

        for row in self.boardArr:
            printStr += '|' + ' '.join(row) + '| \n'

        return printStr
    
    # updates board by adding '0' at appropriate pos in selected col    
    def playerMove(self, colNum):
        '''
        drops a 0 in the current board at the first free row in the 
        specified column (colNum)
        
        returns updated board as an object of board class
        '''

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
        '''
        drops an X in the current board at the first free row in the 
        specified column (colNum)
        
        returns updated board as an object of board class
        '''

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
        '''
        drops a 0 in the current board at the first free row in the 
        specified column (colNum)
        
        returns the score of the ai, player, ai - player
        '''
        
        playerScore = 0 
        indices_0 = np.where(self.boardArr == 'O') # location of '0'. ([rows],[cols])
        indices_0_zip = zip(indices_0[0], indices_0[1]) # (row_i,col_i)        
        
        for i in range(len(indices_0_zip)):
            for j in range(i,len(indices_0_zip)):

                if indices_0_zip[i][0] == indices_0_zip[j][0] and \
                indices_0_zip[i][1] + 1 == indices_0_zip[j][1]: # same row, consecutive col
                    playerScore += 2
                
                if indices_0_zip[i][1] == indices_0_zip[j][1] and \
                indices_0_zip[i][0] + 1 == indices_0_zip[j][0]: # same col, consecutive row
                    playerScore += 2
                
                if indices_0_zip[i][1] + 1 == indices_0_zip[j][1] and \
                indices_0_zip[i][0] + 1 == indices_0_zip[j][0]: # diagnol --> \ dir
                    playerScore += 1
                
                if indices_0_zip[i][1] == indices_0_zip[j][1] + 1 and \
                indices_0_zip[i][0] + 1 == indices_0_zip[j][0]: # diagnol --> / dir
                    playerScore += 1

        aiScore = 0 
        indices_X = np.where(self.boardArr == 'X') # location of '0'. ([rows],[cols])
        indices_X_zip = zip(indices_X[0], indices_X[1]) # (row_i,col_i)        
        
        for i in range(len(indices_X_zip)):
            for j in range(i,len(indices_X_zip)):

                if indices_X_zip[i][0] == indices_X_zip[j][0] and \
                indices_X_zip[i][1] + 1 == indices_X_zip[j][1]: # same row, consecutive col
                    aiScore += 2
                
                if indices_X_zip[i][1] == indices_X_zip[j][1] and \
                indices_X_zip[i][0] + 1 == indices_X_zip[j][0]: # same col, consecutive row
                    aiScore += 2
                
                if indices_X_zip[i][1] + 1 == indices_X_zip[j][1] and \
                indices_X_zip[i][0] + 1 == indices_X_zip[j][0]: # diagnol --> / dir
                    aiScore += 1
                    
                if indices_X_zip[i][1] == indices_X_zip[j][1] + 1 and \
                indices_X_zip[i][0] + 1 == indices_X_zip[j][0]: # diagnol --> \ dir
                    aiScore += 1
                    
        
        return aiScore, playerScore,  aiScore - playerScore  # playerScore - aiScore

    # returns a list of successors    
    def successors(self, kind):
        '''
        returns a list of successor boards for a current board based on all the 
        possible places where the computer can move
        '''
        
        childBoards = []
                
        if kind == 'min':
            
            for col_pos in range(self.boardArr.shape[1]):
                
                newBoardObj = self.playerMove(col_pos)
                
                if not newBoardObj: continue # if col is full
                
                childBoards.append(newBoardObj)
        
        if kind == 'max':

            for col_pos in range(self.boardArr.shape[1]):
                
                newBoardObj = self.aiMove(col_pos)

                if not newBoardObj: continue # if col is full              
                
                childBoards.append(newBoardObj)         
        
        return childBoards        
        
            
    # checks if board is full (hence is goal)
    def isGoal(self): # goal reached when all dots filled
        '''
        returns True is board is full else returns False
        '''
        return len(np.where(self.boardArr == '.')[0]) == 0
        
    
###############################################################################
def minMaxSearch(currentNode, depth, kind, maxDepth, alphaBeta=False, alpha=-maxsize, beta=maxsize):
    '''
    returns board with the best next move based on minimax search
    '''
    
    if depth == maxDepth: # if leaf node
        
        return currentNode.evaluate()[2] 
        
    if kind == 'max':            
        
        childNodes = currentNode.successors(kind)
        currVal = alpha # initialize a lowest possible value (only changes when alphaBeta is True)
        
        for childNode in childNodes:
            
            if alphaBeta:
                
                childVal = minMaxSearch(childNode, depth+1, 'min', maxDepth, True, currVal, beta) 
                
                if childVal > currVal:

                    # if we are looking at root --> capture best board in next layer                    
                    if depth == 0: # find the move with the highest value
                    
                        bestNextMove = childNode

                    currVal = childVal
                
                                       
                if beta <= currVal: # if true, dont consider other childNodes
                    break 
            else: 
                childVal = minMaxSearch(childNode, depth+1, 'min', maxDepth) 

                if childVal >= currVal:
                    
                    if depth == 0: # set find the move with the highest value

                        bestNextMove = childNode
                    
                    currVal = childVal
                                        
        if depth == 0: # return the node that corresponds to next move 

            try:
                return bestNextMove
            except:
                return childNode 
                
        else:  
            
            return currVal
            
    if kind == 'min':
        
        childNodes = currentNode.successors(kind)
        currVal = beta # initialize a largest possible value
            
        for childNode in childNodes:
            
            if alphaBeta:
                
                childVal = minMaxSearch(childNode, depth+1, 'max', maxDepth, True, alpha, currVal) 
                currVal = min(currVal, childVal)

                if currVal <= alpha: # if true, dont consider other childNodes
                    break
            
            else:
                
                childVal = minMaxSearch(childNode, depth+1, 'max', maxDepth) 
                currVal = min(currVal, childVal)
            
        return currVal            

###############################################################################
    
def playGame(boardShape = [9,9], alphaBeta=False):
    '''
    plays the game, continuously asks user for move and then performs computer 
    move through minimax search by calling minMaxSearch() function prints scores
    after each play. Checks to see if board is full, if yes, game ends and final 
    score and winner is printed.
    '''
    
    charArr = np.chararray(boardShape)
    charArr[:] = '.'
    
    initBoard = board(charArr)
    
    print 'Here is the initial board:'
    
    print initBoard.printBoard()

    currBoard = initBoard # all dots
    
    maxDepth = int(input('Please pick the number of turns ahead the computer should look: '))
    
    while True:
        
        # Player Turn
        playerMoveCol = int(input('Please enter a column number (0 to 8) to drop checkers in: ')) 
        
        while playerMoveCol > 8 or playerMoveCol < 0: # if invalid col number

            print 'value out of range! \n'             
            playerMoveCol = int(input('Please enter a column number (0 to 8) to drop checkers in: ')) 
        
        nextBoard_afterPlayer = currBoard.playerMove(playerMoveCol) # board with player move
        
        while not nextBoard_afterPlayer: # selected column in full
        
            playerMoveCol = int(input('Selected column is full, please select another column: ')) 
            
            nextBoard_afterPlayer = currBoard.playerMove(playerMoveCol)
            
        
        print nextBoard_afterPlayer.printBoard()
        print 'player score: ', nextBoard_afterPlayer.evaluate()[1]
        print 'computer score: ', nextBoard_afterPlayer.evaluate()[0], '\n'
        
        goalReached_player = nextBoard_afterPlayer.isGoal()
        
        if goalReached_player: break           
        
        # AI Turn       
        if alphaBeta:
            nextBoard_afterAI = minMaxSearch(nextBoard_afterPlayer, 0, 'max', maxDepth, True)
        else:            
            nextBoard_afterAI = minMaxSearch(nextBoard_afterPlayer, 0, 'max', maxDepth)     
        
        print 'Computer has played. Here is the board: \n'
        print nextBoard_afterAI.printBoard()        
        print 'player score: ', nextBoard_afterAI.evaluate()[1]
        print 'computer score: ', nextBoard_afterAI.evaluate()[0], '\n'
        
        goalReached_ai = nextBoard_afterAI.isGoal()   
        
        if goalReached_ai: break   

        currBoard = nextBoard_afterAI
    
    if goalReached_ai: finalBoard = nextBoard_afterAI
    if goalReached_player: finalBoard = nextBoard_afterPlayer
    
    aiScore, playerScore, finalScore = finalBoard.evaluate() 
    
    print '--------------GAME HAS ENDED-------------- \n\n'
    print 'Computer\'s Score: ', aiScore
    print 'Your Score: ', playerScore, '\n\n'
            
    if finalScore < 0:
        print 'You win! Congrats!'
        
    if finalScore > 0:
        print 'Computer Wins!'
        
        
###############################################################################
playGame(boardShape = [5,5], alphaBeta=False)


