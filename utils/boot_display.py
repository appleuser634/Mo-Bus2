from machine import Pin, I2C, PWM
import time

from utils import ap_mode

class boot():
    
    buzzer = PWM(Pin(17), freq=1600, duty=512)
    time.sleep(0.1)
    buzzer.deinit()
    time.sleep(0.05)

    buzzer = PWM(Pin(17), freq=1000, duty=512)
    time.sleep(0.1)
    buzzer.deinit()
    time.sleep(0.1)

    
    def boot_animation(self,switchs,oled):

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
        
        if switchs.s1.value() == 0:
            ap_mode.start()
