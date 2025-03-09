import pygame
import sys
import math

# Initialisierung von Pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sonar Bildschirm")

GREEN = (0, 214, 35)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2

radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.45
line_width = 2

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    
    screen.fill(BLACK)

    rect = pygame.Rect(
        center_x - radius,
        center_y - radius,
        radius * 2,
        radius * 2
    )

    pygame.draw.arc(screen, GREEN, rect, 0, math.pi, line_width)

    pygame.draw.circle(screen, GREEN, (center_x, center_y), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()