import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
import time
from random import randint
from threading import Thread

verbose = 1

global kill_threads
kill_threads = False

global thread1



# Servo
global last_dc
servo_pin = "P8_13"

# Dual engine
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


def say_no():
    global last_dc
    print "Wally says no!"
    interval = 0.5
    dc = float(60)
    PWM.set_duty_cycle(servo_pin, dc)
    for i in range(0, 3):
        dc = float(25)
        # print dc
        PWM.set_duty_cycle(servo_pin, dc)
        time.sleep(interval)
        dc = float(60)
        # print dc
        PWM.set_duty_cycle(servo_pin, dc)
        time.sleep(interval)
    last_dc = dc


def say_yes():
    global last_dc
    print "Wally says yes!"
    interval = 1
    direction = -1
    if last_dc < 20:
        direction = 1
    dc = last_dc + (float(20) * direction)
    PWM.set_duty_cycle(servo_pin, dc)
    last_dc = dc


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def test_whells():
    global kill_threads
    while not kill_threads:
        print "Initializing whells..."

        clockwise(True)
        clockwise(False)

        for i in range(0, 6):
            increase_speed(True)
            time.sleep(1)
            increase_speed(False)
            time.sleep(1)

        for i in range(0, 7):
            decrease_speed(True)
            time.sleep(1)
            decrease_speed(False)
            time.sleep(1)

        clockwise(True)
        counter_clockwise(False)

        for i in range(0, 6):
            increase_speed(True)
            time.sleep(1)
            increase_speed(False)
            time.sleep(1)

        for i in range(0, 7):
            decrease_speed(True)
            time.sleep(1)
            decrease_speed(False)
            time.sleep(1)

def main():
    global last_dc
    dc = 50.0
    last_dc = dc
    PWM.start(servo_pin, dc, 200)
    PWM.set_duty_cycle(servo_pin, dc)
    thread1.start()
    while 1:
        user_input = raw_input("DC 1: ")
        if len(user_input):
            if not is_number(user_input):
                if str(user_input) == 'y':
                    say_yes()
                if str(user_input) == 'n':
                    say_no()
                continue
            dc = float(user_input)
            if dc < 0:
                print "Executing special command: [%s]" % (dc)
                if float(dc) == float(-2):
                    say_no()
                    continue
                elif float(dc) == float(-3):
                    say_yes()
                    continue
                else:
                    break
            if dc > 99:
                dc = 99
        else:
            dc = float(randint(0, 60))
            print "random value: [%d]" % int(dc)
        if dc < 0:
            break
        PWM.set_duty_cycle(servo_pin, dc)
        last_dc = dc


def clear():
    global kill_threads
    kill_threads = True
    counter = 0
    while thread1.is_alive():
        print "Waiting for whells thread to stop... [%d]" % counter
        counter += 1
        time.sleep(1)
    outpin = servo_pin
    PWM.stop(enableR)
    PWM.stop(enableL)
    PWM.cleanup()
    GPIO.setup(outpin, GPIO.OUT)
    GPIO.output(outpin, GPIO.LOW)
    GPIO.cleanup()

    print "Done!"

thread1 = Thread(target=test_whells)
main()
clear()
