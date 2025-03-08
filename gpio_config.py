import RPi.GPIO as GPIO # type: ignore
import time

# Pin-Definitionen
LED_1 = 27
LED_2 = 21
LED_3 = 16

TRIG = 23
ECHO = 17

def init_gpio():
    # GPIO-Modus setzen
    GPIO.setmode(GPIO.BCM)
    
    # LED-Pins konfigurieren
    GPIO.setup(LED_1, GPIO.OUT)
    GPIO.setup(LED_2, GPIO.OUT)
    GPIO.setup(LED_3, GPIO.OUT)
    
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

def led_start():
    GPIO.output(LED_1, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LED_2, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LED_3, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LED_1, GPIO.LOW)
    GPIO.output(LED_2, GPIO.LOW)
    GPIO.output(LED_3, GPIO.LOW)