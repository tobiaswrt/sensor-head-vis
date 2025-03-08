import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # GPIO-Pins nach BCM-Nummerierung

TRIG = 23               # GPIO23 (Pin 16)
ECHO = 17               # GPIO17 (Pin 11)

GPIO.setup(TRIG, GPIO.OUT)  # Trigger als Ausgang
GPIO.setup(ECHO, GPIO.IN)   # Echo als Eingang
GPIO.output(TRIG, False)    # Trigger initial auf LOW setzen

LED_1 = 27

GPIO.setup(LED_1, GPIO.OUT)

print("Warte auf Sensor...")
time.sleep(2)

def led_blink ():
    GPIO.output(LED_1, GPIO.HIGH)
    time.sleep(4)
    GPIO.output(LED_1, GPIO.LOW)

try:
    while True:

        # Trigger-Puls senden
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # Zeitmessung starten
        led_blink()
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

        print(f"Distanz: {distance} cm")

        time.sleep(1)

except KeyboardInterrupt:
    # Bei STRG + C aufräumen
    print("Messung beendet.")
    GPIO.cleanup()