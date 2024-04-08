# Shy
# 03/04/2024

"""
Example
Multimemter
test = Instrument()
name = test.get_device_name()
vol = test.voltage_detect(name[0])
cur = test.current_detect(name[0])
"""

import pyvisa
import time

class Multimemter():
    rm = pyvisa.ResourceManager()
    def __init__(self):
        print("Instrument Initial")


    def get_device_name(self):
        """

        :return: instruments name
        """
        # 创建一个资源管理器
        self.rm = pyvisa.ResourceManager()

        # 列出所有连接的VISA设备的资源描述符
        instruments = self.rm.list_resources()

        # 打印出所有找到的资源描述符
        for instrument in instruments:
            print(instrument)

        return instruments

    def voltage_detect(self,name):
        """

        :param name: Instrument name
        :return:
        """
        time.sleep(1)
        multimeter = self.rm.open_resource(name)
        multimeter.write('CONF:VOLT:DC AUTO')  # 设置为DC电压测量模式 量程自选
        # multimeter.write('CONF:CURR:DC AUTO') # 设置为DC电流测量模式 量程自选
        # 会将万用表配置为远程模式,要想实时测量需要按下shift(local)按键

        # 读取电压值
        voltage = multimeter.query('READ?')
        print(f"{voltage} V")
        return voltage

    def current_detect(self,name):
        """

        :param name: Instrument name
        :return:
        """
        time.sleep(1)
        multimeter = self.rm.open_resource(name)
        multimeter.write('CONF:CURR:DC AUTO') # 设置为DC电流测量模式 量程自选
        # 会将万用表配置为远程模式,要想实时测量需要按下shift(local)按键

        # 读取电流值
        current = multimeter.query('READ?')
        print(f"{current} A")
        return current


class PowerSource():
    def __init__(self):
        print("Power Source Initialize")

    def get_device_name(self):
        """

        :return: instruments name
        """
        # 创建一个资源管理器
        self.rm = pyvisa.ResourceManager()

        # 列出所有连接的VISA设备的资源描述符
        instruments = self.rm.list_resources()

        # 打印出所有找到的资源描述符
        for instrument in instruments:
            print(instrument)

        return instruments
