import math
import random
import EightTile

"""
 Data structures useful for implementing SearchAgents
"""

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

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def __len__(self):
        return len(self.list) 
    
    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

class PriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer

    def push(self, item):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(item))


def manhattanDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )


class utility:

    def shuffle(self, Puzzle, step_count):
        # print Puzzle
        #for i in range(step_count):
            #row, col = self.find(Puzzle, 0)
            # print("ROW COLONE",row,col)
            #free = self._get_legal_moves(Puzzle)
            # print ("FREEEE",free)
            #target = random.choice(free)
            # print("TARGT",target)
            #self.swap(Puzzle, (row, col), target)
            #row, col = target
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
            free.append((row - 1, col)) #up [up]
            #print("up")
        if col > 0:
            free.append((row, col - 1)) #left [up, left]
            #print("left")
        if row < 2:
            #free.append((row + 1, col)) #down [up, left, down]
            #print("down")
        if col < 2:
            free.append((row, col + 1)) #right [up, left, down, right]
            #print("right")

        print ("")
        
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
