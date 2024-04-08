"""Myself"""
import hid
from PI26.pi26Driver import *
# from pi26_driver import * # Yifei
if __name__ == '__main__':
    hidBridge = hid.device()
    hidBridge.open(0x1a86, 0xfe07)
    hidBridge.set_nonblocking(1)

    """reset pi26"""
    pi26_reset(hidBridge)

    """turn on internal vref"""
    pi26_vref_config(hidBridge,1)


    """write 0x56 to the GPIO write data register"""
    pi26_spi_write(hidBridge, 0x4856)  # write 0x56 to the GPIO write data register
    pi26_register_read(hidBridge, GPIO_Write_Data, 1)

    """Configure All GPIO to DAC output"""
    pi26_dac_pin_config(hidBridge,0XFF)

    """set DAC0 out 0XFFF"""
    pi26_dac_write(hidBridge,0,0XFFF) # Measure GPIO 0  should be 2.5V

    """set DAC1 out 0XFFF"""
    pi26_dac_write(hidBridge,1,0XFFF) # Measure GPIO 1  should be 2.5V





