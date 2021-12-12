import network
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import sys

class network_setting():
    
    def __init__(self,oled):
        self.oled = oled

    def loop_animation(self,loading_charas,times):
        for _ in range(times):
            for l in loading_charas:
                self.oled.fill(0)
                display_string = "Connecting " + l
                self.oled.text(display_string, 20, 30)
                self.oled.show()

    def connect_network(self,ssid, password):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        loading_charas = ['\\','|','/','-']
        self.loop_animation(loading_charas,10)

        while not wlan.isconnected():
            try:
                wlan.connect(ssid, password)
                self.loop_animation(loading_charas,4)
            except Exception as e:
                sys.print_exception(e) 

        self.oled.fill(0)
        self.oled.text("ON LINE!!", 30, 30)
        self.oled.show()

        time.sleep(2)

        self.oled.fill(0)
        self.oled.show()
        print('network config:', wlan.ifconfig())
