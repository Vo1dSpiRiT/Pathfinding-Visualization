from Scripts.Node import Node
import numpy as np

class Grid():
    def __init__(self, rows, cols, nodeDimensions, startNodePosition, endNodePosition):
        self.rows = rows
        self.cols = cols
        self.nodeDimensions = nodeDimensions
        self._startNodePosition = startNodePosition
        self._endNodePosition = endNodePosition
        self.nodes = self.getNodes()
        self.startNode = self.getStartNode()
        self.endNode = self.getEndNode()
        
    def __getitem__(self, index):
        return self.nodes[index]
    
    def __setitem__(self, index, value):
        self.nodes[index] = value
        
    def getNodes(self):
        nodes = np.empty((self.rows, self.cols), dtype=object)
        for i in range(self.rows):
            for j in range(self.cols):
                nodes[i, j] = Node(i, j, self.nodeDimensions)
        nodes[int(self.startNodePosition.x), int(self.startNodePosition.y)].isStart = True
        nodes[int(self.endNodePosition.x), int(self.endNodePosition.y)].isEnd = True
        return nodes
    
    def draw(self, surface):
        for node in self.nodes.flatten():
            node.draw(surface)
    
    def reset(self):
        self.nodes = self.getNodes()
        
    def getPressedNode(self, mousePosition):
        row = int(mousePosition[0] // self.nodeDimensions[0])
        col = int(mousePosition[1] // self.nodeDimensions[1])
        return self.nodes[row, col]
    def getStartNode(self):
        return self.nodes[int(self.startNodePosition.x), int(self.startNodePosition.y)]
        
    def getEndNode(self):
        return self.nodes[int(self.endNodePosition.x), int(self.endNodePosition.y)]

    def changeStartNode(self, node):
        self.startNodePosition = node.position
        
    def changeEndNode(self, node):
        self.endNodePosition = node.position
    
    @property
    def startNodePosition(self):
        return self._startNodePosition
    
    @startNodePosition.setter
    def startNodePosition(self, newPosition):
        self._toggleStartNode()
        self._startNodePosition = newPosition
        self.startNode = self.getStartNode()
        self._toggleStartNode()
        
    @property
    def endNodePosition(self):
        return self._endNodePosition
    
    @endNodePosition.setter
    def endNodePosition(self, newPosition):
        self._toggleEndNode()
        self._endNodePosition = newPosition
        self.endNode = self.getEndNode()
        self._toggleEndNode()
    
    def _toggleStartNode(self):
        self.startNode.isStart = not self.startNode.isStart

    def _toggleEndNode(self):
        self.endNode.isEnd = not self.endNode.isEnd
        