from Queue import LifoQueue
from Queue import Queue
from copy import deepcopy


def initiate_list(n):
    row_list = list()
    for i in range(0, n):
        row_list.append(True)
    return row_list


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
        # if parentL is None:
        #     self.rows = initiate_list(len(stateL[0]))
        # else:
        #     self.rows = parentL.rows


def readfile(filename):
    file_input = open(filename, 'r')
    i = 1
    alg = ''
    N, n_lizard_goal = 0, 0
    flag_tree, flag_doomed = False, False
    init_board = [[]]
    for line in file_input:
        if i == 1:
            alg = line.strip()
        elif i == 2:
            N = int(line.strip())
            init_board = [[0 for x in range(N)] for y in range(N)]
        elif i == 3:
            n_lizard_goal = int(line.strip())
        else:
            j = 0
            for char in line.strip():
                init_board[i - 4][j] = int(char)
                if char == '2':
                    flag_tree = True

                j += 1
        i += 1
    if (not flag_tree) and (n_lizard_goal > N):
        flag_doomed = True
    print N, n_lizard_goal
    return dict(alg=alg, N=N, goal=n_lizard_goal, board=init_board, doomed=flag_doomed)


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


def goal_test(node_test, goal):
    if node_test.nLizards == int(goal):
        return True
    else:
        return False


def update_state(state, row, column, n):
    # up
    x = row - 1
    board = deepcopy(state)
    while x >= 0:
        if board[x][column] == 0:
            board[x][column] = 3
        if board[x][column] == 2:
            x = 0
        x -= 1

    # down
    x = row + 1
    while x < n:
        if board[x][column] == 0:
            board[x][column] = 3
        if board[x][column] == 2:
            x = n
        x += 1
    # left
    x = column - 1
    while x >= 0:

        if board[row][x] == 0:
            board[row][x] = 3
        if board[row][x] == 2:
            x = 0
        x -= 1
    # right
    x = column + 1
    while x < n:
        if board[row][x] == 0:
            board[row][x] = 3
        if board[row][x] == 2:
            x = n
        x += 1

    # 1Q
    x = row - 1
    y = column + 1
    while x >= 0 and y < n:
        if board[x][y] == 0:
            board[x][y] = 3
        if board[x][y] == 2:
            x = 0
        x -= 1
        y += 1
    # 2Q
    x = row - 1
    y = column - 1
    while x >= 0 and y >= 0:
        if board[x][y] == 0:
            board[x][y] = 3
        if board[x][y] == 2:
            x = 0
        x -= 1
        y -= 1
    # 3Q
    x = row + 1
    y = column - 1
    while x < n and y >= 0:
        if board[x][y] == 0:
            board[x][y] = 3
        if board[x][y] == 2:
            y = 0
        x += 1
        y -= 1
    # 4Q
    x = row + 1
    y = column + 1
    while x < n and y < n:
        if board[x][y] == 0:
            board[x][y] = 3
        if board[x][y] == 2:
            x = n
        x += 1
        y += 1

    board[row][column] = 1
    return board


def expand(frontier_arg, node, n):
    node_number = node.nodeNumber
    # which row will I look at now?

    for i in range(0, n):
        if node.state[node.nLizards][i] == 0:
            node_number += 1
            new_node = Node(update_state(node.state, node.nLizards, i, n), node.nLizards + 1, node, node_number)
            frontier_arg.put_nowait(new_node)


def printM(M):
    for i in M:
        print i


def search(initial, goal, algorithm, n):
    if algorithm == "BFS":
        frontier = Queue()
    else:
        frontier = LifoQueue()
    visited_rows = initiate_list(n)
    frontier.put_nowait(initial)
    while not frontier.empty():
        print frontier.qsize()
        node = frontier.get_nowait()
        if goal_test(node, goal):
            return node
        else:
            expand(frontier, node, n)
    return "FAIL"


init_param = readfile("input4.txt")
initialNode = Node(init_param['board'], 0, None, 1)
if not init_param['doomed']:
    if init_param['alg'] == "BFS" or init_param['alg'] == "DFS":
        result = search(initialNode, init_param['goal'], init_param['alg'], init_param['N'])
        if result == "FAIL":
            write_output(result, init_param['board'])
        else:
            write_output("OK", result.state)
    elif init_param['alg'] == "SA":
        print "SA"
    else:
        write_output("FAIL", init_param['board'])
else:
    write_output("FAIL", init_param['board'])
