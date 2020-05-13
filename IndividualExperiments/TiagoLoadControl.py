#!/usr/bin/env python
"""
================================================
ABElectronics ADC Differential Pi 8-Channel ADC demo
Requires python smbus to be installed
run with: python demo_readvoltage.py
================================================
Initialise the ADC device using the default addresses and sample rate,
change this value if you have changed the address selection jumpers
Sample rate can be 12,14, 16 or 18
https://github.com/abelectronicsuk/ABElectronics_Python_Libraries
Modified by Andre Broekman 2019-09-18
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time, os
from mMotorDriver import cMotorDriver as md

try:
    from mMCP3424 import ADCDifferentialPi
except ImportError:
    print("Failed to import ADCDifferentialPi from python system path")
    print("Importing from parent folder instead")
    try:
        from mMCP3424 import ADCDifferentialPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main(): # Start of the main program
    print("Raspberry Pi load control for Wind Africa centrifuge testing")
    print("Andre Broekman and Tiago Gaspar")
    ###### USER VARIABLES ######
    calibrationFactor = 100 # calibration factor for Converting Volts to kg
    targetLoad = 70 # target load (kg); THE LOAD IS ZEROED AT THE START OF THE SCRIPT
    minimumLoad = 2 # load (kg) where the motor should reverse directions / accepted as the contact load
    holdTime = 10 # number of seconds that the motor is turned off when either targetLoad or minimumLoad is reached
    startSpeed = 9 # good starting PWM% is 5% for the cyclic pull-out test (at 1G); use 7% for 30G to overcome static friction
    # For 25kg and 30kg set the starting speed to 7% (@30G)
    # For 50kg set starting speed at 7%
    # For 60kg set starting speed at 9%
    # For 70kg set starting speed at 10%

    ###### SYSTEM VARIABLES ##### DO NOT MODIFY
    cRead = 0 # number of times data has been successfully read from the ADC
    cFail = 0 # number of times that reading from the ADC has failed
    cycleCount = 1 # how many load cycle the actuator has done
    tStart = time.time() # Start time of the program in Unix seconds
    tPrior = time.time() # Used for gain control
    bReadPrior = True # Gain control; sets the flag when we need to update the prior loading variables
    loadPrior = 0 # Gain control; the previous load from some time in the past
    direction = 1 # starting direction should be to push forward; 1=forward and 0=backward
    readingLoad = 0 # current load on the load cell (kg); init variable
    currentSpeed = startSpeed # Set the current speed (that can be altered by the gain function) equal to user set start speed
    # MCP3424 ADC
    print("Create ADC instance...")
    adc = ADCDifferentialPi(0x68, 12) # Initialzie the ADC object
    adc.set_pga(1)  # Set the PGA; PGA gain selection: 1 = 1x +-2.048V | 2 = 2x +-1.024V | 4 = 4x +-0.512V | 8 = 8x +-0.256V
    adc.set_bit_rate(14)  # Set the bit-rate: 12 = 12 bit (240SPS max) | 14 = 14 bit (60SPS max) | 16 = 16 bit (15SPS max) | 18 = 18 bit (3.75SPS max)
    zeroLoad = 0 # The zero load that is subtracted fromthe reading
    # Motor controller
    print("Create motor controller instance...")
    motor = md()  # Pins should be 27=DIR, 18=PWM, 22=SLP




    # Retract the motor for a few seconds
    print("Retract the motor")
    motor.setBackward()
    motor.setSpeed(10)
    motor.setEnable(enabled=1)
    time.sleep(0.5)
    for i in range(4):
        print("Retracting" + ".."*(i+1))
        time.sleep(1)
    motor.setSpeed(startSpeed)
    motor.setEnable(enabled=0)
    time.sleep(1)

    # Calculate the zero load
    print("Calculate the zero load on the load cell")
    cRead = 0
    zeroLoad = 0
    for kk in range(100):
        try:
            time.sleep(0.001)
            reading = adc.read_voltage(1)
            readingLoad = reading * calibrationFactor
            cRead += 1
            zeroLoad += readingLoad 
        except:
            time.sleep(0.005)
            cFail += 1
    zeroLoad /= cRead # This is now the zero load in kg averaged over 100 readings
    print("Zero load = " + str(round(zeroLoad,3)) + " kg")
    print("Enter main loop for actuator control")
    time.sleep(1)


    readingLoad = 0
    while True: # Enter the main loop
        cRead += 1
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
            if ((tPrior + 2) < time.time()): # Check if we need to add power every second
                tPrior = time.time()
                # Only allow gain if gradient is small, a load is already applied and we are further away than 5 kg from the target load
                if  ( ((readingLoad - loadPrior) < 1) and (readingLoad > 5) and (readingLoad < targetLoad - 5) ):
                    if readingLoad < 50:
                        currentSpeed += 1
                        statusMotor += "; 1% GAIN added"
                    else:
                        currentSpeed += 2
                        statusMotor += "; 2% GAIN added"
                    motor.setSpeed(currentSpeed)
                    bReadPrior = True
                else:
                    print("Dont add any power gain")
        elif ((direction == 1) and (readingLoad > targetLoad)):
            motor.setEnable(enabled=0) # Stop the motor
            time.sleep(0.001)
            print("Stop going forward. Target load (max) reached")
            print("Motor speed % = " + str(currentSpeed))
            time.sleep(holdTime)
            statusMotor = "Set motor backward"
            print(statusMotor)
            direction = 0 # Change the direction to go backward
            motor.setBackward() # Set the motor direction to retract/revers
            motor.setSpeed(startSpeed) # Set the retract speed the same as the start speed
            currentSpeed = startSpeed
            motor.setEnable(enabled=1) # Enable power to the motor
        elif ((direction == 0) and (readingLoad > minimumLoad)):
            motorStatus = "Go backward. Target load (min) not reached"
            motor.setEnable(enabled=1)
            motor.setBackward()
        elif ((direction == 0) and (readingLoad <= minimumLoad)):
            motor.setEnable(enabled=0) # Turn off the motor
            print("Stop going backward. Target load (min) reached")
            time.sleep(holdTime)
            statusMotor = "Set motor forward"
            print(statusMotor)
            direction = 1 # Set the motor direction to go forward
            motor.setSpeed(startSpeed) # Reset the speed of the motor controller
            currentSpeed = startSpeed # Reset the variable that controls the current motor speed
            loadPrior = readingLoad # Set the loadPrior to the latest load reading
            tPrior = time.time() + 2 # Ensures that the gain will not take place for another few seconds
            motor.setForward() # Set the motor direction to go forward
            motor.setEnable(enabled=1) # Enable power for the motor
            cycleCount += 1 # Number of load cycles the program has run
        else:
            print("Invalid control logic!!!!")


        if ((cRead % 3) == 0): # Only print new data to screen periodically
            os.system('clear')  # clear the console
            print("Time                    : " + str(round(time.time() - tStart, 1)) + " sec")
            print("Feedback frequency      : " + str(int(1/((time.time() - tStart) / cRead))) + " Hz")
            print("Total readings          : " + str(cRead))
            print("Cyclic count            : " + str(cycleCount) )
            print("Failed readings (%)     : " + str( round( ((cFail/cRead)*100),1) ) )
            print("Load cell [kg]          : " + str(round(readingLoad,3) ))
            print("Current motor speed [%] : " + str(currentSpeed))
            print("Motor status            : " + statusMotor)
            print("Load gradient [kg/s]    : " + str( round((readingLoad - loadPrior)/2, 3) ) )


if __name__ == "__main__":
    main()
