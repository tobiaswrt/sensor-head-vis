import math
import RPi.GPIO as GPIO
import time
from gpio_config import *

def deg_to_rad(degrees):
    return degrees * math.pi / 180

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