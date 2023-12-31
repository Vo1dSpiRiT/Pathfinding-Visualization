import numpy as np

def Dijkstra(grid):
    visitedNodesInOrder = np.empty(0)
    startNode = grid.startNode
    endNode = grid.endNode
    
    startNode.distance = 0
    unvisitedNodes = grid.nodes.flatten()
    while len(unvisitedNodes):
        closestNode, index = getClosestNode(unvisitedNodes)
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
        
def getShortestPath(endNode):
    currentNode = endNode
    path = []
    while currentNode.previousNode:
        path.append(currentNode)
        currentNode = currentNode.previousNode
    return path

def getClosestNode(unvisitedNodes):
    closestNode = unvisitedNodes[0]
    index = 0
    for i, node in enumerate(unvisitedNodes):
        if node.distance < closestNode.distance:
            closestNode = node
            index = i
    return closestNode, index
        
def getUnvisitedNeighbors(grid, currentNode):
    neighbors = []
    x, y = int(currentNode.position.x), int(currentNode.position.y)
    if x > 0:
        neighbors.append(grid[x-1, y])
    if x < grid.rows-1:
        neighbors.append(grid[x+1, y])
    if y > 0:
        neighbors.append(grid[x, y-1])
    if y < grid.cols-1:
        neighbors.append(grid[x, y+1])
    return [neighbor for neighbor in neighbors if not (neighbor.isVisited or neighbor.previousNode)]
