"""

"""
import time

time_delay = 0.05

def ch32_spi_full_duplex(pHidBdg, pData, pNum):
    """
    ch32 bridge spi full duplex communication (used case like pb01)
    :param pData: send data which is transmitted in mosi line
                  (note: list format, each element is byte, like [0x5a, 0x36])
    :param pNum: the number of return data which in transmitted in miso line
    :return: return data which is from spi slave device (return data format is bytes)
    """
    data = [0x1, len(pData) + 5, 0x03, 0x11, 0x0, 0x0, len(pData)]
    data.extend(pData)
    pHidBdg.write(data)
    time.sleep(time_delay)
    read_data = pHidBdg.read(pNum + 1)
    return read_data[1:]


def ch32_i2c_write(pHidBdg, pSlaveAddr, pI2cConf, pDataList):
    """
    i2c write function
    :param pHidBdg: hid object
    :param pSlaveAddr: slave address (7bit address)
    :param pI2cConf: i2c configuration (note: 8bit like 0x5A)
                     - user can use pI2cConf to configure i2c speed etc.
    :param pDataList: write data list (note: list format, like [0x5A, 0xA5])
                      - pDataList can include lots of information,
                      - like block address, register address, write data etc.
                      - protocol layer can be implemented in this list.
    :return:
    """
    data = [0x1, len(pDataList) + 5, 0x01, 0x12, pSlaveAddr, pI2cConf, len(pDataList)]
    data.extend(pDataList)
    pHidBdg.write(data)
    time.sleep(time_delay)


def ch32_i2c_read(pHidBdg, pSlaveAddr, pI2cConf, pReadNum, pRegAddr):
    """
    i2c read function
    :param pHidBdg: hid object
    :param pSlaveAddr: slave address (7bit address)
    :param pI2cConf: i2c configuration (note: 8bit like 0x5A)
                     - user can use pI2cConf to configure i2c speed etc.
    :param pReadNum: read data number
    :param pRegAddr: read register address (note: list format, like [0x20])
                     - to support 16bit or more bit register address, using list format
    :return:
    """
    # send read register address
    data = [0x1, len(pRegAddr)+5, 0x02, 0x12, pSlaveAddr, pI2cConf, pReadNum]
    data.extend(pRegAddr)
    pHidBdg.write(data)
    time.sleep(time_delay)
    # read data from hid device
    read_data = pHidBdg.read(pReadNum + 1)
    return read_data[1:]


def ch32_gpio_write(pHidBdg, gpio_pin, gpio_data ):
    """
    GPIO write function
    :param pHidBdg: hid object
    :param gpio_pin: gpio pin number
                      0 - gpio0
                      1 - gpio1
                      2 - gpio2
                      3 - gpio3
                      ...
                      7 - gpio7
    :param gpio_data: gpio toggle value (note: list format, like [0x01])
                      0 - gpio output low
                      1 - gpio output high
    :return:
    """
    data = [0x1, len(gpio_data) + 5, 0x01, 0x80, gpio_pin, 0x00, len(gpio_data)]
    data.extend(gpio_data)
    pHidBdg.write(data)
    time.sleep(0.05)
