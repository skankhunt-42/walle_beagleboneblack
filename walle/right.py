import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM 
import time

verbose = 1

enable = 'P9_22'    # Pin to use for PWM speed control
in1    = 'P9_23'
in2    = 'P9_14'
step = 10.0    # Change in speed
min  = 30.0    # Min duty cycle
max  = 100.0     # Max duty cycle
ms   = 100     # Update time, in ms
speed = min    # Current speed


PWM.start(enable, 0, 1000)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

def clockwise():
	if verbose:
		print "Set clockwise"
	GPIO.output(in1, GPIO.HIGH)
	GPIO.output(in2, GPIO.LOW)

def counter_clockwise():
	if verbose:
		print "Set counter-clockwise"
	GPIO.output(in1, GPIO.LOW)
	GPIO.output(in2, GPIO.HIGH)

def sweep():
	global speed
	global step
	global min
	global max
	speed = speed + step
	if (speed >= max):
		speed = max
	if (speed <= min):
		speed = min
	if verbose:
		print "sweep - speed: [%f]" % (speed)
	PWM.set_duty_cycle(enable, speed)

def increase_speed():
	global speed
	global step
	global min
	global max
	speed = speed + step
	if (speed >= max):
		speed = max
	if (speed <= min):
		speed = min
	if verbose:
		print "speed: [%f]" % (speed)
	PWM.set_duty_cycle(enable, speed)

def decrease_speed():
	global speed
	global step
	global min
	global max
	speed = speed - step
	if (speed >= max):
		speed = max
	if (speed <= min):
		speed = min
	if verbose:
		print "speed: [%f]" % (speed)
	PWM.set_duty_cycle(enable, speed)

print "Initializing..."

clockwise()

for i in range(0,6):
	increase_speed()
	time.sleep(1)

#counter_clockwise()

for i in range(0,7):
	decrease_speed()
	time.sleep(1)

PWM.stop(enable)
GPIO.cleanup()

print "Done!"



