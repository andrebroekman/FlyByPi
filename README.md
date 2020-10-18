# Fly-By-Pi Controller for Geotechnical Centrifuges :bird:
[Fly-by-Pi: Open source closed-loop control for geotechnical centrifuge testing applications. The full article published in the HardwareX open access journal can be found using the DOI link: https://doi.org/10.1016/j.ohx.2020.e00151](https://doi.org/10.1016/j.ohx.2020.e00151)


![Image of a geotechnical centrifuge](https://github.com/andrebroekman/FlyByPi/blob/master/centrifuge.png)

A simple Python implementation for closed-loop control of linear actuators and/or motors, developed specifically for the Raspberry Pi platform. Primarily developed for geotechnical centrifuge applications at the Department of Civil Engineering, University of Pretoria.

Demo files of both time- and load-based control is included. The class files for the motor driver and ADC (MCP3424) and motor controller (Pololu 24v13) should be replaced/amended as neccesary repending on the particular type of hardware that is implemented.

## Getting Started
Either download or git clone this repository to the desired directory on the Raspberry Pi:
```
cd /home/pi/Desktop
git clone https://github.com/andrebroekman/FlyByPi
```


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
* mMCP3424.py -  class file
* mMotorDriver.py - [Pololu 24v3 motor driver](https://www.pololu.com/product/2992) class file


## Individual Experiments
Archived implementation scripts. Ensure that these scripts are copied to the same directory as that of the class files if they are to be used.  Otherwise, create a copy of one for the template scripts that provide a default framework.


## UDP Demonstration
A small test utility to demonstration communication using the UDP protocol. A script for both a sever and client is provided. Tested successfully to send packets between a Raspberry Pi in the centrifuge and a computer in the control room.


## Author
Fly-By-Pi repository is maintained by Andre Broekman in conjunction with the [Department of Civil Engineering, University of Pretoria](https://www.up.ac.za/civil-engineering), South Africa. Feel free to get in touch via [LinkedIn](https://www.linkedin.com/in/broekmanandre/), [ResearchGate](https://www.researchgate.net/profile/Andre_Broekman) or [Twitter](https://twitter.com/BroekmanAndre). For more information regarding the [geotechnical centrifuge](https://www.up.ac.za/civil-engineering/article/1914311/geotechnical-centrifuge-laboratory) located at the University of Pretoria, please contact [Prof. SW Jacobsz](https://www.up.ac.za/civil-engineering/article/49328/staff)

