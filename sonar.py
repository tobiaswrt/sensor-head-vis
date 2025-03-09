from functions import *
from gpio_config import *
import RPi.GPIO as GPIO
import pygame
import sys
import math
import threading

# Initialisierung
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
scan_active = False
wave_radius = 0 # Radius der ausbreitenden Welle
wave_speed = 2  # Geschwindigkeit der Welle
max_distance = 400  # Maximale Entfernung in cm
distance_scale = radius / max_distance  # Skalierungsfaktor für die Anzeige

waves = []  # Liste von [radius, alpha] für jede Welle
wave_interval = 80  # Abstand zwischen den Wellen

# Simutlierter Wert (später durch echten HC-SR04 Wert ersetzen)
current_distance = 0 # in cm
current_angle_rad = math.pi/2
detected_point = None

running = True

def measure_distance():
    # Trigger-Puls senden
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Zeitmessung starten
    pulse_start = time.time()
    timeout = pulse_start + 0.1

    # Warten bis Echo HIGH wird
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        pulse_start = time.time()

    pulse_end = time.time()
    timeout = pulse_end + 0.1

    # Warten bis Echo wieder LOW wird
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        pulse_end = time.time()

    # Berechnung Zeitdauer
    pulse_duration = pulse_end - pulse_start

    # Entfernung berechnen (Schallgeschwindigkeit = 34300 cm/s)
    # Durch 2 teilen, da Signal hin und zurück läuft
    distance = round(pulse_duration * 34300 / 2, 2)

    if distance > max_distance:
        distance = max_distance
    elif distance < 0:
        distance = 0

    return distance

def sensor_thread():
    global current_distance, running, scan_active

    while running:
        if scan_active:
            current_distance = measure_distance()
            
        time.sleep(0.05)

# Hauptschleife
try:
    init_gpio()

    # Sensor-Thread starten
    sensor = threading.Thread(target = sensor_thread)
    sensor.daemon = True    # Thread endet, wenn Hauptprogramm endet
    sensor.start() 

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
                        waves = [[0, 255]]
        
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
            # Wellen aktualisieren und zeichnen
            new_waves = []
            for wave in waves:
                wave_radius, alpha = wave

                # Halbkreis für die Welle zeichnen
                wave_color = (0, 214, 35, alpha)

                # Transparente Surface für die Welle erstellen
                wave_surface = pygame.Surface((wave_radius * 2, wave_radius * 2), pygame.SRCALPHA)
                pygame.draw.arc(wave_surface, wave_color, (0, 0, wave_radius * 2, wave_radius * 2), 0, math.pi, 2)

                # Surface auf den Hauptbildschirm übertragen
                screen.blit(wave_surface, (center_x - wave_radius, center_y - wave_radius))

                wave_radius  += wave_speed
                alpha_decrease = 2
                alpha = max(0, alpha - alpha_decrease) # Welle wird transparenter

                # Welle beibehalten, wenn sie noch sichtbar ist
                if wave_radius < radius:
                    new_waves.append([wave_radius, alpha])

                # Wenn eine Welle die aktuelle Distanz erreicht
                if abs(wave_radius - current_distance * distance_scale) < wave_speed and alpha > 150:
                    # Erkennungswert im 90° Winkel (direkt nach oben)
                    angle_rad = math.pi/2   # 90° in Radianten
                    detected_point = (
                        center_x + current_distance * distance_scale * math.cos(angle_rad),
                        center_y - current_distance * distance_scale * math.sin(angle_rad)
                    )

            # Neue Welle zeichnen, falls nötig
            if not waves or waves [0][0] > wave_interval:
                new_waves.insert(0, [0, 255])

            waves = new_waves

            # Erkanntes Objekt zeichnen
            if detected_point:
                pygame.draw.circle(screen, GREEN, (int(detected_point[0]), int(detected_point[1])), 8)

            # Aktuelle Distanz anzeigen
            distance_text = font.render(f"Distanz: {current_distance} cm", True, BLACK)
            screen.blit(distance_text, (50, 50))
        else:
            # Anzeige, dass Scan pausiert ist
            pause_text = font.render("Drücke LEERTASTE zum Scannen", True, GREEN)
            screen.blit(pause_text, (50,50))

        # Mittelpunkt markieren
        pygame.draw.circle(screen, GREEN, (center_x, center_y), 4)

        pygame.display.flip()
        clock.tick(60)

except KeyboardInterrupt:
    print("Programm beendet.")
finally:
    running = False
    cleanup_gpio()
    pygame.quit()
    sys.exit()