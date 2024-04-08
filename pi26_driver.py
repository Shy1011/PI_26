# -*- coding: utf-8 -*-
# @Time    : 2024/3/26 11:21
# @Author  : yifei.su
# @File    : pi26_driver.py

from hid_driver import *

def pi26_spi_write(pHidBridge, pPara):
    """
    pi26 spi write operation only send 16bit parameter
    :param pHidBridge: hid bridge object
    :param pPara: 16bit parameter like 0x1234
    :return:
    """
    paraList = [(pPara >> 8) & 0x00FF, pPara & 0x00FF]
    ch32_spi_full_duplex(pHidBridge, paraList, 2)


def pi26_spi_read(pHidBridge, pPara):
    """
    pi26 spi read operation
        step1 - send read register
        step2 - send NOP(0x0000) to read back data
    :param pHidBridge: hid bridge object
    :param pPara: read register address
    :return: returned data
    """
    paraList = [(pPara >> 8) & 0x00FF, pPara & 0x00FF]
    # 0011 1000 0110 0100
    ch32_spi_full_duplex(pHidBridge, paraList, 2)

    rtData = ch32_spi_full_duplex(pHidBridge, [0x00, 0x00], 2)
    return hex((rtData[0] << 8) | rtData[1])

def pi26_register_read(pHidBridge, regsel,readbacken):
    """
    pi26 spi read operation
        step1 - send read register
        step2 - send NOP(0x0000) to read back data
    :param pHidBridge: hid bridge object
    :param pPara: read register address
    :param pPara: readback enable 0 / 1
    :return: returned data
    """
    ch32_spi_full_duplex(pHidBridge, [0x38,(0x00|(readbacken<<6)|(regsel<<2))], 2)

    rtData = ch32_spi_full_duplex(pHidBridge, [0x00, 0x00], 2)
    print(f" register {bin(regsel)} 's data is {hex((rtData[0] << 8) | rtData[1])}")
    return hex((rtData[0] << 8) | rtData[1])



def pi26_general_control_config(pHidBridge, pAdcPreChg, pAdcBufEn, pLock, pAllDac, pAdcRg, pDacRg):
    """
    pi26 general purpose control configuration
    :param pHidBridge: hid bridge object
    :param pAdcPreChg: ADC buffer precharge enable
    :param pAdcBufEn: ADC buffer enable
    :param pLock: I/Ox pin configuration
    :param pAllDac: enable write all DACs
    :param pAdcRg: set ADC gain
                   0 - Vref
                   1 - 2 * Vref
    :param pDacRg: set DAC gain
                   0 - Vref
                   1 - 2 * Vref
    :return: none

    """
    msb = 0x18 | (pAdcPreChg << 1) | pAdcBufEn
    lsb = (pLock << 7) | (pAllDac << 6) | (pAdcRg << 5) | (pDacRg << 4)
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)

def pi24_osc_freq(pHidBridge):
    # 0e 01
    ch32_spi_full_duplex(pHidBridge, [0x0e, 0x01], 2)
    ch32_spi_full_duplex(pHidBridge, [0xa0, 0xc0], 2)
    ch32_spi_full_duplex(pHidBridge, [0xa1, 0xde], 2)
    ch32_spi_full_duplex(pHidBridge, [0xa2, 0x40], 2)


def pi26_reset(pHidBridge):
    """
    reset pi26
    :param pHidBridge: hid bridge object
    :return:
    """
    ch32_spi_full_duplex(pHidBridge, [0x7D, 0xAC], 2)


def pi26_readback_ldac_mode(pHidBridge, pEnable, pRegReadBack, pLdacMode):
    """
    pi26 readback ladc mode operation
    :param pHidBridge: hid bridge object
    :param pEnable: enbalbe readback. 1 bit, like 0x1
                    0 - no readback is initiated
                    1 - enable pRegReadBack selected register
    :param pRegReadBack: readback register. 4 bit, like 0xF
    :param pLdacMode: ldac mode. 2 bit, like 0x2
                      00 - auto update
                      01 - stop update
                      10 - enable update (work with 01 together)
                      11 - reserved
    :return:
    """
    msb = 0x38      # register address is 0b0111
    lsb = (pEnable << 6) | (pRegReadBack << 2) | pLdacMode  # include EN,REG_READBACK & LDAC mode
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)


def pi26_dac_write(pHidBridge, pDacPin, pDacAddr, pData):
    """
    configure selected gpio work as dac mode and set dac data
    :param pHidBridge: hid bridge object
    :param pDacPin: selected gpio pin. one byte, like 0x05
                   each bit represent selected channel
                   bitx = 0 - no selected
                   bitx = 1 - selected
    :param pDacAddr: dac address (only 3bits, like 0x7)
    :param pData: dac data (12 bit, like 0x8A5)
    :return:
    """
    ch32_spi_full_duplex(pHidBridge, [0x28, pDacPin], 2)
#0010 1000
    msb = ((0x8 | pDacAddr) << 4) | ((pData & 0xF00) >> 8)
    lsb = pData & 0xFF
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)


# 返回的是什么?
def pi26_dac_readback(pHidBridge, pDacCh):
    """
    read pi26 dac data register
    :param pHidBridge: hid bridge object
    :param pDacCh: read dac channel number (only 3 bits, like 0x7)
    :return: return 2 value
             1 - dac address (3bit, like 0x7)
             2 - dac channel data (12 bits, like 0x800)
    """
    ch32_spi_full_duplex(pHidBridge, [0x08, (0x18 | pDacCh)], 2)

    rtData = ch32_spi_full_duplex(pHidBridge, [0x00, 0x00], 2)
    rtDdcAddr = (rtData[0] & 0x70) >> 4
    rtDacData = ((rtData[0] & 0x0F) << 8) | rtData[1]
    return rtDdcAddr, rtDacData


def pi26_adc_config(pHidBridge, pAdcCh, pReptEn, pTemEn):
    """
    configure selected pin work as ADC mode
    :param pHidBridge: hid bridge object
    :param pAdcCh: selected adc channel. one byte, like 0x05
                   each bit represent selected channel
                   bitx = 0 - no selected
                   bitx = 1 - selected
    :param pReptEn: repeat sequence enable
                    0 - disable
                    1 - enable
    :param pTemEn: include temp in sequence
                    0 - include
                    1 - don't include
    :return:
    """
    """ adc pin configuration """
    ch32_spi_full_duplex(pHidBridge, [0x20, pAdcCh], 2)

    """ adc sequence configuration """
    msb = 0x10 | (pReptEn << 1) | pTemEn
    ch32_spi_full_duplex(pHidBridge, [msb, pAdcCh], 2)


def pi26_adc_read(pHidBridge, pNum):
    """
    execute adc read operation
    :param pHidBridge: hid bridge object
    :param pNum: read number
    :return: read data. list format, like [data0, data1, data2]
             list element number is equal to pNum
    """
    """ first nop get invalid data """
    ch32_spi_full_duplex(pHidBridge, [0x00, 0x00], 2)

    """ read valid data """
    dataList = []
    for cnt in range(pNum):
        temData = ch32_spi_full_duplex(pHidBridge, [0x00, 0x00], 2)
        dataList.append(((temData[0] << 8) | temData[1]) & 0x0FFF)

    return dataList

def pi26_adc_read_single(pHidBridge, pNum):
    """
    execute adc read operation
    :param pHidBridge: hid bridge object
    :param pNum: read number
    :return: read data. list format, like [data0, data1, data2]
             list element number is equal to pNum
    """
    """ first nop get invalid data """
    ch32_spi_full_duplex(pHidBridge, [0x00, 0x00], 2)

    """ read valid data """
    dataList = []
    for cnt in range(pNum):
        temData = ch32_spi_full_duplex(pHidBridge, [0x00, 0x00], 2)
        dataList.append(((temData[0] << 8) | temData[1]) & 0x0FFF)

    return dataList


def pi26_gpio_output_config(pHidBridge, pBusy, pPin):
    """
    set selected pin work as gpio output mode
    :param pHidBridge: hid bridge object
    :param pBusy: enable the I/O 7 pins as busy
                  0 - disable
                  1 - enable
    :param pPin: selected pin. one byte, like 0x05
                   each bit represent selected pin
                   bitx = 0 - no selected
                   bitx = 1 - selected
    :return:
    """
    msb = 0x40 | pBusy
    ch32_spi_full_duplex(pHidBridge, [msb, pPin], 2)


def pi26_gpio_op_config(pHidBridge, pPin):
    """
    set selected pin work as open-drain mode, pPin selected pin will work as open-drain mode
    note: before invoke this function should invoke pi26_gpio_output_config first
    :param pHidBridge: hid bridge object
    :param pPin:  selected pin. one byte, like 0x05
                   each bit represent selected pin
                   bitx = 0 - no selected
                   bitx = 1 - selected
    :return:
    """
    ch32_spi_full_duplex(pHidBridge, [0x60, pPin], 2)


def pi26_gpio_write_data(pHidBridge, pData):
    """
    configure gpio output data
    :param pHidBridge: hid bridge object
    :param pData: gpio output data. one byte, like 0x05
                  each bit corresponding pin
                  bitx = 0 - output low
                  bitx = 1 - output high
    :return:
    """
    ch32_spi_full_duplex(pHidBridge, [0x48, pData], 2)


def pi26_gpio_read_config(pHidBridge, pEn, pPin):
    """
    configure selected pin work as gpio input mode
    :param pHidBridge: hid bridge object
    :param pEn: enable gpio readback
    :param pPin: selected pin. one byte, like 0x05
                 each bit represent selected pin
                 bitx = 0 - no selected
                 bitx = 1 - selected
    :return:
    """
    msb = 0x50 | (pEn << 2)
    ch32_spi_full_duplex(pHidBridge, [msb, pPin], 2)


def pi26_gpio_read(pHidBridge, pEn, pPin):
    """
    read gpio input data
    :param pHidBridge: hid bridge object
    :param pEn: enable gpio readback
    :param pPin: selected pin work as gpio input mode. one byte, like 0x05
                 each bit represent selected pin
                 bitx = 0 - no selected
                 bitx = 1 - selected
    :return: gpio input data. one byte, like 0xA5.
             each bit represent corresponding gpio
    """
    """ configure selected gpio work as input mode """
    pi26_gpio_read_config(pHidBridge, pEn, pPin)

    """ send NOP to read gpio data """
    tem = ch32_spi_full_duplex(pHidBridge, [0x00, 0x00], 2)   # 为什么是一个16位的值?
    return (tem[0] << 8) | tem[1]

def pi26_osc_fre(pHidBridge):
    """
    GPIO0 output OSC frequency
    :param pHidBridge:
    :return:
    """
    pi26_spi_write(pHidBridge, 0x7001)
    pi26_spi_write(pHidBridge, 0xA0C0)
    pi26_spi_write(pHidBridge, 0xA1DE)
    pi26_spi_write(pHidBridge, 0xA240) #?    pi26_spi_write(hidBridge, 0x7001)
    pi26_spi_write(pHidBridge, 0xA0C0)
    pi26_spi_write(pHidBridge, 0xA1DE)
    pi26_spi_write(pHidBridge, 0xA240) #?

def pi26_osc_fre_off(pHidBridge):
    """
    GPIO0 does not output OSC frequency
    :param pHidBridge:
    :return:
    """
    pi26_spi_write(pHidBridge, 0xA200)


def pi26_three_state_config(pHidBridge, pPin):
    """
    set selected pin work as three state
    :param pHidBridge: hid bridge object
    :param pPin: selected pin. one byte, like 0x05
                 each bit represent selected pin
                 bitx = 0 - no selected
                 bitx = 1 - selected
    :return:
    """
    ch32_spi_full_duplex(pHidBridge, [0x68, pPin], 2)


def pi26_gpio_pulldw_config(pHidBridge, pPin):
    """
    set selected pin work as pull down mode
    :param pHidBridge: hid bridge object
    :param pPin: selected pin. one byte, like 0x05
                 each bit represent selected pin
                 bitx = 0 - no selected
                 bitx = 1 - selected
    :return:
    """
    ch32_spi_full_duplex(pHidBridge, [0x30, pPin], 2)


def pi26_power_down_config(pHidBridge, pPdAll, pEnRef, pPin):
    """
    configure power mode
    :param pHidBridge: hid bridge object
    :param pPdAll: all DACs, ADC, reference power down enable
                   0 - disable
                   1 - enable
    :param pEnRef: enable internal reference
                   0 - external vref
                   1 - internal vref
    :param pPin: selected pin will be power down. one byte, like 0x05
                 each bit represent selected pin
                 bitx = 0 - no selected
                 bitx = 1 - selected
    :return:
    """
    msb = 0x58 | (pPdAll << 2) | (pEnRef << 1)
    ch32_spi_full_duplex(pHidBridge, [msb, pPin], 2)
    # pi26_power_down_config(hidBridge, 0, 1, 0xFF) # turn on internal power supply
    # pi26_power_down_config(hidBridge, 0, 0, 0xFF) # turn on external power supply
def pi26_vref_config(pHidBridge, pVref):
    """
    configure pi26 vref source
    :param pHidBridge: hid bridge object
    :param pVref: one bit
                  0 - external vref
                  1 - internal vref (2.5V)
    :return:
    """
    vref = 0x58 | (pVref << 1)
    ch32_spi_full_duplex(pHidBridge, [vref, 0x00], 2)
