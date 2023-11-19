import pygame

class Node():
    colors = {"unvisited": None,
              "visited": [(255, 50, 50), (200, 55, 0)],
              "start": [(100, 0, 150), (180, 0, 190)],
              "end": [(255, 150, 0), (255, 100, 0)],
              "wall": [(70, 70, 70), (50, 50, 50)],
              "path": [(120, 220, 0), (0, 153, 76)],
              "selected": [(255, 255, 0), (220, 200, 50)]}
    def __init__(self, x, y, dimensions):
        self.position = pygame.Vector2(x, y)
        self.dimensions = dimensions
        self._isStart = False
        self._isEnd = False
        self._isVisited = False
        self._isWall = False
        self._isPath = False
        self._isSelected = False
        self._animated = False
        self.weight = 0
        self.distance = float('inf')
        self.previousNode = None
        self.color = Node.colors["unvisited"]
        self.updateColor()
        self.rect = pygame.Rect(int(self.position.x*self.dimensions[0]),
                           int(self.position.y*self.dimensions[1]),
                           self.dimensions[0], self.dimensions[1])
        
    def __repr__(self):
        return f"{self.position.x}, {self.position.y}"
        
    def draw(self, surface):
        if self.color:
            pygame.draw.rect(surface, self.color[0], self.rect)
        
    def updateColor(self):
        if self.isStart:
            self.color = Node.colors["start"]
        elif self.isEnd:
            self.color = Node.colors["end"]
        elif self.isSelected:
            self.color = Node.colors["selected"]
        elif self.isWall:
            self.color = Node.colors["wall"]
        elif self.animated:
            if self.isPath:
                self.color = Node.colors["path"]
            elif self._isVisited:
                self.color = Node.colors["visited"]

        else:
            self.color = Node.colors["unvisited"]
                        
    @property
    def isStart(self):
        return self._isStart
    
    @isStart.setter
    def isStart(self, value):
        self._isStart = value
        self.updateColor()
        
    @property
    def isEnd(self):
        return self._isEnd
    
    @isEnd.setter
    def isEnd(self, value):
        self._isEnd = value
        self.updateColor()
        
    @property
    def isWall(self):
        return self._isWall
    
    @isWall.setter
    def isWall(self, value):
        self._isWall = value
        self.updateColor()
        
    @property
    def isVisited(self):
        return self._isVisited
    
    @isVisited.setter
    def isVisited(self, value):
        self._isVisited = value
        self.updateColor()
        
    @property
    def isPath(self):
        return self._isPath
    
    @isPath.setter
    def isPath(self, value):
        self._isPath = value
        self.updateColor()
        
    @property
    def isSelected(self):
        return self._isSelected
    
    @isSelected.setter
    def isSelected(self, value):
        self._isSelected = value
        self.updateColor()
        
    @property
    def animated(self):
        return self._animated
    
    @animated.setter
    def animated(self, value):
        self._animated = value
        self.updateColor()
        