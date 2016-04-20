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

grid_test = [[0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]

goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 20] # [2, 1, 20] the cost field has 3 values: right turn, no turn, left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D() should return the array
# 
# [[' ', ' ', ' ', 'R/R', '#', 'R/L'],
#  [' ', ' ', ' ', '#/R', ' ', '#'],
#  ['*', '#', '#', '#/L', '#', 'R/L'],
#  [' ', ' ', ' ', '#/L', ' ', ' '],
#  [' ', ' ', ' ', '#/L', ' ', ' ']]
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

# the action field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']


# ----------------------------------------
# modify code below
# ----------------------------------------



def optimum_policy2D():
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
	
	return policy2D, policy, value # Make sure your function returns the expected grid.

# comment out for final submission

policy2D, policy, value = optimum_policy2D()

"""
value = [[[999 for col in range(len(grid[0]))] for row in range(len(grid))] for orient in range(4)]
policy = [[[999 for col in range(len(grid[0]))] for row in range(len(grid))] for orient in range(4)]
policy2D = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
"""
"""
print '\nvalues:\n'
for orient in range(4):
    print 'orient: %s\n' %forward_name[orient]
    for row in range(len(value[orient])):
        print value[orient][row]
    print '\n'
    for row in range(len(policy[orient])):
        print policy[orient][row]
    print '\n'
"""
#print '\npolicy:\n'
for row in range(len(policy2D)):
    print policy2D[row]



"""

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


"""