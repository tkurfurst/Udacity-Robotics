# ----------
# User Instructions:
# 
# Create a function compute_value() which returns
# a grid of values. Value is defined as the minimum
# number of moves required to get from a cell to the
# goal. 
#
# If it is impossible to reach the goal from a cell
# you should assign that cell a value of 99.

# ----------
"""
grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
"""
grid = [[0,0],
		[0,0]]

occupied = 1
empty = 0

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# insert code below
# ----------------------------------------

def compute_value():
	value = [[99 for col in range(len(grid[0]))] for row in range(len(grid))]

	def neighbour(cell):
		n = []
		x, y = cell[0], cell[1]
		if grid[x][y] == occupied:
			return []
		for move in delta:
			xnext = x + move[0]
			ynext = y + move[1]
			if xnext >= 0 and xnext <= len(grid)-1 and ynext >= 0 and ynext <= len(grid[0])-1:
				next = grid[xnext][ynext]
				if next == empty:
					n.append([xnext,ynext])
		return n

	def isgoal(cell):
		return True if cell == goal else False

	def dynamic(cell):
		x = cell[0]
		y = cell[1]
		empty = -1
		minval = 1e6
		d = value[x][y]
		if isgoal(cell):
			return 0
		elif d == empty:
			for n in neighbour([x, y]):
				v = dynamic([n[0],n[1]]) 
				if v < minval:
					minval = v
		else:
			return d
	
	change = True

	while change == True:
		change = False		
		for row in range(len(grid)):
			for col in range(len(grid[0])):
				minval = 1e6
				if isgoal([row,col]):
					if value[row][col] > 0:
						value[row][col] = 0
						print value[row][col]
						change = True
				elif grid[row][col] == 0:
					for n in neighbour([row, col]):
						if value[n[0]][n[1]] < value[row][col]:
							value[row][col] = value[n[0]][n[1]] + cost_step
							print value[row][col]
							change = True

	return value #make sure your function returns a grid of values as demonstrated in the previous video.


value = compute_value()

for row in range(len(value)):
	print value[row]


"""
for row in range(len(value)):
	print value[row]
value = compute_value()

def neighbour(cell):
	n = []
	x, y = cell[0], cell[1]
	if grid[x][y] == occupied:
		return []
	for move in delta:
		xnext = x + move[0]
		ynext = y + move[1]
		if xnext >= 0 and xnext <= len(grid)-1 and ynext >= 0 and ynext <= len(grid[0])-1:
			next = grid[xnext][ynext]
			if next == empty:
				n.append([xnext,ynext])
	return n

#print neighbour([2,2])

value = [[-1 if grid[row][col] == 0 else 99 for col in range(len(grid[0]))] for row in range(len(grid))]
value[len(grid)-1][len(grid[0])-1] = 0

def isgoal(cell):
		return True if cell == goal else False

def dynvalue(cell):

	x = cell[0]
	y = cell[1]
	empty = -1
	minval = 1e6

	print 'called dynvalue([%d,%d])' %(x,y)	
	d = value[x][y]
	
	if isgoal(cell):
		return 0 
	elif d != empty:
		return d
	else:
		print neighbour([x, y])
		for n in neighbour([x, y]):
			v = dynvalue([n[0],n[1]]) 
			if v <= minval:
				minval = v
		#print minval
		value[x][y] = minval + 1
		return minval


print neighbour([0,0])
print neighbour([0,1])
print neighbour([1,0])
print neighbour([1,1])
print dynvalue([0,1])
"""