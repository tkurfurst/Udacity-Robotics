
colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']

motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7
p_move = 0.8


"""
### START - VIDEO TEST ###

colors = [['green', 'green', 'green'],
          ['green', 'red', 'red'],
          ['green', 'green', 'green']]


moves
[0, 1] - right, [0, -1] - left
[1, 0] - down, [-1, 0] - up


# motions = [[0,0], [1,0],[0,-1]]
# measurements = ['red', 'green','red']

motions = [[0,0], [0, 1]]
measurements = ['red', 'red']

p_move = 0.5 #0.8
sensor_right = 1.0 # 0.8


### END - VIDEO TEST ###
"""

def show(p):
    for i in range(len(p)):
    	print '[',
    	for j in range(len(p[i])):
        	print '%4.5f' %(p[i][j]*100),
        print ']'
#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

p = []

def uniform_dist(target, default=0.0):
	rows = len(target)
	columns = len(target[0])
	if  default:
		entry = default
	else:
		entry = 1.0/(float(rows)*float(columns))
	p = [[entry for i in range(columns)] for j in range(rows)]
	return p

p=uniform_dist(colors)

def sense(p, colors, Z):
	sum = 0.0
	rows = len(p)
	columns = len(p[0])
	for row in range(rows):
		for column in range(columns):
			hit = (Z == colors[row][column])
			p[row][column] = p[row][column] * (hit * sensor_right + (1-hit) * (1-sensor_right))
			sum += p[row][column]
	for row in range(rows):
		for column in range(columns):
   			p[row][column] = p[row][column]/sum
	return p


def move(p, U):
   	
   	q = uniform_dist(p, default=0.0)
   	rows = len(p)
	columns = len(p[0])
	
	v = U[0] # vertical motion
	h = U[1] # horizontal motion
	
	for row in range(rows):
		for column in range(columns):
			old = p[row][column]
			s = p_move * (p[(row-v) % rows][(column-h) % columns])
			s = s + (1-p_move) * (p[(row) % rows][(column) % columns])
			q[row][column] = s
	p = q
	return p

print 'original'
show(p)
for k in range(len(measurements)):
    p = move(p, motions[k])
    p = sense(p, colors, measurements[k])
    print 'iteration'
    show(p)
print 'final'

#Your probability array must be printed 
#with the following code.

show(p)

test = uniform_dist(colors, default=0.0)
print 'test'
show(test)