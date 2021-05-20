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
        wx.Frame.__init__(self, parent, title=title, size=(400, 250))
        self.Center()

        icon = wx.Icon()
        icon.LoadFile("day.png", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        #self.tbicon=wx.Icon()
        #self.tbicon.SetIcon(icon,"Environmental Monitor")

        self.panel = wx.Panel(self)
        self.tLabel = wx.StaticText(self.panel, style = wx.ALIGN_CENTER, label="环境温度")
        self.hLabel = wx.StaticText(self.panel, style = wx.ALIGN_CENTER, label="环境湿度")
        self.pLabel = wx.StaticText(self.panel, style = wx.ALIGN_CENTER, label="大气压强")
        self.lLabel = wx.StaticText(self.panel, style = wx.ALIGN_CENTER, label="日照强度")
        self.nLabel = wx.StaticText(self.panel, style = wx.ALIGN_CENTER, label="平均噪声")

        self.tValueLabel = wx.StaticText(self.panel, style = wx.ALIGN_CENTER, label="-1")
        self.hValueLabel = wx.StaticText(self.panel, style = wx.ALIGN_CENTER, label="0")
        self.pValueLabel = wx.StaticText(self.panel, style = wx.ALIGN_CENTER, label="0")
        self.lValueLabel = wx.StaticText(self.panel, style = wx.ALIGN_CENTER, label="0")
        self.nValueLabel = wx.StaticText(self.panel, style = wx.ALIGN_CENTER, label="0")

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

        bmp = wx.Bitmap('day.png')
        self.img = wx.StaticBitmap(self.panel, -1, bmp)

        hbox = wx.BoxSizer()
        hbox.Add(vbox1, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        hbox.Add(vbox2, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        hbox.Add(self.img, proportion=1, flag=wx.EXPAND | wx.ALL, border=40)
        self.panel.SetSizer(hbox)

    def startBle(self):
        self.bleThread = BleThread(self)
        self.bleThread.start()

    def updateTempData(self, value):
        self.tValueLabel.SetLabelText(value)

    def updateHumiData(self, value):
        self.hValueLabel.SetLabelText(value)

    def updatePresData(self, value):
        self.pValueLabel.SetLabelText(value)

    def updateLightData(self, value):
        self.lValueLabel.SetLabelText(value)
        if (float(value) < 0.5):
            bmp = wx.Bitmap('night.png')
            self.img.SetBitmap(bmp)
        else:
            bmp = wx.Bitmap('day.png')
            self.img.SetBitmap(bmp)

    def updateNoiseData(self, value):
        self.nValueLabel.SetLabelText(value)


class BleThread(threading.Thread):

    def __init__(self, parent):
        super(BleThread, self).__init__()  # 继承
        self.parent = parent
        self.setDaemon(True)

    def run(self):
        self.connect(macaddr)
        self.updateData()
        time.sleep(delay)
        self.subscribe()
        while 1:
            time.sleep(1000)

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
        time.sleep(delay)
        self.device.subscribe(uuid.UUID(humi_characteristic), callback=self.handleHumiData, wait_for_response=True)
        time.sleep(delay)
        self.device.subscribe(uuid.UUID(pres_characteristic), callback=self.handleBaroData, wait_for_response=True)
        time.sleep(delay)
        self.device.subscribe(uuid.UUID(light_characteristic), callback=self.handleLightData, wait_for_response=True)
        time.sleep(delay)
        self.device.subscribe(uuid.UUID(noise_characteristic), callback=self.handleNoiseData, wait_for_response=True)
        print("BLE subscribe success")

    def getDevice(self):
        return self.device

    def handleTempData(self, handle, value):
        temp = (value[1] * 256 + value[0]) / 100
        tempStr = "{:.2f} ℃".format(temp)
        print("temp : {:.2f} 'C".format(temp))
        wx.CallAfter(self.parent.updateTempData, tempStr)

    def handleHumiData(self, handle, value):
        humi = (value[1] * 256 + value[0]) / 100
        humiStr = "{:.2f} %".format(humi)
        print("humi : {:.2f} %".format(humi))
        #self.hValueLabel.SetLabel("{:.2f} %".format(humi))
        wx.CallAfter(self.parent.updateHumiData, humiStr)

    def handleBaroData(self, handle, value):
        baro = (value[2] * 256 * 256 + value[1] * 256 + value[0]) / 10 / 1000
        baroStr = "{:.2f} kPa".format(baro)
        print("baro : {:.2f} kPa".format(baro))
        #self.pValueLabel.SetLabel("{:.2f} Pa".format(baro))
        wx.CallAfter(self.parent.updatePresData, baroStr)

    def handleLightData(self, handle, value):
        light = (value[1] * 256 + value[0]) / 100
        lightStr = "{:.2f}   ".format(light)
        print("light : {:.2f}   ".format(light))
        #self.lValueLabel.SetLabel("{:.2f}   ".format(light))
        wx.CallAfter(self.parent.updateLightData, lightStr)

    def handleNoiseData(self, handle, value):
        noise = (value[1] * 256 + value[0]) / 100
        noiseStr = "{:.2f} dB".format(noise)
        print("noise : {:.2f} dB".format(noise))
        #self.nValueLabel.SetLabel("{:.2f} 'C".format(noise))
        wx.CallAfter(self.parent.updateNoiseData, noiseStr)

    def updateData(self):
        #value = device.char_read("00002a6e-0000-1000-8000-00805f9b34fb")
        tValue = self.device.char_read_handle("0x000f")
        hValue = self.device.char_read_handle("0x0012")
        pValue = self.device.char_read_handle("0x0015")
        lValue = self.device.char_read_handle("0x0018")
        nValue = self.device.char_read_handle("0x001c")

        self.handleTempData(0, tValue)
        self.handleHumiData(0, hValue)
        self.handleBaroData(0, pValue)
        self.handleLightData(0, lValue)
        self.handleNoiseData(0, nValue)

        #self.temp = (self.tValue[1] * 256 + self.tValue[0]) / 100
        #self.humi = (self.hValue[1] * 256 + self.hValue[0]) / 100
        #self.baro = (self.pValue[2] * 256 * 256 + self.pValue[1] * 256 + self.pValue[0]) / 10
        #self.light = (self.lValue[1] * 256 + self.lValue[0]) / 100
        #self.noise = (self.nValue[1] * 256 + self.nValue[0]) / 100

        #print("temp : {:.2f} 'C".format(self.temp))
        #print("humi : {:.2f} % ".format(self.humi))
        #print("baro : {:.2f} Pa".format(self.baro))
        #print("light: {:.2f}   ".format(self.light))
        #print("noise: {:.2f} dB".format(self.noise))
        #print("--------------------------------")

        #self.tValueLabel.SetLabelText("{:.2f} 'C".format(self.temp))
        #self.hValueLabel.SetLabelText("{:.2f} % ".format(self.humi))
        #self.pValueLabel.SetLabelText("{:.2f} Pa".format(self.baro))
        #self.lValueLabel.SetLabelText("{:.2f}   ".format(self.light))
        #self.nValueLabel.SetLabelText("{:.2f} dB".format(self.noise))


def main():
    # 创建应用程序对象
    app = wx.App()

    #ble = BleDevice()
    #ble.connect(macaddr)
    #ble.updateData()
    win = AppUI(None)
    win.Show()
    win.startBle()

    # 进入应用程序事件主循环
    app.MainLoop()


if __name__ == '__main__':
    main()
