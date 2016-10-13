import grid

# global current state of the backtrack
partialPath = []
visited = []
solutionFound = False
bestDistance = -1
bestPath = []
maze = None
endLocation = (-1,-1)

# profiling
backtrackingNodes = 0

def main():
    global maze
    global bestPath
    global bestDistance
    mazeFileName = raw_input("Enter file name containing the maze: ")
    print 'The maze read from file',mazeFileName, 'is:'
    (maze,start) = ReadMaze(mazeFileName)
    print maze
    print 'Starting Location:', start,'\n'
    print '\nAttempting to Solve the Maze'
    results = SolveMaze(start)
    print 'This maze was',results,'\n'
    if results == 'Solved':
        print 'The best distance:', bestDistance
        print 'The best path was:', bestPath
        for step in visited:
            maze[step[0]][step[1]] = '.'
        for step in bestPath:
            maze[step[0]][step[1]] = '+'
        maze[endLocation[0]][endLocation[1]] = 'T'
        maze[start[0]][start[1]] = 'P'
    print maze


def SolveMaze(start):
    """Attempts to find a path from 'P' at the start location to the
       'T' by following the paths (blanks)"""


    def backtrack(row, column, distance ):
        global partialPath
        global solutionFound
        global bestDistance
        global bestPath
        global endLocation
        global backtrackingNodes
        global visited

        visited.append((row, column))
        backtrackingNodes += 1

        moves = possibleNextMoves(row, column, maze)
        for move in moves:
            moveRow = move[0]
            moveCol = move[1]
            if promising(moveRow, moveCol, distance):

                if maze[moveRow][moveCol] == 'T':  # a solution is found
                    if (not solutionFound) or distance+1 < bestDistance: # check if its best
                        bestDistance = distance+1
                        bestPath = [] + partialPath
                        bestPath.append((moveRow,moveCol))
                        endLocation = (moveRow, moveCol)
                        solutionFound = True
                else:
                    # update global "current state" for child before call
                    distance += 1
                    partialPath.append((moveRow,moveCol))
                    maze[moveRow][moveCol] = '.'
                   
                    backtrack(moveRow, moveCol, distance)
                    
                    # undo change to global "current state" after backtracking
                    distance -= 1
                    partialPath.pop()
                    maze[moveRow][moveCol] = ' '
    # end def backtrack
        

    def promising(moveRow, moveCol, distance):
        if maze[moveRow][moveCol] == 'T':
            return True
        else: 
            min_left = abs(moveRow - endLocation[0]) + abs(moveCol - endLocation[1])  
            if solutionFound and distance + min_left + 1>= bestDistance:
                return False
            else:
                return True    

        ##### ADD CODE HERE for Part A (c) #####




    def possibleNextMoves(currentRow, currentCol, maze):
        """Returns legal next moves in nextMoveLocations list """
        nextMoveLocations = []
        if currentRow-1 >= 0 and maze[currentRow-1][currentCol] in ' T': # Up
            nextMoveLocations.append((currentRow-1,currentCol))
        if currentCol+1 < maze.getWidth() \
             and maze[currentRow][currentCol+1] in ' T': # Right
            nextMoveLocations.append((currentRow,currentCol+1))
        if currentRow+1 < maze.getHeight() \
             and maze[currentRow+1][currentCol] in ' T': # Down
            nextMoveLocations.append((currentRow+1,currentCol))
        if currentCol-1 >=0 and maze[currentRow][currentCol-1] in ' T': # Left
            nextMoveLocations.append((currentRow,currentCol-1))
        return nextMoveLocations

        

    # set-up initial "current state" information
    global partialPath
    global solutionFound
    global bestDistance
    global bestPath
    global maze
    global endLocation
    global backtrackingNodes
    backtrackingNodes = 0

    partialPath = []
    solutionFound = False
   
    backtrack(start[0], start[1], 0)
    if solutionFound:
        return "Solved"
    else:
        return "Unsolved"
    
    
def ReadMaze(mazeFileName):
    """Read a maze file with the following format:
        First Line:  integer number of rows
        Second Line: integer number of columns
        Starting on line three will be a "picture" of the maze with:
        '*' character marking a barrier,
        'P' character marking the starting Parking lot,
        'T' character marking the target mountain Top, and
        ' ' (blank character marking a path"""

    mazeFile = open(mazeFileName, 'r')
    numberOfRows = int(mazeFile.readline().rstrip('\n'))
    numberOfColumns = int(mazeFile.readline().rstrip('\n'))

    maze = grid.Grid(numberOfRows,numberOfColumns, 'X')
    for row in xrange(numberOfRows):
        line = mazeFile.readline()
        for column in xrange(numberOfColumns):
            maze[row][column] = line[column]
            if line[column] == 'P':
                startLocation = (row, column)

    return (maze,startLocation)


main()
print "Number of Backtracking Nodes:", backtrackingNodes
