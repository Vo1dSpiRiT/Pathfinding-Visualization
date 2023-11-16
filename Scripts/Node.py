import pygame

class Node():
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.isStart = False
        self.isEnd = False
        self.isVisited = False
        self.weight = 0
        self.distance = float('inf')
        self.color = (0, 0, 255)
        
    def draw(self, surface, dimensions):
        pygame.draw.rect(surface, self.color, self.position*dimensions)
        
    