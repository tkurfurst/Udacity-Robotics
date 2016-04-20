# ----------
# User Instructions:
# 
# Create a function optimum_policy() that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell.
# 
# un-navigable cells must contain an empty string
# WITH a space, as shown in the previous video.
# Don't forget to mark the goal with a '*'

# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy():
    
    value = [[99 for col in range(len(grid[0]))] for row in range(len(grid))]
    
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    policy[len(grid)-1][len(grid[0])-1] = '*'
    
    change = True

    while change:
    
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                
                # if goal position set value to 0, policy to *
                if x == goal[0] and y == goal[1]:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        policy[x][y] = '*'
                        change = True

                # if not goal position and not obstacle
                elif grid[x][y] == 0:
                    
                    # explore all neighbours/actions that lead from current position
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        # test to ensure actions result in grid and not obstacle
                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            # candidate new value (x,y) == value from neighbours (x2,y2) + cost_step
                            v2 = value[x2][y2] + cost_step
                            # if candidate value less than current value then this is an improvement and potential path
                            if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2
                                policy[x][y] = delta_name[a]
                                
    return policy, value # Make sure your function returns the expected grid.

policy, value = optimum_policy()

print '\nvalues:\n'
for row in range(len(value)):
    print value[row]

print '\npolicy:\n'
for row in range(len(policy)):
    print policy[row]


