import pygame
from pygame.math import Vector2
pygame.font.init()
import numpy as np
from Scripts.Grid import Grid
from Scripts.Dijkstra import Dijkstra

resolution = Vector2(1000, 700)
WIN = pygame.display.set_mode((int(resolution.x), int(resolution.y)))
pygame.display.set_caption("Pathfinding Visualizer")

FPS_Font = pygame.font.SysFont('comicsans', 40)
TARGET_FPS = 60

def draw_window(TimePerFrame):
    WIN.fill((20, 80, 145))
    grid.draw(WIN)
    drawlines(WIN)
    drawFPS(TimePerFrame)
    pygame.display.update()
    
    
def getFPS(TimePerFrame):
    return round(1 / TimePerFrame)

def drawFPS(TimePerFrame):
    CurrentFPS = getFPS(TimePerFrame)
    FPS_Text = FPS_Font.render("FPS: "  + str(CurrentFPS), 1, (255, 255, 255))
    WIN.blit(FPS_Text, (int(resolution.x) - 150, 10))
    
gridDimensions = [40, 30] #rows, columns
nodeDimensions = [resolution[0]/gridDimensions[0], resolution[1]/gridDimensions[1]]
grid = Grid(gridDimensions[0], gridDimensions[1], nodeDimensions, Vector2(0,0), Vector2(4,4))
    
def drawlines(surface):
    lineColor = (20, 20, 145)
    for i in range(gridDimensions[1]+1):
        pygame.draw.line(surface, lineColor,
                        (0, int(i * nodeDimensions[1])),
                        (int(gridDimensions[0] * nodeDimensions[0]),int(i * nodeDimensions[1])))
    for i in range(gridDimensions[0]+1):
        pygame.draw.line(surface, lineColor,
                        (int(i * nodeDimensions[0]), 0),
                        (int(i * nodeDimensions[0]),int(gridDimensions[1] * nodeDimensions[1])))
    

def main():
    clock = pygame.time.Clock()
    running = True
    algorithmComplete = False
    blocks = {"S": "start", "E": "end", "W": "wall", "G": "weight"}
    weight = 10
    mouseHold = False
    selectedBlock = "end"
    currentAnimatedNode = None
    while running:
        TimePerFrame  = clock.tick(60) * .001
        dt = TimePerFrame * TARGET_FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            mousePosition = pygame.mouse.get_pos()
            mousePressed = pygame.mouse.get_pressed()
            if mousePressed[0]:
                if algorithmComplete:
                    algorithmComplete = False
                    grid.reset()
                    
                selectedNode = grid.getPressedNode(mousePosition)
                if not (selectedNode.isEnd or selectedNode.isStart):
                    if selectedBlock == "start":
                        grid.changeStartNode(selectedNode)
                    if selectedBlock == "end":
                        grid.changeEndNode(selectedNode)
                    if selectedBlock == "wall":
                        if not mouseHold:
                            wallState = selectedNode.isWall
                        selectedNode.isWall = not wallState
                    if selectedBlock == "weight":
                        if selectedNode.weight != weight:
                            selectedNode.weight = weight
                        else:
                            selectedNode.weight = 0
                mouseHold = True
            else:
                mouseHold = False
                    
            if event.type == pygame.KEYDOWN:
                keysPressed = pygame.key.get_pressed()
                if keysPressed[pygame.K_s]:
                    selectedBlock = blocks["S"]
                if keysPressed[pygame.K_e]:
                    selectedBlock = blocks["E"]
                if keysPressed[pygame.K_w]:
                    selectedBlock = blocks["W"]
                if keysPressed[pygame.K_g]:
                    selectedBlock = blocks["G"]
                if keysPressed[pygame.K_r]:
                    algorithmComplete = False
                    grid.reset()
                if keysPressed[pygame.K_SPACE]:
                    if not algorithmComplete:
                        visitedNodesInOrder, shortestPath = Dijkstra(grid)
                        algorithmComplete = True
                    else:
                        algorithmComplete = False
                        grid.reset()
                
        if algorithmComplete:
            if len(visitedNodesInOrder) or len(shortestPath):
                if len(visitedNodesInOrder):
                    if currentAnimatedNode:
                        currentAnimatedNode.isSelected = False
                    currentAnimatedNode = visitedNodesInOrder[0]
                    visitedNodesInOrder = np.delete(visitedNodesInOrder, 0)
                    currentAnimatedNode.animated = True
                elif len(shortestPath):
                    currentAnimatedNode = shortestPath[-1]
                    currentAnimatedNode.isPath = True
                    shortestPath = np.delete(shortestPath, -1)
                currentAnimatedNode.isSelected = True
                    
        draw_window(TimePerFrame)

    pygame.quit()
    
if __name__ == "__main__":
    main()