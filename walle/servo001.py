import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time


servo_pin = "P9_14"
dc = 50.0
PWM.start(servo_pin, dc, 200)
PWM.set_duty_cycle(servo_pin, dc)
while 1:
	user_input = raw_input("DC: ")
	if len(user_input):
		dc = float(user_input)
	else:
		dc = 0.0
	if dc < 0:
		break	
	PWM.set_duty_cycle(servo_pin, dc)
PWM.cleanup()

