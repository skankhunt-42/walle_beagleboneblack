import Adafruit_BBIO.GPIO as GPIO
import time


outpin = "P9_12"
GPIO.setup(outpin, GPIO.OUT)
for i in range(0,3):
	GPIO.output(outpin, GPIO.HIGH)
	#time.sleep(3)
	a=raw_input("Next")
	if len(a):
		break
	GPIO.output(outpin, GPIO.LOW)
	#time.sleep(3)
	a=raw_input("Next")
	if len(a):
		break
GPIO.cleanup()

