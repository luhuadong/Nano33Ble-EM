# 导入模块
import pygatt
import time
import wx
import threading
import binascii
import uuid


temp_characteristic  = "00002a6e-0000-1000-8000-00805f9b34fb"
humi_characteristic  = "00002a6f-0000-1000-8000-00805f9b34fb"
pres_characteristic  = "00002a6d-0000-1000-8000-00805f9b34fb"
light_characteristic = "936b6a25-e503-4f7c-9349-bcc76c22b8c3"
noise_characteristic = "936b6a25-e503-4f7c-9349-bcc76c22b8c4"

adapter = pygatt.GATTToolBackend()
macaddr = '93:89:C7:2D:5F:12'
delay = 3

class AppUI(wx.Frame):

    def __init__(self, parent, title="Environmental Monitor"):
        wx.Frame.__init__(self, parent, title=title)
        self.Center()

        self.panel = wx.Panel(self)
        self.tLabel = wx.StaticText(self.panel, label="环境温度")
        self.hLabel = wx.StaticText(self.panel, label="环境湿度")
        self.pLabel = wx.StaticText(self.panel, label="大气压强")
        self.lLabel = wx.StaticText(self.panel, label="日照强度")
        self.nLabel = wx.StaticText(self.panel, label="平均噪声")

        self.tValueLabel = wx.StaticText(self.panel, label="0")
        #self.tValueLabel = wx.StaticText(self.panel,-1, style = wx.ALIGN_CENTER, label="-1")
        self.hValueLabel = wx.StaticText(self.panel, label="0")
        self.pValueLabel = wx.StaticText(self.panel, label="0")
        self.lValueLabel = wx.StaticText(self.panel, label="0")
        self.nValueLabel = wx.StaticText(self.panel, label="0")

        #self.__startBtn  = wx.Button(self.panel, label="Start")
        #self.__stopBtn   = wx.Button(self.panel, label="Stop")

        vbox1 = wx.BoxSizer(wx.VERTICAL)  # 默认水平布局
        vbox1.Add(self.tLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(self.hLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(self.pLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(self.lLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(self.nLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        #vbox1.Add(self.__startBtn, proportion=1, flag=wx.ALIGN_CENTER, border=20)

        vbox2 = wx.BoxSizer(wx.VERTICAL)  # 默认水平布局
        vbox2.Add(self.tValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.hValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.pValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.lValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.nValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        #vbox2.Add(self.__stopBtn, proportion=1, flag=wx.ALIGN_CENTER, border=20)

        hbox = wx.BoxSizer()
        hbox.Add(vbox1, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        hbox.Add(vbox2, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        self.panel.SetSizer(hbox)

    def connect(self, macaddr, period=3000):
        try:
            adapter.start()
            self.device = adapter.connect(macaddr)
            self.period = period
            print("BLE connected")
        except:
            print("BLE device init failed")
            adapter.stop()

    def subscribe(self):
        self.device.subscribe(uuid.UUID(temp_characteristic), callback=self.handleTempData, wait_for_response=True)
        #time.sleep(delay)
        #self.device.subscribe(uuid.UUID(humi_characteristic), callback=self.handleHumiData, wait_for_response=True)
        #time.sleep(delay)
        #self.device.subscribe(uuid.UUID(pres_characteristic), callback=self.handleBaroData, wait_for_response=True)
        #time.sleep(delay)
        #self.device.subscribe(uuid.UUID(light_characteristic), callback=self.handleLightData, wait_for_response=True)
        #time.sleep(delay)
        #self.device.subscribe(uuid.UUID(noise_characteristic), callback=self.handleNoiseData, wait_for_response=True)
        print("BLE subscribe success")

    def getDevice(self):
        return self.device

    def handleTempData(self, handle, value):
        temp = (value[1] * 256 + value[0]) / 100
        tempStr = "{:.2f}".format(temp)
        #tempStr = "tempStr"
        txt1 = "Python GUI development"
        txt2 = "using wxPython"
        txt3 = " Python port of wxWidget "
        txt = txt1+"\n"+txt2+"\n"+txt3
        print("temp : {:.2f} 'C".format(temp))
        #self.tValueLabel.SetLabelText(tempStr)
        self.tValueLabel.SetLabelText(tempStr)
        #self.tValueLabel.SetLabel("{:.2f} 'C".format(temp))

    def handleHumiData(self, handle, value):
        humi = (value[1] * 256 + value[0]) / 100
        print("humi : {:.2f} %".format(humi))
        self.hValueLabel.SetLabel("{:.2f} %".format(humi))

    def handleBaroData(self, handle, value):
        baro = (value[2] * 256 * 256 + value[1] * 256 + value[0]) / 10
        print("baro : {:.2f} Pa".format(baro))
        self.pValueLabel.SetLabel("{:.2f} Pa".format(baro))

    def handleLightData(self, handle, value):
        light = (value[1] * 256 + value[0]) / 100
        print("light : {:.2f}   ".format(light))
        self.lValueLabel.SetLabel("{:.2f}   ".format(light))

    def handleNoiseData(self, handle, value):
        noise = (value[1] * 256 + value[0]) / 100
        print("noise : {:.2f} dB".format(noise))
        self.nValueLabel.SetLabel("{:.2f} 'C".format(noise))

    def updateData(self):
        #value = device.char_read("00002a6e-0000-1000-8000-00805f9b34fb")
        self.tValue = self.device.char_read_handle("0x000f")
        self.hValue = self.device.char_read_handle("0x0012")
        self.pValue = self.device.char_read_handle("0x0015")
        self.lValue = self.device.char_read_handle("0x0018")
        self.nValue = self.device.char_read_handle("0x001c")

        self.temp = (self.tValue[1] * 256 + self.tValue[0]) / 100
        self.humi = (self.hValue[1] * 256 + self.hValue[0]) / 100
        self.baro = (self.pValue[2] * 256 * 256 + self.pValue[1] * 256 + self.pValue[0]) / 10
        self.light = (self.lValue[1] * 256 + self.lValue[0]) / 100
        self.noise = (self.nValue[1] * 256 + self.nValue[0]) / 100

        print("temp : {:.2f} 'C".format(self.temp))
        print("humi : {:.2f} % ".format(self.humi))
        print("baro : {:.2f} Pa".format(self.baro))
        print("light: {:.2f}   ".format(self.light))
        print("noise: {:.2f} dB".format(self.noise))
        print("--------------------------------")

        self.tValueLabel.SetLabelText("{:.2f} 'C".format(self.temp))
        self.hValueLabel.SetLabelText("{:.2f} % ".format(self.humi))
        self.pValueLabel.SetLabelText("{:.2f} Pa".format(self.baro))
        self.lValueLabel.SetLabelText("{:.2f}   ".format(self.light))
        self.nValueLabel.SetLabelText("{:.2f} dB".format(self.noise))


def main():
    # 创建应用程序对象
    app = wx.App()

    #ble = BleDevice()
    #ble.connect(macaddr)
    #ble.updateData()
    win = AppUI(None)
    win.Show()

    win.connect(macaddr)
    #win.updateData()
    time.sleep(delay)
    win.subscribe()

    # 进入应用程序事件主循环
    app.MainLoop()


if __name__ == '__main__':
    main()
