#!/usr/bin/env python
"""
Fly-by-Pi Controller
	
Code based on source code provided by:
ABElectronics ADC Differential Pi 8-Channel ADC demo
https://github.com/abelectronicsuk/ABElectronics_Python_Libraries

Initialize and test the ADC continniously to establish prevelance
of read errors due to interference and data corruption.

Run using: sudo python3 StressTestADC.py
Modified by Andre Broekman 2020/05/13
Open Source License: Creative Commons Attribution-ShareAlike
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time, os


try:
    from mMCP3424 import ADCDifferentialPi
except ImportError:
    print("Failed to import ADCDifferentialPi from python system path")
	exit(1)


def main():
    cRead = 0  # total read count
    cFail = 0  # failed read count
    adc = ADCDifferentialPi(0x68, 12) # adc instance

    """
    PGA gain selection 
    1 = 1x = +-2.048 V
    2 = 2x = +-1.024 V
    4 = 4x = +-0.512 V => default experiment setting
    8 = 8x = +-0.256 V
    """
    adc.set_pga(4)  # Set the PGA

    """
    Sample rate and resolution
    12 = 12 bit (240SPS max)
    14 = 14 bit (60SPS max) => default experiment setting
    16 = 16 bit (15SPS max)
    18 = 18 bit (3.75SPS max)
    """
    adc.set_bit_rate(14)  # set the bit-rate to 60 SPS

    tStart = time.time()  # start time of test
    while True:
        cRead += 1  # increment read counter
        try:  # try reading data from adc channels and print data to screen periodically
            reading = adc.read_voltage(1) # read input Voltage on C1
        except:  # broad exception capture for reading corruption
            cFail += 1
            time.sleep(0.005)    # sleep 5 ms in event of bus error
        time.sleep(0.010)        # sleep 10 ms after every reading cycle
        if ((cRead % 100) == 0): # only print new data to screen periodically
            os.system('clear')   # clear the console
            print("Time:    " + str(round(time.time() - tStart, 1)) + " [sec]")
            print("Freq:    " + str(int(1/((time.time() - tStart) / cRead))) + " [Hz]")
            print("Count:   " + str(cRead))
            print("Fail:    " + str(cFail))
            print("Fail(%): " + str(round(((cFail/cRead)*100), 2)))
            print("C1: %04f [V]" % reading)


if __name__ == "__main__":
    main()
