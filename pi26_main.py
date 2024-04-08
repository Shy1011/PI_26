# -*- coding: utf-8 -*-
# @Time    : 2024/3/26 16:10
# @Author  : yifei.su
# @File    : pi26_main.py

import hid
from pi26_driver import *

DAC_ADC_MODE = 0x00
GPIO_MODE = 0x01

PI26_MODE = GPIO_MODE


if __name__ == '__main__':
    hidBridge = hid.device()
    hidBridge.open(0x1a86, 0xfe07)
    hidBridge.set_nonblocking(1)

    """ reset pi26 """
    pi26_reset(hidBridge)

    """ enable internal vref """
    pi26_vref_config(hidBridge, 1)

    """ pi26 spi write & read test """
    pi26_spi_write(hidBridge, 0x4856)     # write 0x56 to the GPIO write data register
    print(f"spi write data is:", pi26_spi_read(hidBridge, 0x3864))  # enable readback and read GPIO data register
                                                                    # should return above step data, like 0x56

    if PI26_MODE == DAC_ADC_MODE:
        """ pi26 dac write & readback operation """
        pi26_dac_write(hidBridge, 0xFF, 0x0, 0xF00)     # configure all gpio as DAC output and DAC0 data is 0x200
        pi26_dac_write(hidBridge, 0xFF, 0x1, 0x400)     # configure all gpio as DAC output and DAC1 data is 0x400
        pi26_dac_write(hidBridge, 0xFF, 0x2, 0x600)     # configure all gpio as DAC output and DAC2 data is 0x600
        pi26_dac_write(hidBridge, 0xFF, 0x3, 0x800)     # configure all gpio as DAC output and DAC3 data is 0x800
        pi26_dac_write(hidBridge, 0xFF, 0x4, 0xa00)     # configure all gpio as DAC output and DAC4 data is 0xa00
        pi26_dac_write(hidBridge, 0xFF, 0x5, 0xc00)     # configure all gpio as DAC output and DAC5 data is 0xc00
        pi26_dac_write(hidBridge, 0xFF, 0x6, 0xe00)     # configure all gpio as DAC output and DAC6 data is 0xe00
        pi26_dac_write(hidBridge, 0xFF, 0x7, 0xfff)     # configure all gpio as DAC output and DAC7 data is 0xf00
        print("Measure the Voltage")
        # input()
        adcAddr, adcData = pi26_dac_readback(hidBridge, 0x2)    # read DAC2 data
        print(f"return adc address is:{hex(adcAddr)}, adc data is:{hex(adcData)}")

        """ pi26 dac power down """

        # pi26_power_down_config(hidBridge, 1, 1, 0x00)
        """ pi26 adc operation """
        pi26_adc_config(hidBridge, 0x03, 0x1, 0x1)      # configure gpio0/1 as ADC input and enable repeat/temp
        print(f"adc read data is:", [hex(n) for n in pi26_adc_read(hidBridge, 9)])  # read gpio0/1/temp 3 times
        # pi26_adc_config(hidBridge, 0x03, 0x1, 0x1)      # configure gpio0/1 as ADC input and enable repeat/temp
        print(f"adc read data is:", [hex(n) for n in pi26_adc_read(hidBridge, 9)])  # read gpio0/1/temp 3 times

    elif PI26_MODE == GPIO_MODE:
        ''' short gpio0 to gpio4,  gpio1 to gpio5, gpio2 to gpio6, gpio3 to gpio7
                    execute below code will print gpio output configure data.
                    like gpio output configure 0x03, will print 0x33'''

        """ pi26 gpio output configure """
        pi26_gpio_output_config(hidBridge, 0, 0xFF)     # set gpio0~3 as output mode
        pi26_gpio_write_data(hidBridge, 0xff)           # gpio0~4 output data is 0xA

        """ pi26 gpio input configure """
        print(f"read gpio input data is:{hex(pi26_gpio_read(hidBridge, 1, 0xFF))}")  # set gpio4~7 as input mode
                                                                                     # and read gpio input data

        """ pi26 gpio three-state configure """
        # pi26_three_state_config(hidBridge, 0x0F)           # set gpio0~3 as 3-state mode
        #
        # """ pi26 gpio pull-down configure """
        # pi26_gpio_pulldw_config(hidBridge, 0x0F)            # set gpio0~3 as pull down






