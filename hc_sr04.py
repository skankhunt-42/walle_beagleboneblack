#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Adafruit_BBIO.GPIO as GPIO
import time

# * TRIGGER		P8_12 gpio1[12] GPIO44	out	pulldown		Mode: 7
# * ECHO		P8_11 gpio1[13] GPIO45	in	pulldown		Mode: 7 *** with R 1KOhm (actually 1.2KOhm)
# * GND			P9_1	GND
# * VCC			P9_5	VDD_5V

echo = "P8_11"
trigger = "P8_12"
gnd = "P9_1"
vcc = "P9_5"

def distanceMeasurement(TRIG,ECHO):

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    pulseStart = time.time()
    pulseEnd = time.time()
    while GPIO.input(ECHO) == 0:
        pulseStart = time.time()
    while GPIO.input(ECHO) == 1:
        pulseEnd = time.time()

    pulseDuration = pulseEnd - pulseStart
    distance = pulseDuration * 17150
    distance = round(distance, 2)
    return distance

#Configuration
GPIO.setup(trigger,GPIO.OUT) #Trigger
GPIO.setup(echo,GPIO.IN)  #Echo


#Security
GPIO.output(trigger, False)
time.sleep(0.5)

#main Loop
try:
    counter = 0
    while True:
       recoveredDIstance = distanceMeasurement(trigger,echo)
       print "Distance: ",recoveredDIstance,"cm"
       counter += 1
       time.sleep(0.1)
       if counter > 200:
       # user_input = raw_input("Stop?: ")
       # if len(user_input) and str(user_input) == 'y':
           GPIO.cleanup()
           break;
except KeyboardInterrupt:
    print "Measurement stopped by user"
    GPIO.cleanup()

