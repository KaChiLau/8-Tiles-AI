# Solves a randomized 8-puzzle using

import util
import pdb

_goal_state = [[1, 2, 3],
               [4, 5, 6],
               [7, 8, 0]]

_test_state = [[0, 2, 3],
               [1, 5, 6],
               [4, 7, 8]]

def index(item, seq):
    """Helper function that returns -1 for non-found index value of a seq"""
    if item in seq:
        return seq.index(item)
    else:
        return -1


class EightPuzzle:

    def __init__(self):

        # heuristic value
        self._heurval = 0
        # search depth of current instance
        self._depth = 0
        # parent node in search path
        self._parent = None
        self.adj_matrix = []
        for i in range(3):
            self.adj_matrix.append(_test_state[i][:])

    def getter(self):
        return self.adj_matrix

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj_matrix == other.adj_matrix

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.adj_matrix[row]))
            res += '\r\n'
        return res

    def _clone(self):
        p = EightPuzzle()
        for i in range(3):
            p.adj_matrix[i] = self.adj_matrix[i][:]
        return p

    def _generate_moves(self):
        utilit = util.utility()
        free = utilit._get_legal_moves(self)
        zero = utilit.find(self, 0)

        def swap_and_clone(a, b):
            p = self._clone()
            p = utilit.swap(p, a, b)
            p._depth = self._depth + 1
            p._parent = self
            return p

        return map(lambda pair: swap_and_clone(zero, pair), free)

    def _generate_solution_path(self, path):
        if self._parent == None:
            return path
        else:
            path.append(self)
            return self._parent._generate_solution_path(path)

    def solve(self, heur, algorithm):
	
		def is_solved(puzzle):
			return puzzle.adj_matrix == _goal_state

		if algorithm == 'DFS':
			fringe = util.Stack()
		if algorithm == 'BFS':
			fringe = util.Queue()
		if algorithm == 'UCS':
			fringe = util.PriorityQueueWithFunction(lambda p: p._depth)
		if algorithm == 'A*':
			fringe = util.PriorityQueueWithFunction(lambda p: p._depth + p._heurval)
        
		path = list()
		visited = list()
		move_count = 0
		fringe.push(self)
		
		while not fringe.isEmpty():
			node = fringe.pop()
			move_count += 1
			
			if(node not in visited):
				visited.append(node)
  
				if (is_solved(node)):
					return node._generate_solution_path([]), move_count
                    
				successor = node._generate_moves()
				for move in successor:
					move.parent = node
					fringe.push(move)

	return [], 0

def heur(puzzle, item_total_calc, total_calc):
    """
    Heuristic template that provides the current and target position for each number and the 
    total function.
    
    Parameters:
    puzzle - the puzzle
    item_total_calc - takes 4 parameters: current row, target row, current col, target col. 
    Returns int.
    total_calc - takes 1 parameter, the sum of item_total_calc over all entries, and returns int. 
    total_calc is the value of the heuristic function.
    """
    t = 0
    utilit = util.utility()
    for row in range(3):
        for col in range(3):
            val = utilit.peek(puzzle, row,
                              col) - 1  # value is -1 if the peeked index is 0. triggers if target_row < 0 below.
            target_col = val % 3
            target_row = val / 3

            # account for 0 as blank
            if target_row < 0:
                target_row = 2
            t += item_total_calc(row, target_row, col, target_col)


    return total_calc(t)


# some heuristic functions, the best being the standard manhattan distance in this case, as it comes
# closest to maximizing the estimated distance while still being admissible.

def h_manhattan(puzzle):
    return heur(puzzle,
                lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                lambda t: t)


def h_default(puzzle):
    return 0


def main():
	utility = util.utility()
	p = EightPuzzle()
	shuffle = utility.shuffle(p, 20)
	print "Starting puzzle:"
	print shuffle
	
	selection = raw_input("Which algorithm would you like to use to solve this matrix? (DFS, BFS, UCS, A*, or All for all four) \n")
	if selection == "DFS":
		path, count = shuffle.solve(h_default, 'DFS')
		path.reverse()
		print "Path to goal state:"
		for i in path:
			print i
		print "Solved with DFS search in", count, "node expansions"
	elif selection == "BFS":
		path, count = shuffle.solve(h_default, 'BFS')
		path.reverse()
		print "Path to goal state:"
		for i in path:
			print i
		print "Solved with BFS search in", count, "node expansions"
	elif selection == "UCS":
		path, count = shuffle.solve(h_default, 'UCS')
		path.reverse()
		print "Path to goal state:"
		for i in path:
			print i
		print "Solved with UCS search in", count, "node expansions"
	elif selection == "A*":
		path, count = shuffle.solve(h_manhattan, 'A*')
		path.reverse()
		print "Path to goal state:"
		for i in path:
			print i
		print "Solved with A* search utilizing Manhattan distance hueuristic in", count, "node expansions"
	elif selection == "All" or "all":
		path, count = shuffle.solve(h_manhattan, 'A*')
		path.reverse()
		print "Path to goal state:"
		for i in path:
			print i
		print "Solved with A* search utilizing Manhattan distance hueuristic in", count, "node expansions"
		path, count = shuffle.solve(h_default, 'UCS')
		print "Solved with UCS search in", count, "node expansions"
		path, count = shuffle.solve(h_default, 'BFS')
		print "Solved with BFS search in", count, "node expansions"
		path, count = shuffle.solve(h_default, 'DFS')
		print "Solved with DFS search in", count, "node expansions"

if __name__ == "__main__":
    main()
