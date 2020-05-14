# Fly-By-Pi Controller for Geotechnical Centrifuges :bird:
Fly-by-Pi: Raspberry Pi closed-loop linear actuator controller for geotechnical centrifuges
Python implementation for controlling a linear actuator using a motor controller and ADC for closed-loop feedback and control.
Demo files of both time- and load-based control is included. The class files for the motor driver and ADC (MCP3424) and motor controller (Pololu 24v13) should be replaced/amended as neccesary repending on the particular type of hardware that is implemented.

## Scripts
- StressTestADC.py - stress test the ADC to determine the performance and reliability with simple metrics
- TimeControl.py - demonstration code of time-based control for a motor/actuator
- LoadControl.py - demonstration code of load-based control for a motor/actuator

To run any of the scripts, first change to the active directory to where the files are stored, followed by the excecuting the script:
```
cd /home/pi/Desktop/FlyByPi
sudo python3 TimeControl.py
```

## Class files
mMCP3424.py - ADC class file
mMotorDriver.py - Pololu 24v3 motor driver class file

## Individual Experiments
Archived implementation scripts. Ensure that these scripts are copied to the same directory as that of the class files if they are to be used.  Otherwise, create a copy of one for the template scripts that provide a default framework.

## UDPdemo
A small utility to test communication using the UDP protocol. A script for both a sever and client is provided.

## Author
Fly-By-Pi repository is maintained by Andre Broekman in conjunction with the Department of Civil Engineering, University of Pretoria, South Africa
Feel free to get in touch via [LinkedIn](https://www.linkedin.com/in/broekmanandre/) or [Twitter](https://twitter.com/BroekmanAndre)
