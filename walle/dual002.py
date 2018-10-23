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
step = 10.0    # Change in speed
min  = 30.0    # Min duty cycle
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
		in1 = in1L
		in2 - in2L
	GPIO.output(in1, GPIO.HIGH)
	GPIO.output(in2, GPIO.LOW)

def counter_clockwise(left=False):
	if verbose:
		print "Set counter-clockwise"
	in1 = in1R
	in2 = in2R
	if left:
		in1 = in1L
		in2 - in2L
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
		enable = enableL
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
		enable = enableL
	PWM.set_duty_cycle(enable, speed)

print "Initializing..."

clockwise()

for i in range(0,7):
	increase_speed()
	time.sleep(1)

counter_clockwise()

for i in range(0,3):
	decrease_speed()
	time.sleep(1)

PWM.stop(enableR)
PWM.stop(enableL)
GPIO.cleanup()

print "Done!"


#outpin = "P9_12"
#GPIO.setup(outpin, GPIO.OUT)
#for i in range(0,3):
#	GPIO.output(outpin, GPIO.HIGH)
#	time.sleep(3)
#	GPIO.output(outpin, GPIO.LOW)
#	time.sleep(3)
#GPIO.cleanup()

