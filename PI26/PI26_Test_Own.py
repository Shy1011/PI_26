from pi26Driver import *
import hid
"""
When change from DAC/ADC to GPIO mode. 
Please reset the chip and turn on the internal Vref
Because one chip can not be configured as DAC/ADC and GPIO at the same time.
"""
if __name__ == '__main__':
    hidBridge = hid.device()
    hidBridge.open(0x1a86, 0xfe07)
    hidBridge.set_nonblocking(1)

    while(1) :
        """reset pi26"""
        pi26_reset(hidBridge)

        """turn on internal vref"""
        pi26_vref_config(hidBridge,1)

        """"GPIO0 output OSC fre"""
        pi26_osc_fre(hidBridge)

        """GPIO0 no more output OSC fre"""
        pi26_osc_fre_off(hidBridge)

        """GPIO_Write_Data"""
        pi26_gpio_write_data(hidBridge, 0X56)

        """Readback from All the registers """
        # pi26_readback_reg(hidBridge,GPIO_Write_Data)
        # pi26_readback_reg(hidBridge, Pull_Down_Configuration)

        pi26_readback_reg(hidBridge,DAC_Readback)
        pi26_readback_reg(hidBridge,ADC_Sequence_Register)
        pi26_readback_reg(hidBridge,General_Purpose_Control_Register)
        pi26_readback_reg(hidBridge,ADC_Pin_Configuration)
        pi26_readback_reg(hidBridge,DAC_Pin_Configuration)
        pi26_readback_reg(hidBridge,Pull_Down_Configuration)
        pi26_readback_reg(hidBridge,Readback_and_LDAC_Mode)
        pi26_readback_reg(hidBridge,GPIO_Write_Configuration)
        pi26_readback_reg(hidBridge,GPIO_Write_Data)
        pi26_readback_reg(hidBridge,GPIO_Read_Configuration)
        pi26_readback_reg(hidBridge,Power_Down_Reference_Control)
        pi26_readback_reg(hidBridge,GPIO_Open_Drain_Configuration)
        pi26_readback_reg(hidBridge,Three_State_Configuration)
        pi26_readback_reg(hidBridge,Software_Reset)



        """reset the GPIO"""
        pi26_reset(hidBridge)

        """turn on internal vref"""
        pi26_vref_config(hidBridge,1)


        """Set ALL GPIO to DAC"""
        pi26_dac_pin_config(hidBridge,0XFF)

        """Set all DAC0 output 0X800"""
        pi26_dac_write(hidBridge,0b000,0x800)
        pi26_dac_write(hidBridge, 0b001, 0x800)
        pi26_dac_write(hidBridge, 0b010, 0x800)
        pi26_dac_write(hidBridge, 0b011, 0x800)
        pi26_dac_write(hidBridge, 0b100, 0x800)
        pi26_dac_write(hidBridge, 0b101, 0x800)
        pi26_dac_write(hidBridge, 0b110, 0x800)
        pi26_dac_write(hidBridge, 0b111, 0x800)

        """Readback from DAC Readback Register"""
        pi26_dac_readback(hidBridge,0b11,0b010)
        pi26_pull_down_con(hidBridge,0X00)

        """Set all GPIOs to ADC"""
        pi26_adc_pin_con(hidBridge,0XFF)

        """Open ADC sequence repetition"""
        pi26_adc_aequence(hidBridge, 1, 1, 0XFF)


        """Readback from ADC"""
        result = pi26_adc_conversion_result(hidBridge,1,1,0XFF,9)

        """Get difference between DAC's value with ADC's readback value"""
        difference = []
        for n in result :
            difference.append(hex(0x800 - n))
        print(f"The difference between 0X800 and ADC readback value are : {difference}")


        """reset the GPIO"""
        pi26_reset(hidBridge)

        """turn on internal vref"""
        pi26_vref_config(hidBridge,1)

        """Set all GPIO to output"""
        pi26_gpio_write_config(hidBridge,0,0XFF)

        """"Set GPIO logics to 0XFF"""
        pi26_gpio_write_data(hidBridge,0XFF)

        """Readback from GPIO input"""
        print(pi26_gpio_read_con(hidBridge,1,0XFF))

        """"Set GPIO logics to 0XFF"""
        pi26_gpio_write_data(hidBridge,0X55)

        """Readback from GPIO input"""
        print(pi26_gpio_read_con(hidBridge,1,0XFF))

        """"Set GPIO logics to 0XFF"""
        pi26_gpio_write_data(hidBridge,0XAA)

        """Readback from GPIO input"""
        print(pi26_gpio_read_con(hidBridge,1,0XFF))

        temp = pi26_adc_conversion_result(hidBridge,1,1,0X00,1)
        temperature = 25 + ((temp[0]-(0.5/2.5)*4095)/(2.654*(2.5/2.5)))
        print(temperature)

        input()




