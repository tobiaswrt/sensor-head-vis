from functions import *
import pygame
import sys
import math

# Initialisierung von Pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HC-SR04 Sonar Screen")

GREEN = (0, 214, 35)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2 + SCREEN_HEIGHT // 4

radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.45
line_width = 2

font = pygame.font.SysFont("Arial", 24)
font_small = pygame.font.SysFont("Arial", 16)

# Animations Parameter
scan_angle = 90                         # Startwinkel in Grad
scan_speed = 3                          # Geschwindigkeit der Animation
scan_active = False
scan_pulse_distance = 0                 # Distanz zum Mittelpunkt
pulse_speed = 5                         # Geschwindigkeit des Pulses
max_distance = 400                      # Maximale Entfernung
distance_scale = radius / max_distance  # Skalierungsfaktor für die Anzeige

# Simutlierter Wert (später durch echten HC-SR04 Wert ersetzen)
current_distance = 150 # in cm

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_SPACE:
                 # Scan starten / stoppen
                scan_active = not scan_active
                if scan_active:
                    scan_pulse_distance = 0

            # Distanz mit Pfeiltasten ändern
            if event.key == pygame.K_UP:
                current_distance = min(current_distance + 10, max_distance)
            if event.key == pygame.K_DOWN:
                current_distance = max(current_distance - 10, 0)

    
    screen.fill(BLACK)

    rect = pygame.Rect(
        center_x - radius,
        center_y - radius,
        radius * 2,
        radius * 2
    )

    # Halbkreis zeichnen
    pygame.draw.arc(screen, GREEN, rect, 0, math.pi, line_width)

    # Winkel definieren
    angles = [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi]
    angle_labels = ["0°", "45°", "90°", "135°", "180°"]

    # Abstandsmarkierungen zeichnen
    distance_markers = [100, 200, 300]

    for dist in distance_markers:
        marker_radius = dist * distance_scale
        pygame.draw.arc(screen, GREEN, (center_x - marker_radius, center_y - marker_radius, marker_radius * 2, marker_radius *2), 0, math.pi, 1)

        # Abstandsbeschriftung
        text = font_small.render(f"{dist} cm", True, GREEN)
        text_x = center_x - text.get_width() // 2
        text_y = center_y - marker_radius - text.get_height() - 5
        screen.blit(text, (text_x, text_y))

    # Linien für jeden Winkel
    for i, angle in enumerate(angles):

        end_x = center_x + radius * math.cos(angle)
        end_y = center_y - radius * math.sin(angle)

        # Linien
        pygame.draw.line(screen, GREEN, (center_x, center_y), (end_x, end_y), 1)

        # Markierung der Linien mit dem Kreis
        pygame.draw.circle(screen, GREEN, (int(end_x), int(end_y)), 2)

        text = font.render(angle_labels[i], True, GREEN)

        text_offset = 20

        if angle == 0 or angle == math.pi:  # 0° oder 180°
            text_x = end_x - text.get_width() // 2
            text_y = end_y + text_offset
        elif angle == math.pi/2:  # 90°
            text_x = end_x - text.get_width() // 2
            text_y = end_y - text_offset - text.get_height()
        elif angle == math.pi/4:  # 45°
            text_x = end_x + text_offset // 2
            text_y = end_y - text_offset - text.get_height() // 2
        else:  # 135°
            text_x = end_x - text_offset - text.get_width()
            text_y = end_y - text_offset - text.get_height() // 2

        screen.blit(text, (text_x, text_y))

    # Animation des Scanvorgangs
    if scan_active:
        scan_rad = deg_to_rad(scan_angle)

        # Zeichne Scanlinie vom Mittelpunkt aus
        scan_end_x = center_x + radius * math.cos(scan_rad)
        scan_end_y = center_y - radius * math.sin(scan_rad)
        pygame.draw.line(screen, GREEN, (center_x, center_y), (scan_end_x, scan_end_y), 1)

        # Puls Animation
        if scan_pulse_distance < radius:
            # Zeichne Puls als kleinen Kreis auf Scan Linie
            pulse_x = center_x + scan_pulse_distance * math.cos(scan_rad)
            pulse_y = center_y - scan_pulse_distance * math.sin(scan_rad)
            pygame.draw.circle(screen, GREEN, (int(pulse_x), int(pulse_y)), 4)
            scan_pulse_distance += pulse_speed
        else:
            # Wenn Puls Ende erreicht. akzuelle Distanz anzeigen
            distance_x = center_x + current_distance * distance_scale * math.cos(scan_rad)
            distance_y = center_y - current_distance * distance_scale * math.sin(scan_rad)
            pygame.draw.circle(screen, GREEN, (int(distance_x), int(distance_y)), 8)

            # Nach kurzer Pause neuen Scan starten
            if scan_pulse_distance > radius + 50: # kurze Verzögerung
                scan_pulse_distance = 0
                scan_angle = (scan_angle + scan_speed) % 180 # Winkel aktualisieren

        # AKtuellen Winkel anzeigen
        angle_text = font.render(f"Winkel: {scan_angle}°", True, GREEN)
        screen.blit(angle_text, (50,50))

        # Aktuelle Distanz anzeigen
        distance_text = font.render(f"Distanz: {current_distance} cm", True, GREEN)
        screen.blit(distance_text, (50,100))
    else:
        # Anzeige, dass Scan pausiert ist
        pause_text = font.render("Drücke LEERTASTE zum Scannen", True, GREEN)
        screen.blit(pause_text, (50,50))

    # Mittelpunkt markieren
    pygame.draw.circle(screen, GREEN, (center_x, center_y), 4)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()