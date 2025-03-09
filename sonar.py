import pygame
import sys
import math

# Initialisierung von Pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sonar Bildschirm")

GREEN = (0, 214, 35)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2 + SCREEN_HEIGHT // 4

radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.45
line_width = 2

font = pygame.font.Font(None, 36)

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

    angles = [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi]
    angle_labels = ["0°", "45°", "90°", "135°", "180°"]

    for i, angle in enumerate(angles):

        end_x = center_x + radius * math.cos(angle)
        end_y = center_y - radius * math.sin(angle)

        pygame.draw.line(screen, GREEN, (center_x, center_y), (end_x, end_y), 1)

        pygame.draw.circle(screen, GREEN, (int(end_x), int(end_y)), 2)

        text = font.render(angle_labels[i], True, GREEN)

        text_offset = 25

        if angle == 0 or angle == math.pi:
            text_x = end_x - text.get_width() // 2
            text_y = end_y + text_offset
        elif angle == math.pi/2:
            text_x = end_x - text.get_width() // 2
            text_y = end_y - text_offset - text.get_height()
        elif angle == math.pi/4:
            text_x = end_x - text.get_width() // 2
            text_y = end_y - text_offset - text.get_height() // 2
        else:
            text_x = end_x - text_offset - text.get_width()
            text_y = end_y - text_offset - text.get_width() // 2

        screen.blit(text, (text_x, text_y))

    pygame.draw.circle(screen, GREEN, (center_x, center_y), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()