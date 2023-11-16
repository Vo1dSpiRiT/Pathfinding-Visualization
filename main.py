import pygame
from pygame.math import Vector2
pygame.font.init()

resolution = Vector2(1000, 700)
WIN = pygame.display.set_mode((int(resolution.x), int(resolution.y)))
pygame.display.set_caption("FLAPPY BIRD!")

FPS_Font = pygame.font.SysFont('comicsans', 40)
TARGET_FPS = 60

def draw_window(TimePerFrame):
    WIN.fill((0, 0, 0))
    drawFPS(TimePerFrame)
    pygame.display.update()
    
    
def getFPS(TimePerFrame):
    return round(1 / TimePerFrame)

def drawFPS(TimePerFrame):
    CurrentFPS = getFPS(TimePerFrame)
    FPS_Text = FPS_Font.render("FPS: "  + str(CurrentFPS), 1, (255, 255, 255))
    WIN.blit(FPS_Text, (int(resolution.x) - 150, 10))

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        TimePerFrame  = clock.tick(60) * .001
        dt = TimePerFrame * TARGET_FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                    
                    

        draw_window(TimePerFrame)

    pygame.quit()
    
if __name__ == "__main__":
    main()