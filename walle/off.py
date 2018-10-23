import Adafruit_BBIO.GPIO as GPIO
import time


outpin = "P9_12"
GPIO.setup(outpin, GPIO.OUT)
GPIO.output(outpin, GPIO.LOW)
GPIO.cleanup()

