# -*- coding: utf-8 -*-
# @Time    : 2024/3/28 13:46
# @Author  : Shy
"""
Arun Test
"""


import hid
from pi26_driver import *

import hid
from pi26_driver import *


def reset_vref_open():
    """ reset pi26 """
    pi26_reset(hidBridge)

    """ enable internal vref """
    pi26_vref_config(hidBridge, 1)

"""
DAC Test
set all GPIO to DAC output
pinNum : 0 1 2 3 4 5 6 7

"""
def dac_test(pinNum):
    print("dac test strats")
    pi26_dac_write(hidBridge, 0xff, pinNum, 0x000) # DAC TEST
    print("Measure the Voltage 000")
    input()
    pi26_dac_write(hidBridge, 0xff, pinNum, 0x800)  # DAC TEST
    print("Measure the Voltage 800")
    input()
    pi26_dac_write(hidBridge, 0xff, pinNum, 0xC00)  # DAC TEST
    print("Measure the Voltage C00")
    input()
    pi26_dac_write(hidBridge, 0xff, pinNum, 0xFFF)  # DAC TEST
    print("Measure the Voltage FFF")
    input()
    print("dac test ends")

"""

GP0 to GP7 all set to be adc input
repeat -> 1 enable 0 disable
temp - > 1 enable 0 disable


results
set voltage to 0V

adc read data is: ['0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x33d']
set voltage to Vref/2

adc read data is: ['0x7cd', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x33e']
set voltage to 3/4Vref

adc read data is: ['0xbbc', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x33e']
"""
def adc_test():
    print("ADC test starts")
    """ reset pi26 """
    # reset_vref_open()
    print("set voltage to 0V")
    input()
    pi26_adc_config(hidBridge, 0xFF, 0x1, 0x1)  # configure gpio0/1 as ADC input and enable repeat/temp
    print(f"adc read data is:", [hex(n) for n in pi26_adc_read(hidBridge, 9)])  # read

    print("set voltage to Vref/2 = 1.25")
    input()
    pi26_adc_config(hidBridge, 0xFF, 0x1, 0x1)  # configure gpio0/1 as ADC input and enable repeat/temp
    print(f"adc read data is:", [hex(n) for n in pi26_adc_read(hidBridge, 9)])  # read

    print("set voltage to 3/4Vref = 1.875")
    input()
    pi26_adc_config(hidBridge, 0xFF, 0x1, 0x1)  # configure gpio0/1 as ADC input and enable repeat/temp
    print(f"adc read data is:", [hex(n) for n in pi26_adc_read(hidBridge, 9)])  # read

    print("set voltage to Vref = 2.5")
    input()
    pi26_adc_config(hidBridge, 0xFF, 0x1, 0x1)  # configure gpio0/1 as ADC input and enable repeat/temp
    print(f"adc read data is:", [hex(n) for n in pi26_adc_read(hidBridge, 9)])  # read

    input()
    print("ADC test ends")


def adc_test_2():
    """
    0x800 +- 20codes

    :return:
    """
    print("ADC test starts")
    pi26_adc_config(hidBridge, 0xFF, 0x1, 0x1)  # configure gpio0/1 as ADC input and enable repeat/temp
    datalist = pi26_adc_read(hidBridge, 9)
    for n in datalist:
        print(hex(0x800 - n))
    print(f"adc read data is:", [hex(n) for n in datalist])  # read
    return datalist[8]



"""
Configure GP0 to GP7 as GPIO output. Set GPO write data and check the output is correct value.
GPIO 0-3 logic 1
GPIO 4-7 logic 0
"""
def gpio_test():
    # reset_vref_open()
    print("gpio_test output starts")
    pi26_gpio_output_config(hidBridge, 0, 0x0f) # set GPIO 0 - 7 output
    pi26_gpio_write_data(hidBridge, 0x0f) # GPIO 0-7 are all logic 1
    input()
    print("gpio_test output ends")

"""
set all gpio to input then readback each gpio's value in binary 
for example : 0b1111 0000

"""
def gpio_test2():
    print("gpio input test start")
    print("all gpio set to input and read the logic value in binary")
    # pi26_gpio_read_config(hidBridge, 0, 0xff)
    #
    reset_vref_open() # Beacause when output and input are set together, the GPIO will be considered as output first. So if u read the GPIO data together,i
    # the readback will be the GPIO output's value. For example : GPIO output is set to 0XFF,then even if no connect to GPIO.The gpio input readback will be 0xff
    print(f"read gpio input data is:{bin(pi26_gpio_read(hidBridge, 1, 0xFF))}")  # set gpio4-7 as input mode and print the data in hex
    print("change the state")
    input()
    print(f"read gpio input data is:{bin(pi26_gpio_read(hidBridge, 1, 0xFF))}")  # set gpio4-7 as input mode and print the data in hex
    input()
    print("gpio input test ends")

"""
soft_reset
phenomenon :  GPIO 0- 3 change from Logic 1 to the original state logic 0
"""
def soft_reset():
    print("reset start")
    gpio_test()
    print("GPIO 0-3 set to output logic 1")
    print("Press to reset")
    input()
    pi26_reset(hidBridge)
    input()
    print("reset end")

def temperature_read():
    print("temperature_read start")
    # reset_vref_open()
    pi26_adc_config(hidBridge, 0x00, 0x1, 0x1)  # configure gpio0/1 as ADC input and enable repeat/temp
    print(f"adc read data is:", [hex(n) for n in pi26_adc_read(hidBridge, 1)])  # read
    input()
    print("temperature_read end")

def spi_read_write_test():
    """ pi26 spi write & read test """
    print("spi_read_write_test start")
    pi26_spi_write(hidBridge, 0x4856)     # write 0x56 to the GPIO write data register

    pi26_register_read(hidBridge, 0x9, 1)# enable readback and read GPIO data register should return above step data, like 0x56

    pi26_register_read(hidBridge, 0x1,1)  # enable readback and read  DAC readback default value

    pi26_register_read(hidBridge, 0x6,1)  # enable readback and read pull down configuration default value
    input()
    print("spi_read_write_test end")


if __name__ == '__main__':
    hidBridge = hid.device()
    hidBridge.open(0x1a86, 0xfe07)
    # hidBridge.set_nonblocking(1)

    """ reset pi26 """
    pi26_reset(hidBridge)

    """ enable internal vref """
    pi26_vref_config(hidBridge, 1)

    """Enable osc frequency output : GPIO0"""
    pi26_osc_fre(hidBridge)
    input()
    pi26_spi_write(hidBridge, 0xA200)

    """should return 0x56 0x00 0xff"""
    spi_read_write_test()

    pi26_reset(hidBridge)
    pi26_vref_config(hidBridge, 1)

    """Set all dacs' value to 0X800"""
    # for i in range (0,8) :
    #     pi26_dac_write(hidBridge, 0xff, i, 0x800)  # set DAC 0 - 7 to 0X800

    """Check the difference between ADCS return value with 0X800"""
    temp = adc_test_2()




    # """set all gpios to output and set set GPIO Write Data Register to 0xff"""
    # pi26_gpio_output_config(hidBridge, 0, 0xff)
    # pi26_gpio_write_data(hidBridge, 0xff)  # GPIO
    # print(hex(pi26_gpio_read(hidBridge, 1, 0xFF)))  # print the logic state of all GPIOs
    #
    # """set all gpios to output and set GPIO Write Data Register to 0x55"""
    # pi26_gpio_write_data(hidBridge, 0x55)  # GPIO 0-7 are all logic 1
    # print(hex(pi26_gpio_read(hidBridge, 1, 0xFF)))  # print the logic state of all GPIOs
    #
    # """set all gpios to output and set GPIO Write Data Register to 0xAA"""
    # pi26_gpio_write_data(hidBridge, 0xAA)
    # print(hex(pi26_gpio_read(hidBridge, 1, 0xFF))) # print the logic state of all GPIOs

    # """caculate the temperature"""
    # print(hex(temp))
    # temperature = 25 + ((temp-(0.5/2.5)*4095)/(2.654*(2.5/2.5)))
    # print(f"temp = {temperature}")


