# 导入模块
import pygatt
import time
import wx
import threading
import binascii

adapter = pygatt.GATTToolBackend()
macaddr = '93:89:C7:2D:5F:12'

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
        self.hValueLabel = wx.StaticText(self.panel, label="0")
        self.pValueLabel = wx.StaticText(self.panel, label="0")
        self.lValueLabel = wx.StaticText(self.panel, label="0")
        self.nValueLabel = wx.StaticText(self.panel, label="0")

        self.__startBtn  = wx.Button(self.panel, label="Start")
        self.__stopBtn   = wx.Button(self.panel, label="Stop")

        vbox1 = wx.BoxSizer(wx.VERTICAL)  # 默认水平布局
        vbox1.Add(self.tLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(self.hLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(self.pLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(self.lLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(self.nLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(self.__startBtn, proportion=1, flag=wx.ALIGN_CENTER, border=20)

        vbox2 = wx.BoxSizer(wx.VERTICAL)  # 默认水平布局
        vbox2.Add(self.tValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.hValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.pValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.lValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.nValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.__stopBtn, proportion=1, flag=wx.ALIGN_CENTER, border=20)

        hbox = wx.BoxSizer()
        hbox.Add(vbox1, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        hbox.Add(vbox2, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        self.panel.SetSizer(hbox)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.__startBtn.Bind(wx.EVT_BUTTON, self.OnStart)
        self.__stopBtn.Bind(wx.EVT_BUTTON, self.OnStop)

        self.connect(macaddr)
        
    def OnTimer(self, event):
        self.updateData()

    def OnStart(self, event):
        self.timer.Start(self.__period)
        print("Start timer")

    def OnStop(self, event):
        self.timer.Stop()
        print("Stop timer")

    def connect(self, macaddr, period=3000):
        try:
            adapter.start()
            self.__device = adapter.connect(macaddr)
            self.__period = period
        except:
            print("BLE device init failed")
            adapter.stop()

    def getDevice(self):
        return self.__device

    def updateData(self):
        self.bleThread = BleThread(self, self.getDevice())
        self.bleThread.start()  # update data


class BleThread(threading.Thread):

    def __init__(self, parent, device):
        super(BleThread, self).__init__()  # 继承
        self.parent = parent
        self.__device = device

    def run(self):
        #value = device.char_read("00002a6e-0000-1000-8000-00805f9b34fb")
        self.tValue = self.__device.char_read_handle("0x000f")
        self.hValue = self.__device.char_read_handle("0x0012")
        self.pValue = self.__device.char_read_handle("0x0015")
        self.lValue = self.__device.char_read_handle("0x0018")
        self.nValue = self.__device.char_read_handle("0x001c")

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

        #self.tValueLabel.SetLabelText("{:.2f} 'C".format(temp))
        #self.hValueLabel.SetLabelText("{:.2f} % ".format(humi))
        #self.pValueLabel.SetLabelText("{:.2f} Pa".format(baro))
        #self.lValueLabel.SetLabelText("{:.2f}   ".format(light))
        #self.nValueLabel.SetLabelText("{:.2f} dB".format(noise))

class Event:
    def __init__(self):
        self.handlers = set()

    def handle(self, handler):
        self.handlers.add(handler)
        return self

    def unhandle(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    def getHandlerCount(self):
        return len(self.handlers)

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__  = getHandlerCount

class myBle:
    ADDRESS_TYPE = pygatt.BLEAddressType.random
    read_characteristic = "0000xxxx-0000-1000-8000-00805f9b34fb"
    write_characteristic = "0000xxxx-0000-1000-8000-00805f9b34fb"
    notify_characteristic = "0000xxxxx-0000-1000-8000-00805f9b34fb"
    def __init__(self, device):
        self.device = device
        self.valueChanged = Event()
        self.checkdata = False

    def alert(self):
         self.valueChanged(self.checkdata)

    def write(self,data):
        self.device.write_char(self.write_characteristic,binascii.unhexlify(data))

    def notify(self,handle,data):
        self.checkdata = True

    def read(self):
        if(self.checkdata):
            self.read_data = self.device.char_read(uuid.UUID(self.read_characteristic))
            self.write(bytearray(b'\x10\x00'))
            self.checkdata = False
            return self.read_data
    def discover(self):
        return self.device.discover_characteristics().keys()

def main():
    # 创建应用程序对象
    app = wx.App()

    #ble = BleDevice()
    #ble.connect(macaddr)
    #ble.updateData()
    AppUI(None).Show()

    # 进入应用程序事件主循环
    app.MainLoop()


if __name__ == '__main__':
    main()
