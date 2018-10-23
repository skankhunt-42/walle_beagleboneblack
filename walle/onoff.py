import Adafruit_BBIO.GPIO as GPIO
import time


outpin = "P9_3"
GPIO.setup(outpin, GPIO.OUT)
while 1:
	user_in = raw_input("1:on 0:off -1:shutdown  ")
	if int(user_in) == 1:
		print "Engine start"
		#GPIO.output(outpin, GPIO.HIGH)
	elif int(user_in) == 0:
		GPIO.output(outpin, GPIO.LOW)
		print "Engine stop"
	else:
		break
	time.sleep(1)
GPIO.output(outpin, GPIO.LOW)
GPIO.cleanup()
print "Done!"

