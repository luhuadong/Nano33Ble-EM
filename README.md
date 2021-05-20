# Nano33Ble-EM

An demo using Arduino Nano 33 BLE Sense for Environmental monitoring



## 实现功能

完成 Funpack 第8期任务 —— **环境监测站**

利用 Nano-33 BLE 的传感器，搭建一个小型环境监测站用于监测户外环境。待监测的参数包括：

- [x] 周边环境温度（精度：±0.1°C, ±0.1°F）
- [x] 周边环境湿度（精度：±1%）
- [x] 大气压强（精度：±0.1kPa, ±0.1psi）
- [x] 日照强度（用于判断白天/夜晚）
- [x] 周边平均噪声（精度：±1dB）

数据信息反馈方式可采用以下任意一种方式：

- [ ] 通过对开发板外接显示屏显示
- [x] 通过蓝牙在电脑端口显示
- [ ] 通过手机 App



## 代码说明

本项目代码分为两部分

| 运行平台 | 软件名称                                                     | 说明                                     |
| -------- | ------------------------------------------------------------ | ---------------------------------------- |
| Arduino  | [nina-air.ino](https://github.com/luhuadong/Nano33Ble-EM/blob/main/code/nina-air/nina-air.ino) | 使用 Arduino IDE 编译、上传              |
| PC       | [EnvironmentalMonitor.py](https://github.com/luhuadong/Nano33Ble-EM/blob/main/code/EnvironmentalMonitor.py) | Python 桌面程序，依赖 pygatt 和 wxPython |

重点说明：

- Arduino 通过板载传感器采集温度、湿度、气压、光强、噪声五组数据，其中温度、湿度、气压数据直接从传感器读取，光强、噪声数据通过计算转换；
- Arduino 开启 Standard Environmental Sensing 服务（181A），温度、湿度、气压使用预设 UUID，光强、噪声则使用自定义 UUID；
- Arduino 的 Standard Environmental Sensing 服务的特征值均使用 Read 和 Notify 方式，因此 BLE Client 可以通过主动读取和被动监听的方式接收数据；
- 通过 BLE 传输的数据均为整型数据，需进行转换才能显示；
- 运行 EnvironmentalMonitor.py 前请先安装依赖，并将 macaddr 修改为您所使用的 Nano 33 BLE 板的 MAC 地址。



## 演示效果

基于 wxPython 框架的 Environmental Monitor 桌面程序

![](https://static.getiot.tech/Nano33Ble_EnvironmentalMonitor_Day.png)

当亮度不足时，判定为夜晚，并切换图片

![](https://static.getiot.tech/Nano33Ble_EnvironmentalMonitor_Night.png)



## 心得体会

很高兴再次参加得捷电子和硬禾学堂联合推出的 Funpack 活动，最近工作比较忙，原本计划不参加的，可是被 Arduino Nano 33 BLE Sense 极高的可玩性和**投篮运动手柄**项目吸引了。不过最后没有很好完成投篮运动手柄，临时改成**环境监测站**项目，并且超出截止日期。

但不管怎样，每次参加 Funpack 都能学到东西，而且是快乐地学习，这种感觉跟工作是不一样的，有点像回到大学时期的感觉，很棒！嗯，后面还要抽时间继续完成投篮运动手柄项目。

