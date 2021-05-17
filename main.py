from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

import boot_display
import network_setting

i2c = I2C(scl=Pin(4), sda=Pin(5))
oled = SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.show()

boot_display.boot_animation()
network_setting.connect_network('HUMAX-E938C','MmdhdGR3LThFM')
