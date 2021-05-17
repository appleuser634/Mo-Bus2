from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

i2c = I2C(scl=Pin(4), sda=Pin(5))
oled = SSD1306_I2C(128, 64, i2c)

def boot_animation():

    for i in reversed(range(25,70)):
        oled.fill(0)
        oled.text('Mo-Bus!!', 35, i)
        oled.show()

    time.sleep(1)

    for i in reversed(range(-10,25)):
        oled.fill(0)
        oled.text('Mo-Bus!!', 35, i)
        oled.show()

    oled.fill(0)
    oled.show()
