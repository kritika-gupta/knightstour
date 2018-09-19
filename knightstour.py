#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import sys
import numpy as np
from pygame.locals import *


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


def plotKnightsTour(boardSize, orderedList):
    horse = pygame.image.load("knightPiece.png")

    # Initialize window size and title:
    pygame.init()
    window = pygame.display.set_mode((32 * boardSize, 32 * boardSize))
    pygame.display.set_caption("Knight's Tour")
    background = pygame.image.load("chessBoard.png")
    index = 0

    # Text:
    font = pygame.font.SysFont("Ubuntu", 20, bold=True)
    text = []
    surface = []

    while True:
                # Fill background:
        window.blit(background, (0, 0))

        if index < boardSize * boardSize:
            window.blit(
                horse, (orderedList[index][0] * 32, orderedList[index][1] * 32))
            text.append(font.render(str(index+1), True, (255, 255, 255)))
            surface.append(text[index].get_rect())
            surface[index].center = (
                orderedList[index][0]*32+16, orderedList[index][1]*32+16)
            index += 1
        else:
            window.blit(
                horse, (orderedList[index-1][0]*32, orderedList[index-1][1]*32))
        for x in range(10050000):  # Loop To Control Animation Speed
            pass
        # Check events on window:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 27:
                    pygame.quit()
                    sys.exit()

        for i in range(index):
            window.blit(text[i], surface[i])

        # Update window:
        pygame.display.update()


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
currRow = startRow-1
currCol = startCol-1
currMove = [startRow, startCol]

# Represent Chess Board As 2D Array Initialized With Zeros
boardConfig = np.zeros([boardSize, boardSize])
# Mark Initial Position As The First Move
boardConfig[currRow][currCol] = 1

for i in range(2, boardSize*boardSize+1):
    currMove[0] = currRow
    currMove[1] = currCol
    getNextMove(currMove, moveCombos, boardConfig, boardSize)
    currRow = currMove[0]
    currCol = currMove[1]
    boardConfig[currRow][currCol] = i

if solutionExists(boardConfig, boardSize):
    print(boardConfig)
    orderedList = [None] * (boardSize * boardSize)
    for row in range(boardSize):
        for col in range(boardSize):
            orderedList[int(boardConfig[row][col]-1)] = [row, col]
    plotKnightsTour(boardSize, orderedList)
else:
    # print(boardConfig)
    print("Failed To Obtain Solution")
