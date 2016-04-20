# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# takes no input and RETURNS two grids. The
# first grid, value, should contain the computed
# value of each cell as shown in the video. The
# second grid, policy, should contain the optimum
# policy for each cell.
#
# Stay tuned for a homework help video! This should
# be available by Thursday and will be visible
# in the course content tab.
#
# Good luck! Keep learning!
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.
#
# NOTE: Please do not modify the values of grid,
# success_prob, collision_cost, or cost_step inside
# your function. Doing so could result in your
# submission being inappropriately marked as incorrect.

# -------------
# GLOBAL VARIABLES
#
# You may modify these variables for testing
# purposes, but you should only modify them here.
# Do NOT modify them inside your stochastic_value
# function.

"""
# TEST- grid

grid = [[0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]

goal = [0, len(grid[0])-1]
cost_step = 1
collision_cost = 100
success_prob = 0.5
"""

# FAILED - grid

grid = [[0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0]]

goal = [0, 6]
cost_step = 1
collision_cost = 100
success_prob = 0.8


"""
# ORIGINAL - grid

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]

cost_step = 1               
collision_cost = 100 
success_prob = 0.5                      
goal = [0, len(grid[0])-1] # Goal is in top right corner
"""

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

                     

############## INSERT/MODIFY YOUR CODE BELOW ##################
#
# You may modify the code below if you want, but remember that
# your function must...
#
# 1) ...be called stochastic_value().
# 2) ...NOT take any arguments.
# 3) ...return two grids: FIRST value and THEN policy.

def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob

    change = True
    
    while change:
    
    	change = False
    	
    	for x in range(len(grid)):
    		for y in range(len(grid[0])):
	    		if x == goal[0] and y == goal[1]:
	    			if value[x][y] > 0:
	    				value[x][y] = 0
	    				policy[x][y] = '*'
	    				change = True
	    		elif grid[x][y] == 0: 
					for n in range(len(delta)):
						v2 = cost_step
						for var in [-1,0,1]:
							x2 = x + delta[(n+var) % 4][0]
							y2 = y + delta[(n+var) % 4][1]
							#print x, y, delta_name[(n+var) %4], x2, y2
							##############
							# test for neighbour as valid, collision or off-grid and adjust accordingly
							# case: collision
							if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 1 and var == 0:
								v2 = v2 + collision_cost * success_prob
								#print 'collision 0', v2
							elif x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 1 and var != 0:
								v2 = v2 + collision_cost * failure_prob
								#print 'collision 1', v2
							# case: off-grid
							if (x2 < 0 or x2 >= len(grid) or y2 < 0 or y2 >= len(grid[0])) and var == 0:
								v2 = v2 + collision_cost * success_prob
								#print 'off-grid 0', v2
							elif (x2 < 0 or x2 >= len(grid) or y2 < 0 or y2 >= len(grid[0])) and var != 0:
								v2 = v2 + collision_cost * failure_prob
								#print 'off-grid 1', v2
							# case: valid
							if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0 and var == 0:
								v2 = v2 + value[x2][y2] * success_prob
								#print 'valid 0', v2
							elif x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0 and var != 0:
								v2 = v2 + value[x2][y2] * failure_prob
								#print 'valid 1', v2
							#############
						#print v2, value[x][y]
						if v2 < value[x][y]:
							value[x][y] = v2
							policy[x][y] = delta_name[n]
							change = True
    return value, policy


value, policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)

for row in range(len(value)):
	print value[row]

for row in range(len(policy)):
	print policy[row]
