#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fly-by-Pi Controller

Demonstration on the use of simple time-based cyclic control
for controlling an actuator. The speed (duty-cycle) of the
motor is defined followed by a number of load-unload cycles.

Run using: sudo python3 TimeControl.py
Modified by Andre Broekman 2020/05/13
Open Source License: Creative Commons Attribution-ShareAlike
"""

from mMotorDriver import cMotorDriver as md
from time import sleep

print("Fly-by-Pi Time Control Demonstration")
motor = md()  # pin connections should be 27=DIR, 18=PWM, 22=SLP
motor.setEnable(enabled=0)  # disable the motor driver
motor.setSpeed(20)  # set the duty-cycle to 20%
motor.setForward()  # set starting configuration to push
motor.setEnable(enabled=1)  # enble the motor driver

for cycle in range(1000):  # for a certain number of cycles
    print("Cycle no: " + str(cycle + 1))
	motor.setBackward()  # set the motor to retract
    print("Retracting")
    sleep(2)  # retract the actuator for 2 seconds
    motor.setForward()  # set the motor to extend
    print("Extending")
    sleep(2)  # extend the actuator for 2 seconds
    
motor.setEnable(enabled=0)  # disable the motor driver
exit(0)
print("End of the demonstration")
