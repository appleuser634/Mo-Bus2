import network
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

i2c = I2C(scl=Pin(4), sda=Pin(5))
oled = SSD1306_I2C(128, 64, i2c)

def loop_animation(loading_charas,times):
    for _ in range(times):
        for l in loading_charas:
            oled.fill(0)
            display_string = "Connecting " + l
            oled.text(display_string, 20, 30)
            oled.show()

def connect_network(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    loading_charas = ['\\','|','/','-']
    loop_animation(loading_charas,10)

    while not wlan.isconnected():
        wlan.connect(ssid, password)
        loop_animation(loading_charas,4)

    oled.fill(0)
    oled.text("ON LINE!!", 30, 30)
    oled.show()

    time.sleep(2)

    oled.fill(0)
    oled.show()
    print('network config:', wlan.ifconfig())
