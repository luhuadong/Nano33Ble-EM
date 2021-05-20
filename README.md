# Nano33Ble-EM

An demo using Arduino Nano 33 BLE Sense for Environmental monitoring



## Funpack 第八期

**环境监测站**

利用 NANO-33 BLE 的传感器，搭建一个小型环境监测站用于监测户外环境。待监测的参数包括：

- 周边环境温度（精度：±0.1°C, ±0.1°F）
- 周边环境湿度（精度：±1%）
- 大气压强（精度：±0.1kPa, ±0.1psi）
- 日照强度（用于判断白天/夜晚）
- 周边平均噪声（精度：±1dB）

数据信息反馈方式可采用以下任意一种方式：

1. 通过对开发板外接显示屏显示
2. 通过蓝牙在电脑端口显示
3. 通过手机 App


wxPython 安装

```shell
pip3 install -U \
    -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 \
    wxPython

```

wx.StaticText

A static text control displays one or more lines of read-only text.

```python
StaticText() StaticText(parent, id=ID_ANY, label=EmptyString, pos=DefaultPosition, size=DefaultSize, style=0, name=StaticTextNameStr)
```

TextCtrl

A text control allows text to be displayed and edited.

```python
TextCtrl() TextCtrl(parent, id=ID_ANY, value=EmptyString, pos=DefaultPosition, size=DefaultSize, style=0, validator=DefaultValidator, name=TextCtrlNameStr)
```



相关链接

- <https://stackoverflow.com/questions/44964899/how-to-get-notifications-from-ble-device-using-pygatt-in-python>
- <https://blog.csdn.net/rumswell/article/details/6564181>
- <https://pypi.org/project/pygatt/>
- <https://github.com/peplin/pygatt/issues/232>
- <https://blog.csdn.net/qq_39136415/article/details/107108112>
- <https://github.com/wxWidgets/Phoenix/issues/465>
- <https://github.com/Gawhary/Qt-BLE-Tester>
- <https://blog.csdn.net/qq_26369907/article/details/90408513>

