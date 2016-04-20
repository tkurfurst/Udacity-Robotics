grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]

goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

def search():
    # ----------------------------------------
    # insert code here and make sure it returns the appropriate result
    # ----------------------------------------

    #print 'search(): started'

    path = []

    visited = set()

    frontier = [[0] + init]

    #print 'path:', path,'visited:', visited, 'frontier:', frontier

    def is_goal(path):
        return True if path[1:] == goal else False

    def cell_add(a,b):
        return [a[0]+b[0],a[1]+b[1]] 

    def valid_cell(cell):
        if cell[0] >= 0 and cell[0] <= len(grid)-1 and cell[1] >= 0 and cell[1] <= len(grid[0])-1:
            return True
        else: 
            return False

    def successor(node, grid, visited):
        successors = []
        cost, cell = node[0], node[1:]
        for move in delta:
            nextcell = cell_add(cell, move)
            if valid_cell(nextcell) and tuple(nextcell) not in visited and grid[nextcell[0]][nextcell[1]] == 0:
                successors.append([cost+1] + nextcell)         
        return successors

    i = 0
        
    while not is_goal(path):
        #print 'loop'
        if not frontier:
            #print 'search(): ended in %d paths explored - NO SOLUTION' %(i)
            return 'fail'
        path = frontier.pop()
        #print 'to explore:', path
        #print 'frontier:', frontier
        new_frontier = successor(path, grid,visited)
        #print 'successors:', new_frontier
        visited.add(tuple(path[1:]))
        #print 'add to visited:', tuple(path[1:])
        #print 'visited:', visited
        frontier += new_frontier
        frontier = sorted(frontier, key=lambda x: x[0], reverse=True)
        #print 'new frontier:', frontier
        i +=1
        #print '\n'
    #print 'search(): ended in %d paths explored, %d steps to goal' %(i, path[0])
    return path # you should RETURN your result

print search()