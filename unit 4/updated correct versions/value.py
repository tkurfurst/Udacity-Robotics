# ----------
# User Instructions:
# 
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal. 
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

grid_o = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 1, 0, 1, 0]]

goal = [len(grid)-1, len(grid[0])-1]

cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def compute_value(grid,goal,cost):
    # ----------------------------------------
    # insert code below
    # ----------------------------------------
    
    # make sure your function returns a grid of values as 
    # demonstrated in the previous video.
    # implement recursively f(x,y) = min x',y' f(x',y') + 1

    value = [[99 for col in range(len(grid[0]))] for row in range(len(grid))]
    
    closed = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
    
    init = goal
    
    x = init[0]
    y = init[1]

    value[x][y] = 0

    open = [[x, y]]

    finished = False    # flag that is set value grid is complete
    #resign = False      # flag set if we can't find expand
    #count = 0
    
    while not finished:
        if len(open) == 0:
            finished = True
            return value
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[0]
            y = next[1]
            for i in range(len(delta)):
                x2 = x + delta[i][0]
                y2 = y + delta[i][1]
                if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                    if grid[x2][y2] == 0:
                        if value[x][y] + 1 < value[x2][y2]:
                            value[x2][y2] = value[x][y] + 1
                            open.append([x2, y2])
                        #closed[x2][y2] = 1
                    elif grid[x2][y2] == 1:
                        value[x2][y2] = 99
    return value

values = compute_value(grid,goal,cost)

for i in range(len(values)):
    print values[i] 