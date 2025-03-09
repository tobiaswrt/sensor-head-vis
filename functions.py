import math
import RPi.GPIO as GPIO
import time
from gpio_config import *

def deg_to_rad(degrees):
    return degrees * math.pi / 180