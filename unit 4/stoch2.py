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

grid_orig = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]

grid = [[0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0]]
       
goal = [0, len(grid[0])-1] # Goal is in top right corner


delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

success_prob = 0.5 #0.5                      
failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
collision_cost = 100                    
cost_step = 1        
                     

############## INSERT/MODIFY YOUR CODE BELOW ##################
#
# You may modify the code below if you want, but remember that
# your function must...
#
# 1) ...be called stochastic_value().
# 2) ...NOT take any arguments.
# 3) ...return two grids: FIRST value and THEN policy.

def stochastic_value():
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

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

							if var == 0:
								prob = success_prob
							else:
								prob = failure_prob
							
							if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
								if grid[x2][y2] == 0:
									v2 += value[x2][y2] * prob
								else:
									v2 += collision_cost * prob
							else:
									v2 += collision_cost * prob
						if v2 < value[x][y]:
							value[x][y] = v2
							policy[x][y] = delta_name[n]
							change = True
    return value, policy

    
# REMOVE FOR SUBMISSION

value, policy = stochastic_value() 


#value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
#policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

for row in range(len(value)):
	print '[',
	for col in range(len(grid[0])):
		print '%.2f' %value[row][col],
	print ']'	
for row in range(len(policy)):
	print policy[row]



