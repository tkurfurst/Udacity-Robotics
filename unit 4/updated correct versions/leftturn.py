# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D() below.
#
# You are given a car in a grid with initial state
# init = [x-position, y-position, orientation]
# where x/y-position is its position in a given
# grid and orientation is 0-3 corresponding to 'up',
# 'left', 'down' or 'right'.
#
# Your task is to compute and return the car's optimal
# path to the position specified in `goal'; where
# the costs for each motion are as defined in `cost'.

# EXAMPLE INPUT:

# grid format:
#     0 = navigable space
#     1 = occupied space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 20] # the cost field has 3 values: right turn, no turn, left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D() should return the array
# 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
#
# ----------


# there are four motion directions: up/left/down/right
# increasing the index in this array corresponds to
# a left turn. Decreasing is is a right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # do right
forward_name = ['up', 'left', 'down', 'right']

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']


# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D(grid,init,goal,cost):
    value = [[[999 for col in range(len(grid[0]))] for row in range(len(grid))] for orient in range(4)]
    policy = [[[' ' for col in range(len(grid[0]))] for row in range(len(grid))] for orient in range(4)]
    policy2D = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]

    change = True

    #count = 0

    while change:

        change = False

        for orient in range(4):
            for x in range(len(grid)):
                for y in range(len(grid[0])):
                    #count += 1
                    #print 'orient: %d, x: %d, y: %d' %(orient,x,y)
                    # if goal position set value to 0, policy to *
                    if x == goal[0] and y == goal[1]:
                        if value[orient][x][y] > 0:
                            value[orient][x][y] = 0
                            policy[orient][x][y] = '*'
                            policy2D[x][y] = '*'
                            change = True
                    # if not goal position and not obstacle
                    elif grid[x][y] == 0:
                        # explore all neighbours/actions that lead from current position
                        for a in range(len(action)):
                            o2 = (orient + action[a]) % 4
                            x2 = x + forward[o2][0]
                            y2 = y + forward[o2][1]
                            #print 'old: [%d,%d,%s] action: %s new [%d,%d,%s]' %(x,y,forward_name[orient], action_name[a],x2,y2,forward_name[o2])
                            # test to ensure actions result in grid and not obstacle
                            if (x2 >= 0) and (x2 < len(grid)) and (y2 >= 0) and (y2 < len(grid[0])) and (grid[x2][y2] == 0):
                                #print 'VALID: [%d,%d]' %(x2,y2)
                                #print 'y: %d, lenY: %d' %(y, len(grid[0]))
                                # print 'old: [%d,%d,%s] action: %s new [%d,%d,%s]' %(x,y,forward_name[orient], action_name[a],x2,y2,forward_name[o2])
                                # candidate new value (x,y) == value from neighbours (x2,y2) + cost_step
                                v2 = value[o2][x2][y2] + cost[a]
                                #print 'v2:%d' %v2
                                # if candidate value less than current value then this is an improvement and potential path
                                if v2 < value[orient][x][y]:
                                    change = True
                                    value[orient][x][y] = v2
                                    #policy[orient][x][y] = action_name[a]
                                    policy[orient][x][y] = action[a]
    
    x, y, o = init[0], init[1], init[2]
    #print 'TEST'
    
    while x != goal[0] or y != goal[1]:
        #print 'x: %d, y:%d' %(x,y)
        a = policy[o][x][y]
        policy2D[x][y] = action_name[a+1]
        o = (o + a) % 4
        x = x + forward[o][0]
        y = y + forward[o][1]
        #print x,y, goal[0], goal[1]
        #print (x != goal[0] and y != goal[1])
        #print count
        
    return policy2D # Make sure your function returns the expected grid.

policy = optimum_policy2D(grid,init,goal,cost)

for row in range(len(policy)):
    print policy[row]



