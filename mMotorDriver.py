#!/usr/bin/python3
"""
Fly-by-Pi Controller
	
Class file for the motor driver (Pololu 24v13). Simplifies the
control motor driver by exposing function to enable/disengage
the motor, set the speed (duty cycle) and direction of movement.
Standard Raspberry Pi pinouts are used.

Modified by Andre Broekman 2020/05/13
Open Source License: Creative Commons Attribution-ShareAlike
"""

import RPi.GPIO as GPIO
from time import sleep

class cMotorDriver:
    def __init__(self): 
        self.pinAssign = [18, 27, 22]  # PWM, DIR, SLP
        self.enabled = 0    # LOW state disables the driver, HIGH state enables the driver
        self.direction = 0  # 0 = Current flows from OUTB to OUTA // 1 = Current flows from OUTA to OUTB
        self.speed = 0      # PWM value
        try:
            GPIO.setmode(GPIO.BCM)  # Use Broadcom chip-specific numbering scheme
            for pin in self.pinAssign:  # Set all pins as output
                GPIO.setup(pin, GPIO.OUT)
            self.p = GPIO.PWM(self.pinAssign[0], 300) # 300 Hz PWM frequency
            self.p.start(0) # Start the PWM generator (0% duty cycle)
        except:
            print("MotorDriver class _init_ exception")


    def setEnable(self, enabled=0):  # enable the motor
        try:
            if enabled == 1:
                GPIO.output(self.pinAssign[2], 1)
                self.enabled = 1
            else:
                GPIO.output(self.pinAssign[2], 0)
                self.enabled = 0
        except:
            print("motor enable: try exception")


    def toggleSleep(self):  # toggle the motor sleep state
        try:
            if self.enabled == 0:
                GPIO.output(self.pinAssign[2], 1)
                self.enabled = 1
            else:
                GPIO.output(self.pinAssign[2], 0)
                self.enabled = 0
        except:
            print("motor sleep toggle: try exception")


    def setForward(self):  # set the actuator to extend (go forward)
        try:
            GPIO.output(self.pinAssign[1], 1)
            self.direction = 1
        except:
            print("motor forward: try exception")


    def setBackward(self):  # set the actuator to retract (go backward)
        try:
            GPIO.output(self.pinAssign[1], 0)
            self.direction = 0
        except:
            print("motor backward: try exception")


    def toggleDirection(self):  # toggle the direction of the motor
        try:
            if self.direction == 0:
                GPIO.output(self.pinAssign[1], 1)
                self.direction = 1
            else:
                GPIO.output(self.pinAssign[1], 0)
                self.direction = 0
        except:
            print("motor sleep toggle: try exception")


    def setSpeed(self, speed=0):  # set the duty cycle of PWM pin (0-100%)
        if speed in range(101):
            try:
                self.p.ChangeDutyCycle(speed)
            except:
                print("motor speed: try exception")
        else:
            try:
                self.p.ChangeDutyCycle(0)
            except:
                print("motor speed: catastrophic exception")
   