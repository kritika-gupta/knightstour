import numpy as np
import random

N = 8

# possible x and y coordinates for next position
x_cord = np.array([1,1,2,2,-1,-1,-2,-2])
y_cord = np.array([2,-2,1,-1,2,-2,1,-1])

# define the limits of the board
def limits(x, y):
    return ((x>=0 and y>=0) and (x < N and y < N))

# check if a square is valid and is also empty
def isValid(board, x, y):
    return limits(x,y) and board[x,y] < 0


# return the number of empty and valid adjacent squares
def getDegree(board, x, y):
    count = 0
    for i in range(N):
        if isValid(board, x+x_cord[i], y+y_cord[i]):
            count = count+1
    return count


# pick the next move
def nextMove(board, x, y):
    min_degree = N+1
    min_degree_index = -1
    start =  random.randint(0,N-1)
    for count in range(N):
        i = (start + count)%N
        x1 = x + x_cord[i]
        y1 = y + y_cord[i]
        if isValid(board, x1, y1):
            deg = getDegree(board, x1, y1)
            if deg < min_degree:
                min_degree_index = i
                min_degree = deg

    # if no next square
    if min_degree_index == -1:
        print "No next square"
        return (-1,-1)

    # shift coordinates
    x1 = x + x_cord[min_degree_index]
    y1 = y + y_cord[min_degree_index]

    #next move
    board[x1, y1] = board[x,y]+1
    print "Next move set as",x1,y1
    return (x1, y1)




# display the chess board
def showBoard(board):
    print "\n\n",board,"\n\n"


# check if tour will be closed in the next move
def checkClosed(x, y, xx, yy):
    for i in range(N):
        if (x+x_cord[i] == xx) and (y + y_cord[i] == yy):
            return True
    return False

# generates the legal moves
def findKnightsTour():
    changes = 0;
    # generate empty chessboard with -1 s filled
    board = np.full((N,N), -1, dtype = int)
    #x0, y0 =  random.randint(0,N-1), random.randint(0,N-1)
    x0, y0 = 0, 4    
    print "Starting position is ", x0, " ", y0
    x, y = x0, y0
 
    # set starting point as 1
    board[x,y] = 1

    for i in range(N*N):
        (x, y) = nextMove(board, x, y)
        if (x,y) == (-1,-1):
            print "returned (-1,-1)\n"
            return False
        else:
            changes = changes + 1
            print "Changes = ", changes
            showBoard(board)

    #if checkClosed(x,y,x0,y0)==False:
        #return False

    print "Displaying board\n"
    showBoard(board)
    return True

findKnightsTour()
'''
while findKnightsTour()==False:
    pass
'''
