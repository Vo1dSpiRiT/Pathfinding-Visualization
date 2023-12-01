import numpy as np
from Scripts.Algorithms.Dijkstra import getShortestPath, getUnvisitedNeighbors

def Astar(grid):
    visitedNodesInOrder = np.empty(0)
    startNode = grid.startNode
    endNode = grid.endNode
    
    startNode.distance = 0
    unvisitedNodes = grid.nodes.flatten()
    while len(unvisitedNodes):
        closestNode, index = getClosestNode(unvisitedNodes, endNode)
        unvisitedNodes = np.delete(unvisitedNodes, index)
        if closestNode.distance == float('inf'):
            return visitedNodesInOrder, []
        if closestNode.isWall:
            continue
        visitedNodesInOrder = np.append(visitedNodesInOrder, closestNode)
        if closestNode.isEnd:
            return visitedNodesInOrder, getShortestPath(endNode)
        
        unvisitedNeighbors = getUnvisitedNeighbors(grid, closestNode)
        for neighbor in unvisitedNeighbors:
            neighbor.distance = closestNode.distance + (neighbor.weight+1)
            neighbor.previousNode = closestNode
        closestNode.isVisited = True
        
def getClosestNode(unvisitedNodes, endNode):
    index = 0
    closestNode = unvisitedNodes[0]
    f = potential(closestNode, endNode)
    for i, node in enumerate(unvisitedNodes):
        fnode = potential(node, endNode)
        if (node.distance+fnode <= closestNode.distance+f):
            if (node.distance+fnode < closestNode.distance+f) or fnode < f:
                closestNode = node
                index = i
                f = fnode
    return closestNode, index

def potential(currentNode, endNode):
    return abs(currentNode.position.x - endNode.position.x) + abs(currentNode.position.y - endNode.position.y)