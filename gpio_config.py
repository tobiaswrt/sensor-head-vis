import RPi.GPIO as GPIO
import time

# Pin-Definitionen
LED_1 = 27
TRIG = 23
ECHO = 17

def init_gpio():
    # GPIO-Modus setzen
    GPIO.setmode(GPIO.BCM)
    
    # LED-Pins konfigurieren
    GPIO.setup(LED_1, GPIO.OUT)
    
    # Ultraschallsensor-Pins konfigurieren
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)  # Trigger initial auf LOW setzen

def cleanup_gpio():
    GPIO.cleanup()

def led_blink():
    GPIO.output(LED_1, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LED_1, GPIO.LOW)