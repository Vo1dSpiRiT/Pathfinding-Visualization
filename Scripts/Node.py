import pygame

class Node():
    def __init__(self, x, y, dimensions):
        self.position = pygame.Vector2(x, y)
        self.dimensions = dimensions
        self.isStart = False
        self.isEnd = False
        self.isVisited = False
        self.weight = 0
        self.distance = float('inf')
        self.color = (0, 0, 255)
        self.rect = pygame.Rect(int(self.position.x*self.dimensions[0]),
                           int(self.position.y*self.dimensions[1]),
                           self.dimensions[0], self.dimensions[1])
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        
    