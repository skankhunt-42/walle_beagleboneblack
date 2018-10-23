import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
from random import randint

global last_dc

servo_pin = "P9_14"
dc = 50.0
last_dc = dc

def say_no():
        global last_dc
        print "Wally says no!"
        interval = 0.5
        dc = float(60)
        PWM.set_duty_cycle(servo_pin, dc)
        for i in range(0,3):
                dc = float(25)
                #print dc
                PWM.set_duty_cycle(servo_pin, dc)
                time.sleep(interval)
                dc = float(60)
                #print dc
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


PWM.start(servo_pin, dc, 200)
PWM.set_duty_cycle(servo_pin, dc)
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
        time.sleep(0.5)

outpin = servo_pin
PWM.cleanup()
GPIO.setup(outpin, GPIO.OUT)
GPIO.output(outpin, GPIO.LOW)
GPIO.cleanup()

print "Done!"

