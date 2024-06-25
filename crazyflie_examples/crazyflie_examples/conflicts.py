import matplotlib.pyplot as plt
import networkx as nx
from copy import copy

# CBS outline:
# run aStar once with [] constraints
# pass through calculated constraints + rereun aStar
# run  findConflicts functions again
# pass thorugh any new conflicts found
# so on and so forth...

# def findPath(start, goal):
G = nx.grid_2d_graph(4, 4)


def dist(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


# collects gCosts in a dictionary within A* function below


# calculates hCost (distance from current node and end node)
def hCost(currentNode, end):
    return dist(currentNode, end)


# calculates fCost (gCost + hCost)
def fCost(gCost, currentNode, end):
    fCost = gCost + hCost(currentNode, end)
    return fCost


# I got rid of the gCost = len(path) stuff for now!


def get_adjacent_nodes(currentNode):
    # possible movements: up, down, left, right
    movements = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    children = []
    for move in movements:
        adjacent_node = (currentNode[0] + move[0], currentNode[1] + move[1])

        if 0 <= adjacent_node[0] < 10 and 0 <= adjacent_node[1] < 10:
            children.append(adjacent_node)
    return children


# -----------------------------------------------------------------------------
# NEW CBS:

# make parent node
# node is defined by path A and its constraints + path B and its constraints
# each node is a list


def CBS(startPoints, endPoints):
    parentNode = []
    for startpoint in startPoints:
        parentNode.append(
            aStar(startpoint, endPoints[startPoints.index(startpoint)], [])
        )
        parentNode.append([])

    # all constraints are [] right now since no constraints at parent node
    def gen2Nodes(node):

        constraints = []
        for i in range(len(node)):
            if i % 2 != 0:
                constraints.append(node[i])

        paths = []
        for i in range(len(node)):
            if i % 2 == 0:
                paths.append(node[i])

        #  paths now contains all paths at this node
        # constraints now contains all paths at this node

        constraint1 = findFirstConflict(paths)

        if constraint1 is None:
            #  return paths
            return paths
        # if no conflicts, final paths found
        else:

            if constraint1[0] == "vertex":
                node1 = []
                node2 = []
                for index, path in enumerate(paths):
                    if index != constraint1[3] and index != constraint1[4]:
                        print(index)
                        node1.append(
                            aStar(
                                startPoints[index], endPoints[index], constraints[index]
                            )
                        )
                        node1.append(constraints[index])
                        node2.append(
                            aStar(
                                startPoints[index], endPoints[index], constraints[index]
                            )
                        )
                        node2.append(constraints[index])
                    elif index == constraint1[4]:
                        continue
                    else:
                        # node1 applies conflict1 to the first conflicting agent's path
                        conflicting_constraint1 = copy(constraints[constraint1[3]])
                        conflicting_constraint1.append(constraint1)

                        node1.append(
                            aStar(
                                startPoints[constraint1[3]],
                                endPoints[constraint1[3]],
                                conflicting_constraint1,
                            )
                        )
                        node1.append(conflicting_constraint1)
                        node1.append(
                            aStar(
                                startPoints[constraint1[4]],
                                endPoints[constraint1[4]],
                                constraints[constraint1[4]],
                            )
                        )
                        node1.append(constraints[constraint1[4]])

                        # node2 applies conflict1 to the second conflicting agent's path
                        conflicting_constraint2 = copy(constraints[constraint1[4]])
                        conflicting_constraint2.append(constraint1)

                        node2.append(
                            aStar(
                                startPoints[constraint1[3]],
                                endPoints[constraint1[3]],
                                constraints[constraint1[3]],
                            )
                        )
                        node2.append(constraints[constraint1[3]])
                        node2.append(
                            aStar(
                                startPoints[constraint1[4]],
                                endPoints[constraint1[4]],
                                conflicting_constraint2,
                            )
                        )
                        node2.append(conflicting_constraint2)
            # runs gen2nodes for each child node so it will keep adding branches to the tree until no constraints are found
            output = gen2Nodes(node1)
            if output is not None:
                return output
            return gen2Nodes(node2)

    return gen2Nodes(parentNode)


# ---------------------------------------------------------------------------------------


def aStar(start, end, constraints):
    closedList = [(start)]
    openList = []
    children = []
    cameFrom = {}
    gCosts = {}
    gCosts[start] = 0
    currentNode = start
    while currentNode != end:
        # print("loop entered")
        fCostsOpenList = []
        children = get_adjacent_nodes(currentNode)
        children = [child for child in children if child not in closedList]

        for constraint in constraints:
            if constraint[0] == "vertex":
                node = constraint[1]
                time = constraint[2]
                currTime = gCosts[currentNode]
                if (time - 1) == currTime:
                    children = [child for child in children if child != node]
            else:
                if constraint[0] == "edge":
                    node2 = constraint[2]
                    time = constraint[3]
                    currTime = gCosts[currentNode]
                    if (time + 0.5) == (currTime + 1):
                        children = [child for child in children if child != node2]
        for child in children:
            gCosts[child] = gCosts[currentNode] + 1
            openList.append((child, fCost(gCosts[child], child, end)))
            cameFrom[child] = currentNode

        # finds child node with lowest fCost
        for node in openList:
            fCostsOpenList.append(node[1])
        minIndex = fCostsOpenList.index(min(fCostsOpenList))
        for node in openList:
            if node[1] == fCostsOpenList[minIndex]:
                openList.remove(node)
                # this now appends the child node with lowest fCost to closed List
                closedList.append(node[0])
                currentNode = node[0]
                # print(node[1])
                # print(currentNode)
                break

    # print("closed", closedList)
    # print("open", openList)

    return getPath(cameFrom, start, end)


# create path from closedList
def getPath(cameFrom, start, end):
    path = []
    path.append(end)
    currentNode = end
    while currentNode != start:
        currentNode = cameFrom[currentNode]
        path.insert(0, currentNode)

    #   print("path", path)
    return path


# ---------------------------------------------------------------------------
# new multi agent version
def findFirstConflict(paths):
    first_vertex_conflict = findVertexConflicts(paths)
    first_edge_conflict = findEdgeConflicts(paths)
    first_conflict = None

    print(first_vertex_conflict)
    if first_vertex_conflict == None:
        first_conflict = first_edge_conflict
    elif first_edge_conflict == None:
        first_conflict = first_vertex_conflict
    elif first_vertex_conflict[2] < first_edge_conflict[3]:
        first_conflict = first_vertex_conflict
    else:
        if first_edge_conflict[3] < first_vertex_conflict[2]:
            first_conflict = first_edge_conflict

    print("first conflict:", first_conflict)
    return first_conflict


# -----------------------------------------------------------------
# updated findVertexConflicts for any given number of paths
def findVertexConflicts(paths):
    longestPath = paths[0]
    for i in range(len(paths)):
        if len(paths[i]) > len(longestPath):
            longestPath = paths[i]

    for path in paths:
        if path != longestPath:
            x = len(longestPath) - len(path)

            for _ in range(x):
                path.append(path[len(path) - 1])

    print("paths:", paths)

    for index, nodes in enumerate(zip(*paths)):
        seen_nodes = {}
        for path_index, node in enumerate(nodes):
            if node in seen_nodes:
                print(
                    "Conflict:",
                    node,
                    "Index:",
                    index,
                    "Involved paths:",
                    seen_nodes[node],
                    "and",
                    path_index,
                )
                return ["vertex", node, index, seen_nodes[node], path_index]
            seen_nodes[node] = path_index


# -------------------------------------------------------------------
# update version for multiple agents
def findEdgeConflicts(paths):
    longestPath = paths[0]
    for i in range(len(paths)):
        if len(paths[i]) > len(longestPath):
            longestPath = paths[i]

    for path in paths:
        if path != longestPath:
            x = len(longestPath) - len(path)

            for _ in range(x):
                path.append(path[len(path) - 1])

    print("paths:", paths)

    for index1, path1 in enumerate(paths):
        for index2, path2 in enumerate(paths):
            if index2 <= index1:
                continue
            for t in range(len(path1) - 1):

                if path1[t] == path2[t + 1] and path1[t + 1] == path2[t]:
                    print(["edge", path1[t], path2[t], (i - 1), index1, index2])
                    return ["edge", path1[t], path2[t], (i - 1), index1, index2]


# -----------------------------------------------------------------------------------------------------------------


# aStar((2,2), (4,4), [])
# aStar((4,0), (4,4), [])

# CBS((2,2), (4,4), (2,3), (3,4))

# aStar((2,2), (4,4), [['vertex', (4,3), 3], ['edge', (3,2), (4,2), 1.5]])


# aStar((2,2), (4,4), [['edge', (3,2), (4,2), 1.5], ['edge', (2,4), (3,4), 2.5]])
# no constraints: path [(2,2), (3,2), (4,2), (4,3), (4,4)]
# first constraint: path [(2, 2), (2, 3), (2, 4), (3, 4), (4, 4)]
# both constraints: path [(2, 2), (3, 2), (3, 3), (4, 3), (4, 4)]

# aStar((2,2), (4,4), ['edge', ])
# aStar((2,2), (4,4), [])
# aStar((2,2), (4,4), (findVertexConflicts(aStar((2,2), (4,4), []), aStar((4,0), (4,3), []))))

# findFirstConflict([aStar((2,2), (4,4), []), aStar((4,0), (4,4), []), aStar((1,0), (0,0), [])])
# findFirstConflict(aStar((0,0), (2,0), []), aStar((1,0), (0,0), [])) WORKS!

# findEdgeConflicts(aStar((0,0), (2,0), []), aStar((1,0), (0,0), []))

# this works:
# findVertexConflicts([aStar((2,2), (4,4), []), aStar((4,0), (4,3), []), aStar((3,0), (4,2), [])])

# findEdgeConflicts([aStar((2,2), (4,4), []), aStar((3,2), (2,2), [])])

CBS([(2, 2), (4, 0), (3, 0)], [(4, 4), (4, 3), (3, 5)])
