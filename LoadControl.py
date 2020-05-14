#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fly-by-Pi Controller
	
Demonstration on the use of the load control functionality.
The load is obtained by the centrifuge's DAQ system, sent
through the MCP3424 ADC. The feedback frequency is approximately
63 Hz using this method, yielding an update rate of 15 ms.

Run using: sudo python3 LoadControl.py
Modified by Andre Broekman 2020/05/13
Open Source License: Creative Commons Attribution-ShareAlike
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time, os
from mMotorDriver import cMotorDriver as md

try:
    from mMCP3424 import ADCDifferentialPi
except ImportError:
    print("Failed to import ADCDifferentialPi from python system path")


def main(): # Start of the main program
    print("Fly-by-Pi Load Control Demonstration")
	time.sleep(1)
	print("Setting system variables")
    ###### USER VARIABLES ######
    calibrationFactor = 100 # calibration factor (kg/V)
    targetLoad  = 70 # target load (kg); THE LOAD IS ZEROED AT THE START OF THE SCRIPT
    minimumLoad = 2  # load (kg) where the motor should reverse directions / accepted as the contact load
    holdTime    = 10 # number of seconds that the motor is turned off when either targetLoad or minimumLoad is reached
    startSpeed  = 9  # good starting PWM% is 5% for the cyclic pull-out test (at 1G); use 7% for 30G to overcome static friction
    # For 25kg and 30kg set the starting speed to 7% (@30G)
    # For 50kg set starting speed at 7%
    # For 60kg set starting speed at 9%
    # For 70kg set starting speed at 10%

    ###### SYSTEM VARIABLES ##### DO NOT MODIFY
    cRead = 0 # ADC read counter
    cFail = 0 # ADC read fail counter
	zeroLoad = 0 # The zero/bias load that is subtracted from the reading
    cycleCount = 1 # load cycle counter
    tStart = time.time() # script start time
	direction = 1 # starting direction should be to push forward; 1=forward and 0=backward
    readingLoad = 0 # current load on the load cell (kg); init variable
    currentSpeed = startSpeed # Set the current speed (that can be altered by the gain function) equal to user set start speed
	### Gain control variables
    tPrior = time.time() # prior time
    bReadPrior = True    # sets the flag when we need to update the prior loading variables
    loadPrior = 0 # the previous load from some time in the past
    ### MCP3424 ADC
    print("Creating ADC instance...")
    adc = ADCDifferentialPi(0x68, 12) # Initialzie the ADC object
    adc.set_pga(1)  # PGA gain selection: 1 = 1x +-2.048V
    adc.set_bit_rate(14)  # Set the bit-rate: 14 bit (60SPS max)
    # Motor controller
    print("Create motor controller instance...")
    motor = md()  # Pins should be 27=DIR, 18=PWM, 22=SLP

	print("Initiating control sequence")
    print("Retract the motor")
    motor.setBackward()
    motor.setSpeed(startSpeed)
    motor.setEnable(enabled=1)
    time.sleep(0.5)
    for i in range(4):
        print("Retracting" + ".."*(i+1))
        time.sleep(1)
    motor.setSpeed(startSpeed)
    motor.setEnable(enabled=0)
    time.sleep(1)

    # Calculate the zero/bias load; subtract from all readings
    print("Calculate the zero load on the load cell")
    cRead = 0
    zeroLoad = 0
    for kk in range(100): # take the average of 100 readings
        try:
            time.sleep(0.010)
            reading = adc.read_voltage(1)
            readingLoad = reading * calibrationFactor
            cRead += 1
            zeroLoad += readingLoad 
        except:
            time.sleep(0.005)
            cFail += 1
    zeroLoad /= cRead # True zero load as measured in-flight
    print("Zero load = " + str(round(zeroLoad,3)) + " [kg]")
    
	print("Enter main control loop for load control")
    time.sleep(1)
    readingLoad = 0  # reset the reading
	
    while True: # start the main loop that continues indefinitely
		# First record a new, calibrated reading and then execute/apply the logic control
        cRead += 1  # take a new reading
        # try reading read from adc channels and print data to screen periodically
        try:
            time.sleep(0.001) # Bus stabilization
            reading = adc.read_voltage(1) # read channel 1's Voltage
            readingLoad = reading * calibrationFactor - zeroLoad # Zeroed, calibrated reading in kg
            time.sleep(0.001) # Bus stabilization
            if bReadPrior: # If we need to update the gain variables
                loadPrior = readingLoad
                bReadPrior = False
        except:
            cFail += 1
            time.sleep(0.005)  # sleep 10 ms in event of bus error

        # Logic control
        statusMotor = "404"
        if ((direction == 1) and (readingLoad < targetLoad)):
            motor.setForward()
            motor.setEnable(enabled=1)
            statusMotor = "Go forward. Target load (max) not reached"
            # Update the gain in power is the threshold is exceeded
            if ((tPrior + 2) < time.time()): # check if we need to add power every 2 seconds
                tPrior = time.time() # update time flag
                # Only allow gain if:
 				#   the gradient is small
				#   actuator contact is established
				#   current load is far enough away from the target load
                if  (((readingLoad - loadPrior) < 1) and (readingLoad > minimumLoad) and (readingLoad < targetLoad - 5)):
                    if readingLoad < 50:  # smaller than 50 kg
                        currentSpeed += 1
                        statusMotor += "; 1% GAIN added"
                    else:  # larger than 50 kg; require greater increments
                        currentSpeed += 2
                        statusMotor += "; 2% GAIN added"
                    motor.setSpeed(currentSpeed)
                    bReadPrior = True  # update the prior load variable during next read cycle
                else:
                    print("Cannot add power gain right now")
        elif ((direction == 1) and (readingLoad > targetLoad)): # reached the target load
            motor.setEnable(enabled=0) # stop the motor
            time.sleep(0.010)
            print("Stop going forward. Target load (max) reached")
            print("Motor speed % = " + str(currentSpeed))
            time.sleep(holdTime)  # wait for a certain period of time
            statusMotor = "Set motor backward"
            print(statusMotor)
            direction = 0  # set working direction to retract the actuator
            motor.setBackward()  # set the motor direction to retract/reverse
            motor.setSpeed(startSpeed)  # set the retract speed the same as the start speed
            currentSpeed = startSpeed
            motor.setEnable(enabled=1) # Enable power to the motor
        elif ((direction == 0) and (readingLoad > minimumLoad)): # continue retracting the motor
            motorStatus = "Go backward. Target load (min) not reached"
            motor.setEnable(enabled=1)
            motor.setBackward()
        elif ((direction == 0) and (readingLoad <= minimumLoad)):  # reached minimum of the unload curve
            motor.setEnable(enabled=0) # Turn off the motor
            print("Stop going backward. Target load (min) reached")
            time.sleep(holdTime)  # wait a certain period of time
            statusMotor = "Set motor forward"
            print(statusMotor)
			# Reset the neccesary control variables for the next load curve
            direction = 1 # set the actuator direction to go forward
            motor.setSpeed(startSpeed) # reset the speed of the motor controller
            currentSpeed = startSpeed  # reset the variable that controls the current motor speed
            loadPrior = readingLoad    # set the loadPrior to the latest load reading
            tPrior = time.time() + 2   # ensures that the gain will not take place for another few seconds
            motor.setForward()         # set the motor direction to go forward
            motor.setEnable(enabled=1) # enable power for the motor
            cycleCount += 1 # number of load cycles the program has run
        else:
            print("Warning! Invalid control logic!")


        if ((cRead % 10) == 0): # Only print new data to screen periodically
            os.system('clear')  # clear the console
            print("Time                    : " + str(round(time.time() - tStart, 1)) + " sec")
            print("Feedback frequency      : " + str(int(1/((time.time() - tStart) / cRead))) + " Hz")
            print("Total readings          : " + str(cRead))
            print("Cyclic count            : " + str(cycleCount))
            print("Failed readings (%)     : " + str(round(((cFail/cRead)*100),1)))
            print("Load cell [kg]          : " + str(round(readingLoad,3)))
            print("Current motor speed [%] : " + str(currentSpeed))
            print("Motor status            : " + statusMotor)
            print("Load gradient [kg/s]    : " + str(round((readingLoad - loadPrior)/2, 3)))


if __name__ == "__main__":
    main()
