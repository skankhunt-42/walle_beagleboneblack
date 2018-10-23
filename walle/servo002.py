import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time


servo_pin = "P9_14"
dc = 0.0
PWM.start(servo_pin, dc, 200)
PWM.set_duty_cycle(servo_pin, dc)
while 1:
	user_input = raw_input("Angle: ")
	if len(user_input):
		ang = float(user_input)
	else:
		ang = 0.0
	if ang > 180:
		ang = 180
	if ang < 0:
		break	
	dc = float(5.0/18.0*ang+1)
	print "dc: [%f]" % (dc) 
	PWM.set_duty_cycle(servo_pin, dc)
PWM.cleanup()

