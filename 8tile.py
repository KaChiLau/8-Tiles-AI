# Solves a randomized 8-puzzle using

import random
import math

_goal_state = [[1,2,3],
               [4,5,6],
               [7,8,0]]

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
            self.adj_matrix.append(_goal_state[i][:])

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

    def _get_legal_moves(self):
        """Returns list of tuples with which the free space may
        be swapped"""
        # get row and column of the empty piece
        row, col = self.find(0)
        free = []
        
        # find which pieces can move there
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 2:
            free.append((row + 1, col))
        if col < 2:
            free.append((row, col + 1))

        return free

    def _generate_moves(self):
        free = self._get_legal_moves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self._clone()
            p.swap(a,b)
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
        """Performs A* search for goal state.
        h(puzzle) - heuristic function, returns an integer
        """
        def is_solved(puzzle):
            return puzzle.adj_matrix == _goal_state

        openlist = [self] # represents the calling matrix's initial configuation
        closedlist = [] # represents the moves that the calling matrix will make to solve itself
        move_count = 0
        while len(openlist) > 0:
            x = openlist.pop(0)
            move_count += 1
            if (is_solved(x)):
                if len(closedlist) > 0:
                    return x._generate_solution_path([]), move_count
                else:
                    return [x]

            successor = x._generate_moves()
            index_open = index_closed = -1  
            for move in successor:
                # have we already seen this node?
                index_open = index(move, openlist) 
                index_closed = index(move, closedlist)
                heurval = heur(move)
                fval = heurval + move._depth

                if index_closed == -1 and index_open == -1:
                    move._heurval = heurval
                    openlist.append(move)
                elif index_open > -1:
                    copy = openlist[index_open]
                    if fval < copy._heurval + copy._depth:
                        # copy move's values over existing
                        copy._heurval = heurval
                        copy._parent = move._parent
                        copy._depth = move._depth
                elif index_closed > -1:
                    copy = closedlist[index_closed]
                    if fval < copy._heurval + copy._depth:
                        move._heurval = heurval
                        closedlist.remove(copy)
                        openlist.append(move)

            closedlist.append(x)
			if algorithm is UCS:
				openlist = sorted(openlist, key=lambda p: p.depth)
			else:
				openlist = sorted(openlist, key=lambda p: p._heurval + p._depth)

        # if finished state not found, return failure
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
    This is the value of the heuristic function
    """
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.peek(row, col) - 1 # value is -1 if the peeked index is 0. triggers if target_row < 0 below.
            target_col = val % 3
            target_row = val / 3

            # account for 0 as blank
            if target_row < 0: 
                target_row = 2

            t += item_total_calc(row, target_row, col, target_col)

    return total_calc(t)

#some heuristic functions, the best being the standard manhattan distance in this case, as it comes
#closest to maximizing the estimated distance while still being admissible.

def h_manhattan(puzzle):
    return heur(puzzle,
                lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                lambda t : t)

def h_default(puzzle):
    return 0

def main():
    p = EightPuzzle()
    p.shuffle(20)
    print p

    path, count = p.solve(h_manhattan, A*)
    path.reverse()
    for i in path: 
        print i

    print "Solved with A* search utilizing Manhattan distance hueuristic exploring ", count, "states"
	path, count = p.solve(h_default, UCS)
	print "Solved with UCS in", count, "moves"
	path, count = p.solve(h_default, DFS)
	print "Solved with DFS in", count, "moves"
    path, count = p.solve(h_default, BFS)
    print "Solved with BFS in", count, "moves"

if __name__ == "__main__":
main()