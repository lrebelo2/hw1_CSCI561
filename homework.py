from Queue import Queue
from Queue import LifoQueue
from copy import deepcopy


class Node:
    # state - bi-dimensional arrays containing the nursery
    # nLizards - number of lizards currently in this node's state. Numerically equal to the depth
    # parent - parent Node
    # nodeNumber - unique node identifier
    def __init__(self, stateL, n_lizard, parentL, node_numberL):
        self.state = stateL
        self.nLizards = n_lizard
        self.parent = parentL
        self.nodeNumber = node_numberL


def readfile(filename):
    file_input = open(filename, 'r')
    i = 1
    init_board = [[]]
    for line in file_input:
        if i == 1:
            alg = line.strip()
        elif i == 2:
            N = int(line.strip())
            init_board = [[0 for x in range(N)] for y in range(N)]
        elif i == 3:
            nLizardGoal = line.strip()
        else:
            j = 0
            for char in line.strip():
                init_board[i - 4][j] = char
                j += 1
        i += 1
    return dict(alg=alg, N=N, goal=nLizardGoal, board=init_board)


def write_output(result, matrix):
    file_output = open("output.txt", 'w')
    file_output.write(result)
    file_output.write("\n")
    if result == "OK":
        for x in matrix:
            for a in x:
                if a == '3':
                    a = '0'
                file_output.write(str(a))
            file_output.write("\n")


def goal_test(nodetest, goal):
    print nodetest.nLizards
    if nodetest.nLizards == int(goal):
        print nodetest.state
        return True
    else:
        return False

# FIX THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def update_state(board, row, column, n):
    # up
    x = column
    while x > 0:

        if board[x][column] != '1':
            board[x][column] = '3'
        x -= 1
    # down
    x = column
    while x < n:

        if board[x][column] != '1':
         board[x][column] = '3'
        x += 1
    # left
    x = row
    while x > 0:

        if board[row][x] != '1':
            board[row][x] = '3'
        x -= 1
    # right
    x = row
    while x < n:
        if board[row][x] != '1':
            board[row][x] = '3'
        x += 1
    # 1Q
    x = row - 1
    y = column + 1
    while x > 0 and y < n:
        if board[x][y] != '1':
            board[x][y] = '3'
        x -= 1
        y += 1
    # 2Q
    x = row - 1
    y = column - 1
    while x > 0 and y > 0:
        if board[x][y] != '1':
            board[x][y] = '3'
        x -= 1
        y -= 1
    # 3Q
    x = row + 1
    y = column - 1
    while x < n and y > 0:
        if board[x][y] != '1':
            board[x][y] = '3'
        x += 1
        y -= 1
    # 4Q
    x = row + 1
    y = column + 1
    while x < n and y < n:
        if board[x][y] != '1':
            board[x][y] = '3'
        x += 1
        y += 1

    board[row][column] = '1'
    return board


def expand(frontier, node, n):
    lastNodeNumber = node.nodeNumber
    for i in range(0, n):
        for j in range(0, n):
            if node.state[i][j] == '0':
                lastNodeNumber += 1
                copyx = deepcopy(node.state)
                new_node = Node(update_state(copyx, i, j, n), node.nLizards + 1, node, lastNodeNumber)
                frontier.put_nowait(new_node)
    return frontier


def search(initial, goal, algorithm, n):
    if algorithm == "BFS":
        frontier = Queue()
    else:
        frontier = LifoQueue()
    frontier.put_nowait(initial)
    while not frontier.empty():
        node = frontier.get_nowait()
        if goal_test(node, goal):
            return node
        else:
            frontier = expand(frontier, node, n)
    return "FAIL"


init_param = readfile("input1.txt")
initialNode = Node(init_param['board'], 0, None, 1)
if init_param['alg'] == "BFS" or init_param['alg'] == "DFS":
    result = search(initialNode, init_param['goal'], init_param['alg'], init_param['N'])
    if result == "FAIL":
        write_output(result,init_param['board'])
    else:
        write_output("OK", result.state)
elif init_param['alg'] == "SA":
    print "SA"
