import math
import random
import EightTile

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def __len__(self):
        return len(self.list)

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class utility:

    def shuffle(self, Puzzle, step_count):
        # print Puzzle
        for i in range(step_count):
            row, col = self.find(Puzzle, 0)
            # print("ROW COLONE",row,col)
            free = self._get_legal_moves(Puzzle)
            # print ("FREEEE",free)
            target = random.choice(free)
            # print("TARGT",target)
            self.swap(Puzzle, (row, col), target)
            row, col = target
        return Puzzle

    def something(self, a, b):
        return a + b

    def _get_legal_moves(self, Puzzle):
        """Returns list of tuples with which the free space may
        be swapped"""
        # get row and column of the empty piece
        row, col = self.find(Puzzle, 0)
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

    def find(self, Puzzle, value):
        """returns the row, col coordinates of the specified value
           in the graph"""
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if Puzzle.adj_matrix[row][col] == value:
                    # print("ROW COL", row, col)
                    return row, col

    def peek(self,Puzzle, row, col):

        """returns the value at the specified row and column"""
        # print("Peek Value:", Puzzle.adj_matrix[row][col])
        return Puzzle.adj_matrix[row][col]

    def poke(self, Puzzle, row, col, value):

        """sets the value at the specified row and column"""
        Puzzle.adj_matrix[row][col] = value
        # print("Poke Value:", Puzzle.adj_matrix[row][col])

    def swap(self, Puzzle, pos_a, pos_b):

        """swaps values at the specified coordinates"""

        temp = self.peek(Puzzle, *pos_a)
        # print("TEMP", temp)
        # print("POS A", pos_a[0])
        self.poke(Puzzle, pos_a[0], pos_a[1], self.peek(Puzzle, *pos_b))
        # print("SELF PEEEK",self.peek(Puzzle, *pos_b))
        self.poke(Puzzle, pos_b[0], pos_b[1], temp)
        return Puzzle
