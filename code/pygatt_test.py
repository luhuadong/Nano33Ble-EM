"""
[Services]
attr handle: 0x0001, end grp handle: 0x0005 uuid: 00001800-0000-1000-8000-00805f9b34fb
attr handle: 0x0006, end grp handle: 0x0009 uuid: 00001801-0000-1000-8000-00805f9b34fb
attr handle: 0x000a, end grp handle: 0x000c uuid: 0000180c-0000-1000-8000-00805f9b34fb  (greetingService)
attr handle: 0x000d, end grp handle: 0x001d uuid: 0000181a-0000-1000-8000-00805f9b34fb  (environmentService)

[Characteristics]
handle: 0x0002, char properties: 0x02, char value handle: 0x0003, uuid: 00002a00-0000-1000-8000-00805f9b34fb
handle: 0x0004, char properties: 0x02, char value handle: 0x0005, uuid: 00002a01-0000-1000-8000-00805f9b34fb
handle: 0x0007, char properties: 0x20, char value handle: 0x0008, uuid: 00002a05-0000-1000-8000-00805f9b34fb
handle: 0x000b, char properties: 0x02, char value handle: 0x000c, uuid: 00002a56-0000-1000-8000-00805f9b34fb  (greeting)
handle: 0x000e, char properties: 0x12, char value handle: 0x000f, uuid: 00002a6e-0000-1000-8000-00805f9b34fb  (temperature)
handle: 0x0011, char properties: 0x12, char value handle: 0x0012, uuid: 00002a6f-0000-1000-8000-00805f9b34fb  (humidity)
handle: 0x0014, char properties: 0x12, char value handle: 0x0015, uuid: 00002a6d-0000-1000-8000-00805f9b34fb  (pressure)
handle: 0x0017, char properties: 0x12, char value handle: 0x0018, uuid: 936b6a25-e503-4f7c-9349-bcc76c22b8c3  (light)
handle: 0x001b, char properties: 0x12, char value handle: 0x001c, uuid: 936b6a25-e503-4f7c-9349-bcc76c22b8c4  (noise)
"""

import time
import pygatt

adapter = pygatt.GATTToolBackend()
counter = 10

try:
    adapter.start()
    device = adapter.connect('93:89:C7:2D:5F:12')

    while counter > 0:
        #value = device.char_read("00002a6e-0000-1000-8000-00805f9b34fb")
        tValue = device.char_read_handle("0x000f")
        hValue = device.char_read_handle("0x0012")
        pValue = device.char_read_handle("0x0015")
        lValue = device.char_read_handle("0x0018")
        nValue = device.char_read_handle("0x001c")


        temp = (tValue[1] * 256 + tValue[0]) / 100
        humi = (hValue[1] * 256 + hValue[0]) / 100
        baro = (pValue[2] * 256 * 256 + pValue[1] * 256 + pValue[0]) / 10
        light = (lValue[1] * 256 + lValue[0]) / 100
        noise = (nValue[1] * 256 + nValue[0]) / 100

        print("[{:0>2d}] temp : {:.2f} 'C".format(counter, temp))
        print("[{:0>2d}] humi : {:.2f} % ".format(counter, humi))
        print("[{:0>2d}] baro : {:.2f} Pa".format(counter, baro))
        print("[{:0>2d}] light: {:.2f}   ".format(counter, light))
        print("[{:0>2d}] noise: {:.2f} dB".format(counter, noise))

        time.sleep(3)
        counter -= 1

finally:
    print("end")
    adapter.stop()

