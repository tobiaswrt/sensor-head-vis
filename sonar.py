import pygame
import sys

# Initialisierung von Pygame
pygame.display.init()
pygame.key.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Schwarzer Bildschirm")

clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    
    screen.fill((0, 0, 0))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()