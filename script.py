# -*- coding: utf-8 -*-
"""
Created on Sun Feb 05 18:58:50 2017

@author: Sriram Yarlagadda
"""
import os
import math
import numpy as np
os.chdir('C:/Users/SYARLAG1/Desktop/AI-ConnectFour+Go')


# 9 x 9 board
# 2 points for pair next to each other
# 1 point for every piece diagnol to each other

class board(object):
    
    def __init__(self, shape):
        self.shape = shape
        charArr = np.chararray(shape)
        charArr[:] = '.'
        self.boardArr = charArr # returns the array of the board        
        
    # prints the board with the positions filled    
    def printBoard(self):

        printStr = 'Current Board \n'

        for row in self.board:
            printStr += '|' + ' '.join(row) + '| \n'

        print printStr
    
    # updates board by adding '0' at appropriate pos in selected col    
    def playerMove(self, colNum):
        
        colFull = False        
        targetCol = self.boardArr[:,colNum]

        try:
            highestDot = list(targetCol).index('.') # location of highest empty space   
        except:
            colFull = True
        
        if highestDot == 0: colFull = True
        
        if colFull:
            print 'Selected Column is full'
            return False
               
        self.boardArr[highestDot-1, colNum] = '0'
        
        return self.boardArr
        
    # updates board by adding 'X' at appropriate pos in selected col   
    def AIMove(self, colNum):
                
        colFull = False        
        targetCol = self.boardArr[:,colNum]

        try:
            highestDot = list(targetCol).index('.') # location of highest empty space   
        except:
            colFull = True
        
        if highestDot == 0: colFull = True
        
        if colFull:
            print 'Selected Column is full'
            return False
               
        self.boardArr = self.boardArr[highestDot-1, colNum] = 'X'

        return self.boardArr
        
    def score()
    
###############################################################################
class node():
    
    def __init__(self, board):
        
        self.boardArr = boardArr
    
    def successors(self):
        
        
        
        
        
    

# calc cost for each successor function
# create successor function which lists out possible moves for opponent
# add alpha beta pruning
# goal test function -- tells if state is terminal


def minimax(depth):

    print 'Here is the initial board: \n'
 
    initBoard = board([9,9]).printBoard()
    
    targetCol = input('Please enter column to drop checkers in: ')
    
    



