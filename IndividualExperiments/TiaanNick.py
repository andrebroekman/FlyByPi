#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  motorTest.py jvv

from mMotorDriver import cMotorDriver as md
from time import sleep
import Adafruit_ADS1x15 as Ada
from mTCA9548A import cTCA9548A

print("starting")
motor = md()  # Pins should be 27=DIR, 18=PWM, 22=SLP
motor.setEnable(enabled=1)
motor.setSpeed(20)
#motor.setBackward()
motor.setForward()
sleep(100000)
exit()





for cycle in range(30000):
    motor.setBackward()
    print("Backward")
    sleep(2)
    print("Cycle no " + str(cycle + 1))
    motor.setForward()
    print("Forward")
    sleep(2)
    #motor.setBackward() # Retract pile
    #print("Retract")
    #sleep(5)  # For 30 seconds extend the actuator


print("End of test")
#sleep(1800)
motor.setEnable(enabled=0)
exit()

"""
for i in range(0):
    motor.setBackward()
    print("Backward")
    sleep(5)
    motor.setForward()
    print("Forward")
    sleep(5)

motor.setBackward()
for i in range(100):
    motor.setSpeed(speed=i)
    sleep(0.1)
    print(i)
sleep(1)
motor.toggleDirection()
for i in range(100,50,-1):
    motor.setSpeed(speed=i)
    sleep(0.1)
    print(i)
sleep(2)
""" 

print("Finshed script")
