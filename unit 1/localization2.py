# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'

def localize(colors,measurements,motions,sensor_right,p_move):
    
    
    if len(measurements) != len(motions):
      raise ValueError, "error in size of measurements/motions vector"
    
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]
    #print("initial p")
    #show(p)
    
    # >>> Insert your code here <<<
    
    def move(p, motion, p_move):
        
        rows = len(p)
        columns = len(p[0])
        # initializes p_updated to a uniform distribution over a grid of the same dimensions as p
        p_updated = [[0.0 for column in range(columns)] for row in range(rows)]       
        
        #print("before move")
        #show(p) 
        
        # U is a move vector of the form U = [dx, dy]
        dy = motion[0] # vertical motion
        dx = motion[1] # horizontal motion
        #print (dy, dy, p_move)
        p_stay = 1 - p_move
        for row in range(rows):
          for column in range(columns):
            p_updated[row][column] = p_move * (p[(row-dy) % rows][(column-dx) % columns]) + p_stay * (p[(row) % rows][(column) % columns])
        #print("after move")
        #show(p_updated)
        return p_updated

    def sense(p, colors, measurement, sensor_right):
        sum = 0.0
        rows = len(p)
        columns = len(p[0])
        #print("before sense")
        #show(p)
        sensor_wrong = 1 - sensor_right
        for row in range(rows):
          for column in range(columns):
            #print(sum)
            hit = (measurement == colors[row][column])
            nohit = (measurement != colors[row][column])
            p[row][column] = p[row][column] * (hit * sensor_right + nohit * sensor_wrong)
            sum += p[row][column]
        for row in range(rows):
          for column in range(columns):
              p[row][column] = p[row][column]/sum
        #print("after sense")
        #show(p)
        return p  
    
    for k in range(len(measurements)):
        p = move(p, motions[k], p_move)
        p = sense(p, colors, measurements[k], sensor_right)

    
    return p
"""
def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'
"""

#############################################################
# For the following test case, your output should be 
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]

motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

measurements = ['G','G','G','G','G']

"""
colors = [['G','G','G'],
          ['G','R','R'],
          ['G','G','G']]

motions = [[0,0], [0,1]]
measurements = ['R', 'R']
"""

p = localize(colors,measurements,motions,sensor_right = 0.7, p_move = 0.8)
#print("FINAL")
show(p) # displays your answer

