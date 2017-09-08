from Queue import Queue
from Queue import LifoQueue


class Node:
    # state - bi-dimensional arrays containing the nursery
    # nLizards - number of lizards currently in this node's state. Numerically equal to the depth
    # parent - parent Node
    # nodeNumber - unique node identifier
    def __init__(self, state, n_lizard, parent, node_number):
        self.state = state
        self.nLizards = n_lizard
        self.parent = parent
        self.nodeNumber = node_number


def readfile(file):
    file_input = open(file, 'r')
    i = 1
    global init_board
    for line in file_input:
        if i == 1:
            global alg
            alg = line.strip()
        elif i == 2:
            global N
            N = int(line.strip())
            init_board = [[0 for x in range(N)] for y in range(N)]
        elif i == 3:
            global nLizardGoal
            nLizardGoal = line.strip()
        else:
            j = 0
            for char in line.strip():
                init_board[i - 4][j] = char
                j += 1
        i += 1


def write_output(result, matrix):
    file_output = open("output.txt", 'w')
    file_output.write(result)
    file_output.write("\n")
    if result == "OK":
        for x in matrix:
            for a in x:
                if a == 3:
                    a = 0
                file_output.write(str(a))
            file_output.write("\n")


def goal_test(node):
    if node.nLizards == nLizardGoal:
        return True
    else:
        return False


def expand(frontier, node):
    return frontier


def search(initial, goal, algorithm):
    if algorithm == "BFS":
        frontier = Queue()
    else:
        frontier = LifoQueue()
    frontier.put(initial)
    while ~frontier.empty():
        print frontier
        node = frontier.get()
        if goal_test(node):
            return node
        else:
            frontier = expand(frontier, node)
    return "FAIL"


readfile("input2.txt")
initialNode = Node(init_board, 0, None, 1)
if alg == "BFS" or alg == "DFS":
    search(initialNode, nLizardGoal, alg)
elif alg == "SA":
    print "SA"
# write_output("OK", [[1, 2], [3, 4]])
