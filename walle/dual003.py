import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM 
import time

verbose = 1

enableR = 'P9_21'    # Pin to use for PWM speed control for motor on the right
in1R    = 'P9_15'
in2R   = 'P9_16'
enableL = 'P9_22'    # Pin to use for PWM speed control for motor on the left
in1L    = 'P9_23'
in2L   = 'P9_14'
step = 5.0    # Change in speed
min  = 10.0    # Min duty cycle
max  = 100.0     # Max duty cycle
ms   = 100     # Update time, in ms
speed = min    # Current speed


PWM.start(enableR, 0, 1000)
PWM.start(enableL, 0, 1000)
GPIO.setup(in1R, GPIO.OUT)
GPIO.setup(in1L, GPIO.OUT)
GPIO.setup(in2R, GPIO.OUT)
GPIO.setup(in2L, GPIO.OUT)

def clockwise(left=False):
	if verbose:
		print "Set clockwise"
	in1 = in1R
	in2 = in2R
	if left:
		print "left"
		in1 = in1L
		in2 = in2L
	else:
		print "right"
	GPIO.output(in1, GPIO.HIGH)
	GPIO.output(in2, GPIO.LOW)

def counter_clockwise(left=False):
	if verbose:
		print "Set counter-clockwise"
	in1 = in1R
	in2 = in2R
	if left:
		print "left"
		in1 = in1L
		in2 = in2L
	else:
		print "right"
	GPIO.output(in1, GPIO.LOW)
	GPIO.output(in2, GPIO.HIGH)

def sweep(left=False):
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
	enable = enableR
	if left:
		enable = enableL
	PWM.set_duty_cycle(enable, speed)

def increase_speed(left=False):
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
	enable = enableR
	if left:
		print "Increase left"
		enable = enableL
	else:
		print "Increase right"
	PWM.set_duty_cycle(enable, speed)

def decrease_speed(left=False):
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
	enable = enableR
	if left:
		print "Decrease left"
		enable = enableL
	else:
		print "Decrease right"
	PWM.set_duty_cycle(enable, speed)

print "Initializing..."

clockwise(True)
clockwise(False)

for i in range(0,6):
	increase_speed(True)
	time.sleep(1)
	increase_speed(False)
	time.sleep(1)

#counter_clockwise()

for i in range(0,7):
	decrease_speed(True)
	time.sleep(1)
	decrease_speed(False)
	time.sleep(1)

PWM.stop(enableR)
PWM.stop(enableL)
GPIO.cleanup()

print "Done!"



