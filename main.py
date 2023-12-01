import pygame
from pygame.math import Vector2
pygame.font.init()
import numpy as np
from Scripts.Grid import Grid
from Scripts.Algorithms.Dijkstra import Dijkstra
from Scripts.Algorithms.Astar import Astar

resolution = Vector2(1500, 900)
WIN = pygame.display.set_mode((int(resolution.x), int(resolution.y)))
pygame.display.set_caption("Pathfinding Visualizer")

TextFont = pygame.font.SysFont('sans-serif', 40)

def getFPS(TimePerFrame):
    return round(1 / TimePerFrame)

def drawFPS(TimePerFrame):
    CurrentFPS = getFPS(TimePerFrame)
    FPS_Text = TextFont.render("FPS: "  + str(CurrentFPS), 1, (255, 255, 255))
    WIN.blit(FPS_Text, (int(resolution.x) - 150, 10))
    
def drawSpeed(speed):
    speedText = TextFont.render("Speed: "  + str(speed), 1, (255, 255, 255))
    WIN.blit(speedText, (10, int(resolution.y) - 40))
    
def drawNodeType(nodeType):
    nodeTypeText = TextFont.render("Selected Node: "  + str(nodeType), 1, (255, 255, 255))
    WIN.blit(nodeTypeText, (10, 10))
    
def drawAlgorithm(algorithm):
    if algorithm == Dijkstra:
        name = "Dijkstra"
    elif algorithm == Astar:
        name = "A*"
    text = "Search Algorithm: "  + name
    speedText = TextFont.render(text, 1, (255, 255, 255))
    WIN.blit(speedText, (int(resolution.x) - len(text)*15, int(resolution.y) - 40))
    
def drawLoading():
    loadingTextFont = pygame.font.SysFont('sans-serif', 60)
    loadingText = loadingTextFont.render("Loading. . .", 1, (255, 255, 255))
    WIN.blit(loadingText, (resolution[0]/2-100, resolution[1]/2-20))
    
def displayLoading():
    drawLoading()
    pygame.display.update()
    
displayLoading()
gridDimensions = [150, 90] #columns, rows
nodeDimensions = [resolution[0]/gridDimensions[0], resolution[1]/gridDimensions[1]]
defaultStartPosition = Vector2(round(gridDimensions[0]/4), round(gridDimensions[1]/2))
defaultEndPosition = Vector2(round(gridDimensions[0]*3/4), round(gridDimensions[1]/2))
grid = Grid(gridDimensions[0], gridDimensions[1], nodeDimensions, defaultStartPosition, defaultEndPosition)
    
def drawlines(surface):
    lineColor = (20, 70, 145)
    for i in range(gridDimensions[1]+1):
        pygame.draw.line(surface, lineColor,
                        (0, int(i * nodeDimensions[1])),
                        (int(gridDimensions[0] * nodeDimensions[0]),int(i * nodeDimensions[1])))
    for i in range(gridDimensions[0]+1):
        pygame.draw.line(surface, lineColor,
                        (int(i * nodeDimensions[0]), 0),
                        (int(i * nodeDimensions[0]),int(gridDimensions[1] * nodeDimensions[1])))

def draw_window(TimePerFrame, speed, nodeType, algorithm):
    WIN.fill((20, 80, 145))
    grid.draw(WIN)
    drawlines(WIN)
    drawFPS(TimePerFrame)
    drawSpeed(speed)
    drawNodeType(nodeType)
    drawAlgorithm(algorithm)
    pygame.display.update()
    
def reset():
    displayLoading()
    grid.reset()
    
def main():
    clock = pygame.time.Clock()
    running = True
    algorithmComplete = False
    blocks = {"S": "start", "E": "end", "W": "wall", "G": "weight"}
    weight = 5
    mouseHold = False
    selectedBlock = "wall"
    timePassed = 0
    speed = 1
    currentAnimatedNode = None
    selectedAlgorithm = Dijkstra
    visitedNodesInOrder = np.empty(0)
    shortestPath = []
    while running:
        TimePerFrame  = clock.tick(300) * .001
        dt = TimePerFrame
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            keysPressed = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if keysPressed[pygame.K_s]:
                    selectedBlock = blocks["S"]
                if keysPressed[pygame.K_e]:
                    selectedBlock = blocks["E"]
                if keysPressed[pygame.K_w]:
                    selectedBlock = blocks["W"]
                if keysPressed[pygame.K_g]:
                    selectedBlock = blocks["G"]
                if keysPressed[pygame.K_F1]:
                    selectedAlgorithm = Dijkstra
                if keysPressed[pygame.K_F2]:
                    selectedAlgorithm = Astar
                if keysPressed[pygame.K_r]:
                    algorithmComplete = False
                    reset()
                if keysPressed[pygame.K_RETURN]:
                    if not algorithmComplete:
                        displayLoading()
                        visitedNodesInOrder, shortestPath = selectedAlgorithm(grid)
                        algorithmComplete = True
                        speed = 1
                        timePassed = 0
                    else:
                        algorithmComplete = False
                        reset()
        
        if keysPressed[pygame.K_UP]:
            speed += 1
        if keysPressed[pygame.K_DOWN]:
            if speed > 1:
                speed -= 1
                
        mousePosition = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        if mousePressed[0]:
            if algorithmComplete:
                algorithmComplete = False
                reset()
                    
            selectedNode = grid.getPressedNode(mousePosition)
            if not (selectedNode.isEnd or selectedNode.isStart):
                if not selectedNode.isWall:
                    if selectedBlock == "start":
                        grid.changeStartNode(selectedNode)
                    if selectedBlock == "end":
                        grid.changeEndNode(selectedNode)
                    
                if selectedBlock == "wall":
                    if not mouseHold:
                        selectedState = not selectedNode.isWall
                    if selectedNode.weight and selectedState:
                        selectedNode.weight = 0
                    selectedNode.isWall = selectedState
                    
                if selectedBlock == "weight":
                    if not mouseHold:
                        if selectedNode.weight != weight:
                            selectedState = True
                        else:
                            selectedState = False
                    if selectedState and not selectedNode.isWall:
                        selectedNode.weight = weight
                    else:
                        selectedNode.weight = 0
            mouseHold = True
        else:
            mouseHold = False
                
        
        if algorithmComplete and (len(visitedNodesInOrder) or len(shortestPath)):
            timePassed += dt
            ticks = int(timePassed // (1/speed))
            timePassed %= (1/speed)
            if ticks:
                for tick in range(ticks):
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
                    
        draw_window(TimePerFrame, speed, selectedBlock, selectedAlgorithm)

    pygame.quit()
    
if __name__ == "__main__":
    main()