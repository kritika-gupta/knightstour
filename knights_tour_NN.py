# Kritika Gupta
# Knight's Tour implemented by a Neural Network
import pygame
import sys
import numpy as np
from pygame.locals import *

import random

size = 8
num = 8*size*size
Max_nIter = 50

numNeurons = 0

DX = [1, 2, 2, 1, -1, -2, -2, -1]
DY = [-2, -1, 1, 2, 2, 1, -1, -2]


class Cell():
    def __init__(self, r, c):
        self.row = r
        self.col = c
        self.vec = []
    def push(self, x):
        self.vec.append(x)
    def getVec(self):
        return self.vec
    def getSize(self):
        return len(self.vec)
    def pull(self, x):
        return self.vec[x]



class Neuron():
    def __init__(self):
       
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0     
        self.state, self.output = 0, 0
        self.adj = []
        
    def setpos(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        
    def setOutput(self, x):
        self.output = x
        
    def setSt(self, x):
        self.state = x
        
    def getpos(self):
        return [self.x1, self.y1, self.x2, self.y2]
    
    def getState(self):
        return self.state
    
    def getOutput(self):
        return self.output
    
    def push(self, x):
        self.adj.append(x)
        
    def getAdj(self):
        return self.adj
    


# create all neurons and cells
NeuronList = [Neuron() for i in range(num)]
CellList = [[Cell(i, j) for j in range(size)] for i in range(size)]
next_state = [0 for i in range(num)]
next_output = [0 for i in range(num)]
label = [[0 for j in range(size)] for i in range(size)]
Final_Check = False
adj = [[[] for j in range(size)] for i in range(size)]




def initialize():
    global numNeurons, NeuronList, CellList, next_state, next_output, label, Final_Check, adj
    numNeurons = 0
    for x1 in range(size):
        for y1 in range(size):
            i = x1 + y1*size
            for t in range(8):
                x2 = x1 + DX[t]
                y2 = y1 + DY[t]

                if (x2>=0) and (x2<size) and (y2>=0) and (y2<size):
                    j = x2 + y2*size

                    if i<j:
                        
                        CellList[x1][y1].push(numNeurons)
                        CellList[x2][y2].push(numNeurons)
                        NeuronList[numNeurons].setpos(x1, y1, x2, y2)
                        numNeurons = numNeurons+1

    #for i in range(num):
        #print NeuronList[i].getAdj()

    for x in range(size):
        for y in range(size):
            for u in range(CellList[x][y].getSize()):
                i = CellList[x][y].pull(u)
                
                for v in range(u+1, CellList[x][y].getSize()):
                    j = CellList[x][y].pull(v)
                    NeuronList[i].push(j)
                    NeuronList[j].push(i)



def randomize_outputs():
    global numNeurons, NeuronList, CellList, next_state, next_output, label, Final_Check, adj
    for i in range(numNeurons):
        
        NeuronList[i].setSt(0)
        NeuronList[i].setOutput(random.randint(0, 1))




def next_gen():
    global numNeurons, NeuronList, CellList, next_state, next_output, label, Final_Check, adj
    for i in range(numNeurons):
        next_state[i] = NeuronList[i].getState() + 4 - NeuronList[i].getOutput()
        
       

        for j in range(len(NeuronList[i].getAdj())):
            v = NeuronList[i].getAdj()[j]
            next_state[i] = next_state[i] - NeuronList[v].getOutput()
            
        if next_state[i] < 0:
            next_output[i] = 0
        else:
            if next_state[i] > 3:
                next_output[i] = 1
            else:
                next_output[i] = NeuronList[i].getOutput()
        


def change_neurons():
    global numNeurons, NeuronList, CellList, next_state, next_output, label, Final_Check, adj
    nChanges, nActive = 0, 0

    for i in range(numNeurons):
        if next_state[i]!=NeuronList[i].getState():
            nChanges = nChanges + 1
        NeuronList[i].setSt(next_state[i])
        NeuronList[i].setOutput(next_output[i])
        nActive = nActive + NeuronList[i].getOutput()
    
    return [nChanges, nActive]


def check_deg():
    global numNeurons, NeuronList, CellList, next_state, next_output, label, Final_Check, adj

    degree = [[0 for j in range(size)] for i in range(size)]
    for i in range(numNeurons):
        if NeuronList[i].getOutput()==1:
            pos = NeuronList[i].getpos()
            degree[pos[0]][pos[1]] = degree[pos[0]][pos[1]] + 1
            degree[pos[2]][pos[3]] = degree[pos[2]][pos[3]] + 1
    for i in range(size):
        for j in range(size):
            if degree[i][j]!=2:
                return False
    return True



def visit(i, j, count):
    global numNeurons, NeuronList, CellList, next_state, next_output, label, Final_Check, adj


    label[i][j] = count
    if count==size*size:
        if i*j!=2:
            Final_Check = False
    for t in range(len(adj[i][j])):
        u = adj[i][j][t][0]
        v = adj[i][j][t][1]
        
        if label[u][v]==0:
            visit(u, v, count+1)
            return
        


def check_conn():
    global numNeurons, NeuronList, CellList, next_state, next_output, label, Final_Check, adj

    label = [[0 for j in range(size)] for i in range(size)]
    adj = [[[] for j in range(size)] for i in range(size)]
    
    for i in range(numNeurons):

        
        if NeuronList[i].getOutput()==1:
            pos = NeuronList[i].getpos()
            adj[pos[0]][pos[1]].append((pos[2], pos[3]))
            adj[pos[2]][pos[3]].append((pos[0], pos[1]))
            

    
    Final_Check = True
    nComp = 0

    for i in range(size):
        for j in range(size):
            if label[i][j]==0:
                nComp = nComp + 1
                visit(i, j, 1)

    return nComp       



def printSoln():
    global numNeurons, NeuronList, CellList, next_state, next_output, label, Final_Check, adj

    print "-------------------"
    print size
    for l in label:
        print l


def process():
    global numNeurons, NeuronList, CellList, next_state, next_output, label, Final_Check, adj

    even = False
    nTimes = 0
    
    while(True):
        nTimes = nTimes + 1
        print "\nTime ", nTimes, " : \n"
        
        randomize_outputs()
        
        print "Local Optimization.\n"
        nIter = 0
        while(True):
            next_gen()
            info = change_neurons()
            nChanges = info[0]
            nActive = info[1]
            #print "Num of changes = ", nChanges
            if nChanges==0:
                break
            if check_deg():
                even = True
                break
            
            nIter = nIter + 1
            
            if nIter==Max_nIter:
                break
        
        if even:
            print "All original cells have degree 2\n"
            
            nComp = check_conn()
            print "Number of connected components : ", nComp, "\n"
            if nComp==1:
                if Final_Check:
                    print "\nFound Solution     \n"
                    printSoln()
                    break
                else:
                    print "The soln cannot pass the final check\n"
                
            

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
        for x in range(50050000):  # Loop To Control Animation Speed
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


initialize()
#randomize_outputs()
#for i in range(numNeurons):
        #print NeuronList[i].getAdj()
process()
boardSize = size
boardConfig = label
orderedList = [None] * (boardSize * boardSize)
for row in range(boardSize):
    for col in range(boardSize):
        orderedList[int(boardConfig[row][col]-1)] = [row, col]

plotKnightsTour(boardSize, orderedList)

