# 导入模块
import pygatt
import time
import wx

adapter = pygatt.GATTToolBackend()
macaddr = '93:89:C7:2D:5F:12'


class BleDevice:

    def __init__(self) -> None:
        self.InitUI()

    def InitUI(self):
        win = wx.Frame(None, title="Environmental Monitor")
        bkg = wx.Panel(win)

        tLabel = wx.StaticText(bkg, label="环境温度")
        hLabel = wx.StaticText(bkg, label="环境湿度")
        pLabel = wx.StaticText(bkg, label="大气压强")
        lLabel = wx.StaticText(bkg, label="日照强度")
        nLabel = wx.StaticText(bkg, label="平均噪声")

        self.tValueLabel = wx.StaticText(bkg, label="0")
        self.hValueLabel = wx.StaticText(bkg, label="0")
        self.pValueLabel = wx.StaticText(bkg, label="0")
        self.lValueLabel = wx.StaticText(bkg, label="0")
        self.nValueLabel = wx.StaticText(bkg, label="0")

        vbox1 = wx.BoxSizer(wx.VERTICAL)  # 默认水平布局
        vbox1.Add(tLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(hLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(pLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(lLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox1.Add(nLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)

        vbox2 = wx.BoxSizer(wx.VERTICAL)  # 默认水平布局
        vbox2.Add(self.tValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.hValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.pValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.lValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)
        vbox2.Add(self.nValueLabel, proportion=1, flag=wx.ALIGN_CENTER, border=20)

        hbox = wx.BoxSizer()
        hbox.Add(vbox1, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        hbox.Add(vbox2, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        bkg.SetSizer(hbox)

        win.Show()

    def connect(self, macaddr, period=3):
        try:
            adapter.start()
            self.__device = adapter.connect(macaddr)
        except:
            print("BLE device init failed")
            adapter.stop()

    def getDevice(self):
        return self.__device

    def updateData(self):
        #value = device.char_read("00002a6e-0000-1000-8000-00805f9b34fb")
        tValue = self.__device.char_read_handle("0x000f")
        hValue = self.__device.char_read_handle("0x0012")
        pValue = self.__device.char_read_handle("0x0015")
        lValue = self.__device.char_read_handle("0x0018")
        nValue = self.__device.char_read_handle("0x001c")

        temp = (tValue[1] * 256 + tValue[0]) / 100
        humi = (hValue[1] * 256 + hValue[0]) / 100
        baro = (pValue[2] * 256 * 256 + pValue[1] * 256 + pValue[0]) / 10
        light = (lValue[1] * 256 + lValue[0]) / 100
        noise = (nValue[1] * 256 + nValue[0]) / 100

        print("temp : {:.2f} 'C".format(temp))
        print("humi : {:.2f} % ".format(humi))
        print("baro : {:.2f} Pa".format(baro))
        print("light: {:.2f}   ".format(light))
        print("noise: {:.2f} dB".format(noise))

        self.tValueLabel.SetLabelText("{:.2f} 'C".format(temp))
        self.hValueLabel.SetLabelText("{:.2f} % ".format(humi))
        self.pValueLabel.SetLabelText("{:.2f} Pa".format(baro))
        self.lValueLabel.SetLabelText("{:.2f}   ".format(light))
        self.nValueLabel.SetLabelText("{:.2f} dB".format(noise))


def main():
    # 创建应用程序对象
    app = wx.App()

    ble = BleDevice()
    ble.connect(macaddr)
    ble.updateData()

    # 进入应用程序事件主循环
    app.MainLoop()


if __name__ == '__main__':
    main()
