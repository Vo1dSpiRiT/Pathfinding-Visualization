from Scripts.Node import Node
import numpy as np

class Grid():
    def __init__(self, rows, cols, startNodePosition, endNodePosition):
        self.rows = rows
        self.cols = cols
        self.startNodePosition = startNodePosition
        self.endNodePosition = endNodePosition
        self.nodes = self.getNodes()
        
    def getNodes(self):
        nodes = np.array((self.rows, self.cols), dtype=object)
        for i in range(self.rows):
            for j in range(self.cols):
                nodes[i, j] = Node(i, j)
        nodes[self.startNodePosition.x, self.startNodePosition.y].isStart = True
        nodes[self.endNodePosition.x, self.endNodePosition.y].isEnd = True
    
    def __getitem__(self, index):
        return self.nodes[index]
    
    def __setitem__(self, index, value):
        self.nodes[index] = value
        
    def reset(self):
        self.nodes = self.getNodes()
        
    def update(self, startNodePosition, endNodePosition):
        self.nodes[self.startNodePosition.x, self.startNodePosition.y].isStart = False
        self.nodes[self.endNodePosition.x, self.endNodePosition.y].isEnd = False
        self.startNodePosition = startNodePosition
        self.endNodePosition = endNodePosition
        self.nodes[self.startNodePosition.x, self.startNodePosition.y].isStart = True
        self.nodes[self.endNodePosition.x, self.endNodePosition.y].isEnd = True