
from hid_driver import *
import hid
"""
Register Map
"""
NOP                          = 0b0000
DAC_Readback                 = 0b0001
ADC_Sequence_Register        = 0b0010
General_Purpose_Control_Register = 0b0011
ADC_Pin_Configuration        = 0b0100
DAC_Pin_Configuration        = 0b0101
Pull_Down_Configuration      = 0b0110
Readback_and_LDAC_Mode       = 0b0111
GPIO_Write_Configuration     = 0b1000
GPIO_Write_Data              = 0b1001
GPIO_Read_Configuration      = 0b1010
Power_Down_Reference_Control = 0b1011
GPIO_Open_Drain_Configuration = 0b1100
Three_State_Configuration    = 0b1101
Reserved                         = 0b1110
Software_Reset                   = 0b1111
# DAC_Write                    = 0bXXXX

def pi26_reset(pHidBridge):
    """
    reset pi26
    :param pHidBridge: hid bridge object
    :return:
    """
    ch32_spi_full_duplex(pHidBridge, [0x7D, 0xAC], 2)
    # 0111 1101 1010 1100



def pi26_spi_write(pHidBridge, pPara):
    """
    pi26 spi write operation only send 16bit parameter
    :param pHidBridge: hid bridge object
    :param pPara: 16bit parameter like 0x1234
    :return:
    """
    paraList = [(pPara >> 8) & 0x00FF, pPara & 0x00FF]
    ch32_spi_full_duplex(pHidBridge, paraList, 2)

    # pi26_spi_write(hidBridge, pPara)


def pi26_register_read(pHidBridge, regsel,readbacken):
    """
    pi26 spi read operation
        step1 - send read register
        step2 - send NOP(0x0000) to read back data
    :param pHidBridge: hid bridge object
    :param regsel: read register address
    :param readbacken: readback enable 0 / 1
    :return: returned data
    """
    ch32_spi_full_duplex(pHidBridge, [0x38,(0x00|(readbacken<<6)|(regsel<<2))], 2)

    rtData = ch32_spi_full_duplex(pHidBridge, [0x00, 0x00], 2)
    print(f" register {bin(regsel)} 's data is {hex((rtData[0] << 8) | rtData[1])}")
    return hex((rtData[0] << 8) | rtData[1])


def  pi26_pin_con(pHidBridge,fuctionSel,pin):
    """
    reg : I/Ox Pin Configuration Registers
    Configure GPIO's Function : such as 0100 0101 .etc
    :param pHidBridge: hid bridge object
    :param fuctionSel: function selection :
                        0100: ADC pin configuration.
                        0101: DAC pin configuration.
                        0110: pull-down configuration. (Default condition at power-up.)
                        1000: GPIO write configuration.
                        1010: GPIO read configuration.
                        1100: GPIO open-drain configuration.
                        1101: three-state configuration.
    :param pin: which pin to configure
                such as : 0xFF ;0X01 ,etc
    :return:
    """
    msb = fuctionSel << 3
    lsb = pin
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)


def  pi26_general_purpose_control_register(pHidBridge,adcPrecharge,adcBufferEn,lock,allDacs,adcRange,dacRange) :
    """
    General-Purpose Control Register
    :param pHidBridge:
    :param regAddr:
    :param adcPrecharge:
            0: ADC buffer is not used to precharge the ADC. If the ADC buffer is enabled, it is always powered up (default).
            1: ADC buffer is used to precharge the ADC. If the ADC buffer is enabled, it is powered up while the conversion takes place and then powered down until the next conversion takes place.
    :param adcBufferEn:
            0: ADC buffer is disabled (default).
            1: ADC buffer is enabled.
    :param lock:
            0: the contents of the I/Ox pin configuration registers can be changed (default).
            1: the contents of the I/Ox pin configuration registers cannot be changed.
    :param allDacs:
                -----
    :param adcRange:
            0: ADC gain is 0 V to VREF (default).
            1: ADC gain is 0 V to 2 × VREF.
    :param dacRange:
            0: DAC output range is 0 V to VREF (default).
            1: DAC output range is 0 V to 2 × VREF.
    :return:
    """

    msb = (General_Purpose_Control_Register << 3)|(adcPrecharge<<1)|adcBufferEn
    lsb = (lock << 8) | (allDacs << 7) | (adcRange << 6) | (dacRange << 4)

    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)


def pi26_dac_pin_config(pHidBridge,pin):
    """
    DAC Pin Configuration Register
    :param pHidBridge:
    :param pin:
        D7 to D0
        Select I/Ox pins as DAC outputs.
        1: I/Ox is a DAC output.
        0: I/Ox function is determined by the pin configuration registers (default).
    :return:
    """
    msb = (DAC_Pin_Configuration << 3)
    lsb = pin
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)


def pi26_dac_write(pHidBridge,dacPinSel,dacData):
    """
    DAC Write Register
    :param pHidBridge:
    :param dacPinSel:
            Bit D14 to Bit D12 select the DAC register to which the data in D11 to D0 is loaded.
            000: DAC0
            001: DAC1
            010: DAC2
            011: DAC3
            100: DAC4
            101: DAC5
            110: DAC6
            111: DAC7
    :param dacData:
            12-bit DAC data.  ; 0XFFF
    :return:
    """
    msb = (0x1<<7) | (dacPinSel << 4) | ((dacData&0XF00)>>8)
    lsb = (dacData & 0X0FF)
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)

def pi26_dac_readback(pHidBridge,dacReadbackEn,dacChannelSel):
    """
    DAC Readback Register
    :param pHidBridge:
    :param dacReadbackEn:
            Enable readback of the DAC input register.
            11: readback enabled.
            00: readback disabled (default).
    :param dacChannelSel:
            Select DAC channel.
            000: DAC0
            001: DAC1
            …
            110: DAC6
            111: DAC7
    :return:
    """
    msb = (DAC_Readback << 3)
    lsb = (dacReadbackEn << 3) | dacChannelSel

    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)
    result = ch32_spi_full_duplex(pHidBridge, [0x00, 0x00], 2)
    print(f"DAC {'{:03b}'.format((result[0] & 0b01110000)>>4)} data is {hex(((result[0] & 0X0F) << 8) | result[1])}")
    return hex(((result[0] & 0X0F) << 8) | result[1]) # 1010
    # pi26_dac_readback(hidBridge,0b11,0b000)

def pi26_adc_pin_con(pHidBridge,pin):
    """
    ADC Pin Configuration Register

    :param pHidBridge:
    :param pin:
        elect I/Ox pins as ADC inputs.
        1: I/Ox is an ADC input.
        0: I/Ox function is determined by the pin configuration registers (default).
    :return:
    """
    msb = 0x20
    lsb = pin
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)


def pi26_adc_aequence(pHidBridge,rep,temp,includeAdcChannels):
    """

    :param pHidBridge:
    :param rep:
                ADC sequence repetition.
              0: sequence repetition disabled (default).
              1: sequence repetition enabled.

    :param temp:
            Include temperature indicator in ADC sequence.
              0: disable temperature indicator readback (default).
              1: enable temperature indicator readback.

    :param includeAdcChannels:
                D7 - D0
                Include ADC channels in conversion sequence.
              0: the selected ADC channel is not included in the conversion sequence.
              1: include the selected ADC channel in the conversion sequence.

    :return:
    """
    msb = 0x10 | (rep << 1) | (temp)
    lsb = includeAdcChannels
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)
    # pi26_adc_aequence(pHidBridge,1,1,0XFF)


def pi26_adc_conversion_result(pHidBridge,rep,temp,includeAdcChannels,num):
    """
    ADC Conversion Result
    :param pHidBridge:
    :param num:
        Continuously read the ADC conversion value. 8 : ADC0 - ADC7 9 : add Temperature
    :return:
    """
    result = []
    pi26_adc_aequence(pHidBridge, rep, temp, includeAdcChannels)
    ch32_spi_full_duplex(pHidBridge, [0X00, 0X00], 2) # return invalid data
    for i in range(0,num) :
        data = ch32_spi_full_duplex(pHidBridge, [0X00, 0X00], 2) # return invalid data
        print(hex(((data[0] & 0X0F) << 8)| data[1]))
        result.append(hex(((data[0] & 0X0F) << 8)| data[1]))

    for num in range(0,num):  # change result from str to int
        result[num] = int(result[num],16)
    return result



def pi26_gpio_write_config(pHidBridge,busyEn,pin):
    """
    GPIO Write Configuration Register
    :param pHidBridge:
    :param busyEn:
        Enable the I/O7 pin as BUSY.
        0: Pin I/O7 is not configured as BUSY.
        1: Pin I/O7 is configured as BUSY. D7 must also be set to 1 to enable the I/O7 pin as an output.
    :param pin:
        Select I/Ox pins as GPIO outputs.
        1: I/Ox is a general-purpose output pin.
        0: I/Ox function is determined by the pin configuration registers (default).
    :return:
    """
    msb = (GPIO_Write_Configuration << 3) | busyEn
    lsb = (pin)
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)


def pi26_gpio_open_drain_con(pHidBridge,pin):
    """
    GPIO Open-Drain Configuration Register
    :param pHidBridge:
    :param pin:
        Set output pins as open-drain. The pins must also be set as digital output pins. See Table 31.
          1: I/Ox is an open-drain output pin.
          0: I/Ox is a push/pull output pin (default).
    :return:
    """
    msb = (GPIO_Open_Drain_Configuration << 3)
    lsb = (pin)
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)

def pi26_gpio_write_data(pHidBridge,logicVal):
    """
    GPIO Write Data Register
    :param pHidBridge:
    :param logicVal:
        Set state of output pins.
          1: I/Ox is a Logic 1.
          0: I/Ox is a Logic 0.
    :return:
    """
    msb = (GPIO_Write_Data << 3)
    lsb = logicVal
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)


def pi26_gpio_read_con(pHidBridge,readbackEn,pin):
    """

    :param pHidBridge:
    :param readbackEn:
            Enable GPIO readback.
              1: the next SPI operation clocks out the state of the GPIO pins.
              0: Bit D7 to Bit D0 determine which pins are set as general-purpose inputs.
    :param pin:
    D7 - D0
            Set I/Ox pins as GPIO inputs.
              1: I/Ox is a general-purpose input pin.
              0: I/Ox function is determined by the pin configuration registers (default).
    :return: the state of GPIO input
    """
    msb = (GPIO_Read_Configuration << 3) | (readbackEn << 2)
    lsb = pin
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)
    data = ch32_spi_full_duplex(pHidBridge, [0x00, 0x00], 2)
    result = hex(data[1])
    return result

def pi26_three_state_con(pHidBridge,pin):
    """

    :param pHidBridge:
    :param pin:
        D7 -D0
        Set I/Ox pins as three-state outputs.
          1: I/Ox is a three-state output pin.
          0: I/Ox function is determined by the pin configuration registers (default).
    :return:
    """
    msb = (Three_State_Configuration << 3)
    lsb = pin
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)


def pi26_pull_down_con(pHidBridge,pin):
    """

    :param pHidBridge:
    :param pin:
        D7 - D0
        Set I/Ox pins as weak pull-down outputs.
          1: I/Ox is connected to GND via an 85 kΩ pull-down resistor.
          0: I/Ox function is determined by the pin configuration registers (default).
    :return:
    """
    msb = (Pull_Down_Configuration << 3)
    lsb = pin
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)


def pi26_power_down_reference_control(pHidBridge,pdAll,refEn,pin):
    """
    Power-Down/Reference Control Register
    :param pHidBridge:
    :param pdAll:
        Power down DACs and internal reference.
        0: the reference and DACs power-down states are determined by D9 and D7 to D0 (default).
        1: the reference, DACs and ADC are powered down.
    :param refEn:
        Enable internal reference.
        0: the reference and its buffer are powered down (default). Set this bit if an external reference is used.
        1: the reference and its buffer are powered up. The reference is available on the VREF pin.
    :param pin:
        D7 - D0
        Power down DACs.
        0: the channel is in normal operating mode (default).
        1: the channel is powered down if it is configured as a DAC.
    :return:
    """
    msb = (0b1011 << 3) | (pdAll << 2) | (refEn << 1)
    lsb = pin
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)

def pi26_soft_reset(pHidBridge):
    """
    :param pHidBridge:
    :return:
    """
    ch32_spi_full_duplex(pHidBridge, [0x7D, 0xAC], 2)


def pi26_readback_ldac_mode(pHidBridge, pEnable, regSel, pLdacMode):
    """

    :param pHidBridge:
    :param pEnable:
        Enable readback. Note that the LDAC mode bits are always used regardless of the EN bit.
        1: Bit D5 to Bit D2 select which register is read back. Bit D6 automatically clears when the read is complete.
        0: no readback is initiated.
    :param regSel:
        If Bit D6 is 1, Bits D5 to Bit D2 determine which register is to be read back.
        0000: NOP.
        0001: DAC readback.
        0010: ADC sequence.
        0011: general-purpose configuration.
        0100: ADC pin configuration.
        0101: DAC pin configuration.
        0110: pull-down configuration.
        0111: LDAC configuration.
        1000: GPIO write configuration.
        1001: GPIO write data.
        1010: GPIO read configuration.
        1011: power-down and reference control.
        1100: open-drain configuration.
        1101: three-state pin configuration.
        1110: reserved.
        1111: software reset.
    :param pLdacMode:

    :return:
    """
    msb = 0x38      # register address is 0b0111
    lsb = (pEnable << 6) | (regSel << 2) | pLdacMode  # include EN,REG_READBACK & LDAC mode
    ch32_spi_full_duplex(pHidBridge, [msb, lsb], 2)





def pi26_osc_fre(pHidBridge):
    """
    GPIO0 output OSC frequency
    :param pHidBridge:
    :return:
    """
    pi26_spi_write(pHidBridge, 0x7001)
    pi26_spi_write(pHidBridge, 0xA0C0)
    pi26_spi_write(pHidBridge, 0xA1DE)
    pi26_spi_write(pHidBridge, 0xA240)  # ?    pi26_spi_write(hidBridge, 0x7001)
    pi26_spi_write(pHidBridge, 0xA0C0)
    pi26_spi_write(pHidBridge, 0xA1DE)
    pi26_spi_write(pHidBridge, 0xA240)  # ?


def pi26_osc_fre_off(pHidBridge):
    """
    GPIO0 does not output OSC frequency
    :param pHidBridge:
    :return:
    """
    pi26_spi_write(pHidBridge, 0xA200)

###############################################

def pi26_vref_config(pHidBridge,vrefEn):
    """
    configure pi26 vref source
    :param pHidBridge: hid bridge object
    :param vrefen: one bit
                  0 - external vref
                  1 - internal vref (2.5V)
    :return:
    """
    # vref = (Power_Down_Reference_Control<<3) | (vrefen<<1)
    #
    # ch32_spi_full_duplex(pHidBridge, [vref, 0x00], 2)
    pi26_power_down_reference_control(pHidBridge, 0, vrefEn, 0)


def pi26_readback_reg(pHidBridge,regSel):
    """

    :param pHidBridge:
    :param pEnable:
        Enable readback. Note that the LDAC mode bits are always used regardless of the EN bit.
        1: Bit D5 to Bit D2 select which register is read back. Bit D6 automatically clears when the read is complete.
        0: no readback is initiated.
    :param regSel:
        If Bit D6 is 1, Bits D5 to Bit D2 determine which register is to be read back.
        0000: NOP.
        0001: DAC readback.
        0010: ADC sequence.
        0011: general-purpose configuration.
        0100: ADC pin configuration.
        0101: DAC pin configuration.
        0110: pull-down configuration.
        0111: LDAC configuration.
        1000: GPIO write configuration.
        1001: GPIO write data.
        1010: GPIO read configuration.
        1011: power-down and reference control.
        1100: open-drain configuration.
        1101: three-state pin configuration.
        1110: reserved.
        1111: software reset.
    :param pLdacMode:

    :return:
    """
    pi26_readback_ldac_mode(pHidBridge, 1, regSel, 0b00)
    rtData = ch32_spi_full_duplex(pHidBridge, [0x00, 0x00], 2)
    print(f" register {bin(regSel)} 's data is {hex((rtData[0] << 8) | rtData[1])}")
    return hex((rtData[0] << 8) | rtData[1])