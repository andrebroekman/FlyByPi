# Fly-By-Pi Controller for geotechnical centrifuges :bird:
Fly-by-Pi: Raspberry Pi closed-loop linear actuator controller for geotechnical centrifuges
Python implementation for controlling a linear actuator using a motor controller and ADC for closed-loop feedback and control.
Demo files of both time- and load-based control is included. The class files for the motor driver and ADC (MCP3424) and motor controller (Pololu 24v13) should be replaced/amended as neccesary repending on the particular type of hardware that is implemented.

## Scripts
StressTestADC.py - stress test the ADC to determine the performance and reliability with simple metrics
TimeControl - demonstration code of time-based control for a motor/actuator
LoadControl - demonstration code of load-based control for a motor/actuator

## Class files
mMCP3424.py - ADC class file
mMotorDriver.py - Pololu 24v3 motor driver class file

## Individual Experiments
Existing implementation scripts. Ensure that these scripts are copied to the same directory as that of the class files.

## UDPdemo
A small utility to test communication using the UDP protocol. A script for both a sever and client is provided.






