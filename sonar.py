import pygame
import sys
import math

# Initialisierung von Pygame
pygame.init()

screen = pygame.display.set_mode((600, 350))
pygame.display.set_caption("Sonar Bildschirm")

GREEN = (0, 214, 35)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    
    screen.fill(WHITE)

    rect = [220, 140, 200, 200] # Bereich des Kreises (x, y, Breite, Höhe)
    pygame.draw.arc(screen, GREEN, rect, 0, math.pi, 5) # Farbe, Startwinkel 0, Endwinkel π

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()