#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np


def isLegalMove(x, y, board, boardSize):
    return (x >= 0 and y >= 0 and x < boardSize and y < boardSize and board[x][y] == 0)


def getDegree(x, y, moveCombos, board, boardSize):
    degree = 0
    for i in range(8):
        if isLegalMove(x + moveCombos[i][0], y + moveCombos[i][1], board, boardSize):
            degree += 1
    return degree


def getNextMove(currMove, moveCombos, board, boardSize):
    x = currMove[0]
    y = currMove[1]
    minDegree = 9
    for i in range(8):
        nextX = x + moveCombos[i][0]
        nextY = y + moveCombos[i][1]
        nextDegree = getDegree(nextX, nextY, moveCombos, board, boardSize)
        if isLegalMove(nextX, nextY, board, boardSize) and nextDegree < minDegree:
            currMove[0] = nextX
            currMove[1] = nextY
            minDegree = nextDegree
    return


def solutionExists(boardConfig, boardSize):
    for row in range(boardSize):
        for col in range(boardSize):
            if boardConfig[row][col] == 0:
                return False
    return True


# List Of All Possible Move Combinations For A Knight From An Ideal Cell
moveCombos = [[2, 1], [2, -1], [1, 2], [1, -2],
              [-1, 2], [-1, -2], [-2, 1], [-2, -1]]

# Initialize Problem Variables From User Input
boardSize = int(input("Enter Dimension For Square Board: "))
# Row Co-ordinate For Piece To Start Tour
startRow = int(
    input("Enter Row Number Of Starting Cell (1-N): ")) % boardSize
# Column Co-Oridinate For Piece To Start Tour
startCol = int(
    input("Enter Column Number Of Starting Cell (1-N): ")) % boardSize

# Set Current Row, Column And Move To Staring Cell
currRow = startRow
currCol = startCol
currMove = [startRow, startCol]

boardConfig = np.zeros([boardSize, boardSize])
moveNumber = 1  # Starting Cell Is Considered To Be Move One
boardConfig[currRow][currCol] = moveNumber
moveNumber += 1

for i in range(boardSize*boardSize):
    currMove[0] = currRow
    currMove[1] = currCol
    getNextMove(currMove, moveCombos, boardConfig, boardSize)
    currRow = currMove[0]
    currCol = currMove[1]
    boardConfig[currRow][currCol] = moveNumber
    moveNumber += 1

boardConfig[currRow][currCol] -= 1  # What Does This Do?
