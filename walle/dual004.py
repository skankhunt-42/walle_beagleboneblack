# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt

import sys
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time

import os, struct, array
from fcntl import ioctl


verbose = 1

global enableR
global enableL

enableR = 'P9_21'    # Pin to use for PWM speed control for motor on the right
in1R    = 'P9_15'
in2R   = 'P9_16'
enableL = 'P9_22'    # Pin to use for PWM speed control for motor on the left
in1L    = 'P9_23'
in2L   = 'P9_14'
step = 10.0    # Change in speed
min  = 25.0    # Min duty cycle
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
	PWM.set_duty_cycle(enableR, speed)
	time.sleep(0.2)
	PWM.set_duty_cycle(enableL, speed)

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
	PWM.set_duty_cycle(enableR, speed)
	time.sleep(0.2)
	PWM.set_duty_cycle(enableL, speed)


def shutdown(): 
  global enableR
  global enableL
  PWM.stop(enableR)
  time.sleep(1.0)
  PWM.stop(enableL)
  time.sleep(1.0)
  GPIO.cleanup()
  PWM.cleanup()
  print "Done!"
  sys.exit(0)
                
                
# Iterate over the joystick devices.
print('Available devices:')

for fn in os.listdir('/dev/input'):
  if fn.startswith('js'):
    print('  /dev/input/%s' % (fn))

# We'll store the states here.
axis_states = {}
button_states = {}

# These constants were borrowed from linux/input.h
axis_names = {
  0x00 : 'x',
  0x01 : 'y',
  0x02 : 'z',
  0x03 : 'rx',
  0x04 : 'ry',
  0x05 : 'rz',
  0x06 : 'trottle',
  0x07 : 'rudder',
  0x08 : 'wheel',
  0x09 : 'gas',
  0x0a : 'brake',
  0x10 : 'hat0x',
  0x11 : 'hat0y',
  0x12 : 'hat1x',
  0x13 : 'hat1y',
  0x14 : 'hat2x',
  0x15 : 'hat2y',
  0x16 : 'hat3x',
  0x17 : 'hat3y',
  0x18 : 'pressure',
  0x19 : 'distance',
  0x1a : 'tilt_x',
  0x1b : 'tilt_y',
  0x1c : 'tool_width',
  0x20 : 'volume',
  0x28 : 'misc',
}

button_names = {
  0x120 : 'trigger',
  0x121 : 'thumb',
  0x122 : 'thumb2',
  0x123 : 'top',
  0x124 : 'top2',
  0x125 : 'pinkie',
  0x126 : 'base',
  0x127 : 'base2',
  0x128 : 'base3',
  0x129 : 'base4',
  0x12a : 'base5',
  0x12b : 'base6',
  0x12f : 'dead',
  0x130 : 'a',
  0x131 : 'b',
  0x132 : 'c',
  0x133 : 'x',
  0x134 : 'y',
  0x135 : 'z',
  0x136 : 'tl',
  0x137 : 'tr',
  0x138 : 'tl2',
  0x139 : 'tr2',
  0x13a : 'select',
  0x13b : 'start',
  0x13c : 'mode',
  0x13d : 'thumbl',
  0x13e : 'thumbr',

  0x220 : 'dpad_up',
  0x221 : 'dpad_down',
  0x222 : 'dpad_left',
  0x223 : 'dpad_right',

  # XBox 360 controller uses these codes.
  0x2c0 : 'dpad_left',
  0x2c1 : 'dpad_right',
  0x2c2 : 'dpad_up',
  0x2c3 : 'dpad_down',
}

axis_map = []
button_map = []

# Open the joystick device.
fn = '/dev/input/js0'
print('Opening %s...' % fn)
jsdev = open(fn, 'rb')

# Get the device name.
#buf = bytearray(63)
buf = array.array('c', ['\0'] * 64)
ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
js_name = buf.tostring()
print('Device name: %s' % js_name)

# Get number of axes and buttons.
buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
num_axes = buf[0]

buf = array.array('B', [0])
ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
num_buttons = buf[0]

# Get the axis map.
buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

for axis in buf[:num_axes]:
  axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
  axis_map.append(axis_name)
  axis_states[axis_name] = 0.0

# Get the button map.
buf = array.array('H', [0] * 200)
ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

for btn in buf[:num_buttons]:
  btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
  button_map.append(btn_name)
  button_states[btn_name] = 0

print '%d axes found: %s' % (num_axes, ', '.join(axis_map))
print '%d buttons found: %s' % (num_buttons, ', '.join(button_map))

#sys.exit(0)

print "Initializing..."

clockwise(True)
clockwise(False)

# Main event loop
while True:
  evbuf = jsdev.read(8)
  if evbuf:
    time_evbuf, value, type, number = struct.unpack('IhBB', evbuf)

    #if type & 0x80:
    #  print "(initial)"

    if type & 0x01:
      button = button_map[number]
      if button:
        button_states[button] = value
        if value:
          print "%s pressed" % (button)
          if str(button) == "unknown(0x12d)":
            shutdown()
    #else:
    #  print "%s released" % (button)

    if type & 0x02:
      axis = axis_map[number]
      if axis:
        fvalue = value / 32767.0
        axis_states[axis] = fvalue
        message =  "%s: %.3f" % (axis, fvalue)
        if not str(message).startswith("unknown"):
          print message
          #print "%s: %.3f" % (axis, fvalue)
        if str(axis) == "y":
          print "fvalue: [%f]" % fvalue
          if fvalue < 0:
            counter_clockwise(True)
            fvalue = fvalue * -1
          else:
            clockwise(True)
          dc = (fvalue*1000.0)
          if dc < 1.0:
            dc = 1.0
          if dc > 99.0:
            dc = 99.0
          print "enableL: [%s] dc: [%f]" % (enableL, dc)
          PWM.set_duty_cycle(enableL, dc)
          
        if str(axis) == "rz":
          print "fvalue: [%f]" % fvalue
          if fvalue < 0:
            counter_clockwise(False)
            fvalue = fvalue * -1
          else:
            clockwise(False)
          dc = (fvalue*1000.0)
          if dc < 1.0:
            dc = 1.0
          if dc > 99.0:
            dc = 99.0
          print "enableR: [%s] dc: [%f]" % (enableR, dc)
          PWM.set_duty_cycle(enableR, dc)
                  



#time.sleep(1)
#PWM.set_duty_cycle(enableR, 40.0)
#time.sleep(1)
#PWM.set_duty_cycle(enableL, 40.0)
#time.sleep(5)
#counter_clockwise(False)
#time.sleep(5)
#PWM.set_duty_cycle(enableR, 10.0)
#time.sleep(1)
#PWM.set_duty_cycle(enableL, 10.0)
#time.sleep(1)


shutdown()





