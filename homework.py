import math
import random
from Queue import LifoQueue
from Queue import Queue
from copy import deepcopy


class Node:
    # state - bi-dimensional arrays containing the nursery
    # nLizards - number of lizards currently in this node's state. Numerically equal to the depth
    # parent - parent Node
    # nodeNumber - unique node identifier
    def __init__(self, stateL, n_lizard, parentL, node_numberL, next_free_row):
        self.state = stateL
        self.nLizards = n_lizard
        self.parent = parentL
        self.nodeNumber = node_numberL
        self.row = next_free_row


class Queen:
    def __init__(self, row, column, collisions):
        self.row = row
        self.column = column
        self.collisions = collisions

    def printQ(self):
        print self.row, self.column, self.collisions


class NodeSA:
    def __init__(self, stateL, n_lizard, n):
        self.goal = n_lizard
        self.N = n
        self.state = stateL
        list = []
        queens = []
        enough_lizards = 0
        if n_lizard == 0:
            self.state = stateL
        else:
            for i in range(0, n):
                list.append(i)
            for i in range(0, n):
                next = random.choice(list)
                list.remove(next)
                if self.state[i][next] == 0:
                    self.state[i][next] = 1
                    queens.append(Queen(i, next, 0))
                    enough_lizards += 1
                if enough_lizards == n_lizard:
                    break
            while enough_lizards < n_lizard:
                i = random.randint(0, n - 1)
                j = random.randint(0, n - 1)
                if self.state[i][j] == 0:
                    self.state[i][j] = 1
                    queens.append(Queen(i, j, 0))
                    enough_lizards += 1
        self.queens = queens
        self.collisions()

    def collisions(self):
        collisionsTotal = 0
        n = self.N
        for i in self.queens:
            collisions = 0
            row = i.row
            column = i.column
            x = row - 1
            # up
            while x >= 0:
                if self.state[x][column] == 1:
                    collisions += 1
                if self.state[x][column] == 2:
                    x = 0
                x -= 1

            # down
            x = row + 1
            while x < n:
                if self.state[x][column] == 1:
                    collisions += 1
                if self.state[x][column] == 2:
                    x = n
                x += 1
            # left
            x = column - 1
            while x >= 0:
                if self.state[row][x] == 1:
                    collisions += 1
                if self.state[row][x] == 2:
                    x = 0
                x -= 1
            # right
            x = column + 1
            while x < n:
                if self.state[row][x] == 1:
                    collisions += 1
                if self.state[row][x] == 2:
                    x = n
                x += 1

            # 1Q
            x = row - 1
            y = column + 1
            while x >= 0 and y < n:
                if self.state[x][y] == 1:
                    collisions += 1
                if self.state[x][y] == 2:
                    x = 0
                x -= 1
                y += 1
            # 2Q
            x = row - 1
            y = column - 1
            while x >= 0 and y >= 0:
                if self.state[x][y] == 1:
                    collisions += 1
                if self.state[x][y] == 2:
                    x = 0
                x -= 1
                y -= 1
            # 3Q
            x = row + 1
            y = column - 1
            while x < n and y >= 0:
                if self.state[x][y] == 1:
                    collisions += 1
                if self.state[x][y] == 2:
                    x = n
                x += 1
                y -= 1
            # 4Q
            x = row + 1
            y = column + 1
            while x < n and y < n:
                if self.state[x][y] == 1:
                    collisions += 1
                if self.state[x][y] == 2:
                    x = n
                x += 1
                y += 1
            i.collisions = collisions
            collisionsTotal += collisions
        return collisionsTotal / 2


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
                j += 1
                if char == '2':
                    flag_tree = True
        i += 1
    if not flag_tree and (n_lizard_goal > N):
        flag_doomed = True
    return dict(alg=alg, N=N, goal=n_lizard_goal, board=init_board, tree=flag_tree, doomed=flag_doomed)


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


def printM(m):
    for x in m:
        print x


def goal_test(node_test, goal):
    if node_test.nLizards == int(goal):
        return True
    else:
        return False


def update_state(state, row, column, n):
    tree = False
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
            tree = True
        x -= 1
    # right
    x = column + 1
    while x < n:
        if board[row][x] == 0:
            board[row][x] = 3
        if board[row][x] == 2:
            tree = True
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

    return dict(board=board, tree=tree)


def selectSucessor(nodeL):
    node = deepcopy(nodeL)
    x = 0
    while x == 0:
        queen = random.choice(node.queens)
        x = queen.collisions
    flag = False
    while not flag:
        i = random.randint(0, node.N - 1)
        j = random.randint(0, node.N - 1)
        if node.state[i][j] == 0:
            node.state[queen.row][queen.column] = 0
            node.state[i][j] = 1
            queen.row = i
            queen.column = j
            flag = True
    return node


def selectSucessor2(nodeL):
    node = deepcopy(nodeL)
    x = 0
    while x == 0:
        queen = random.choice(node.queens)
        x = queen.collisions
    flag = False
    while not flag:
        j = random.randint(0, node.N - 1)
        if node.state[j][queen.column] == 0:
            node.state[queen.row][queen.column] = 0
            node.state[j][queen.column] = 1
            queen.row = j
            flag = True
    return node


def searchSA(node, tree):
    minimal_Temperature = 1e-7
    alpha = 0.9997
    cost = node.collisions()
    current = node
    T = cost
    while T > minimal_Temperature and cost != 0:
        if tree:
            next = selectSucessor(current)
        else:
            next = selectSucessor2(current)
        next_cost = next.collisions()
        delta = cost - next_cost
        #print cost
        if delta >= 0:
            current = next
            cost = next_cost
        else:
            if math.exp(delta / T) > random.random():
                current = next
                cost = next_cost
        T *= alpha
    if cost == 0:
        return current
    return "FAIL"


def expand(frontier_arg, node, n):
    flag = False
    node_number = node.nodeNumber
    for i in range(0, n):
        if node.row < n:
            if node.state[node.row][i] == 0:
                flag = True
                node_number += 1
                new_state = update_state(node.state, node.row, i, n)
                if not new_state['tree']:
                    new_node = Node(new_state['board'], node.nLizards + 1, node, node_number, node.row + 1)
                else:
                    new_node = Node(new_state['board'], node.nLizards + 1, node, node_number, node.row)
                frontier_arg.put_nowait(new_node)
    while not flag and node.row + 1 < n:
        node.row += 1
        for i in range(0, n):
            if node.state[node.row][i] == 0:
                node_number += 1
                new_state = update_state(node.state, node.row, i, n)
                if not new_state['tree']:
                    new_node = Node(new_state['board'], node.nLizards + 1, node, node_number, node.row + 1)
                else:
                    new_node = Node(new_state['board'], node.nLizards + 1, node, node_number, node.row)
                frontier_arg.put_nowait(new_node)


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
            expand(frontier, node, n)
    return "FAIL"


init_param = readfile("input.txt")
if not init_param['doomed']:
    if init_param['alg'] == "BFS" or init_param['alg'] == "DFS":
        initialNode = Node(init_param['board'], 0, None, 1, 0)
        result = search(initialNode, init_param['goal'], init_param['alg'], init_param['N'])
        if result == "FAIL":
            write_output(result, init_param['board'])
        else:
            write_output("OK", result.state)
    elif init_param['alg'] == "SA":
        initialNode = NodeSA(init_param['board'], init_param['goal'], init_param['N'])
        result = searchSA(initialNode, init_param['tree'])
        if result == "FAIL":
            write_output(result, init_param['board'])
        else:
            write_output("OK", result.state)

    else:
        write_output("FAIL", init_param['board'])
else:
    write_output("FAIL", init_param['board'])
