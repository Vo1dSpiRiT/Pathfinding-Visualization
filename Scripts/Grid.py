from Scripts.Node import Node
import numpy as np

class Grid():
    def __init__(self, rows, cols, nodeDimensions, startNodePosition, endNodePosition):
        self.rows = rows
        self.cols = cols
        self.startNodePosition = startNodePosition
        self.endNodePosition = endNodePosition
        self.nodes = self.getNodes(nodeDimensions)
        
    def getNodes(self, nodeDimensions):
        nodes = np.empty((self.rows, self.cols), dtype=object)
        for i in range(self.rows):
            for j in range(self.cols):
                nodes[i, j] = Node(i, j, nodeDimensions)
        nodes[self.startNodePosition[0], self.startNodePosition[1]].isStart = True
        nodes[self.endNodePosition[0], self.endNodePosition[1]].isEnd = True
        return nodes
    
    def __getitem__(self, index):
        return self.nodes[index]
    
    def __setitem__(self, index, value):
        self.nodes[index] = value
        
    def reset(self):
        self.nodes = self.getNodes()
        
    def update(self, startNodePosition, endNodePosition):
        self.nodes[self.startNodePosition[0], self.startNodePosition[1]].isStart = False
        self.nodes[self.endNodePosition[0], self.endNodePosition[1]].isEnd = False
        self.startNodePosition = startNodePosition
        self.endNodePosition = endNodePosition
        self.nodes[self.startNodePosition[0], self.startNodePosition[1]].isStart = True
        self.nodes[self.endNodePosition[0], self.endNodePosition[1]].isEnd = True
        
    def draw(self, surface):
        for node in self.nodes.flatten():
            node.draw(surface)