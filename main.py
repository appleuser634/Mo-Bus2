from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from machine import Pin
import time
import sys
import urequests
import ujson

import boot_display
import network_setting

i2c = I2C(scl=Pin(4), sda=Pin(5))
oled = SSD1306_I2C(128, 64, i2c)

s1 = Pin(22, Pin.IN, Pin.PULL_UP)
s2 = Pin(23, Pin.IN, Pin.PULL_UP)

oled.fill(0)
oled.show()

boot_display.boot_animation()
try:
    network_setting.connect_network('HUMAX-E938C','MmdhdGR3LThFM')
except OSError:
    sys.exit()

def encode_morse(morse):

    morse_list = {"._":"A","_...":"B","_._.":"C","_..":"D",".":"E",".._.":"F",\
                "__.":"G","....":"H","..":"I",".___":"J","_._":"K","._..":"L",\
                "__":"M","_.":"N","___":"O",".__.":"P","__._":"Q","._.":"R",\
                "...":"S","_":"T",".._":"U","..._":"V",".__":"W","_.._":"X",\
                "_.__":"Y","__..":"Z","...._.":"!","......":"?","_.....":"(",\
                "__....":")","___...":":",".____":"1","..___":"2","...__":"3",\
                "...._":"4",".....":"5","_....":"6","__...":"7","___..":"8",\
                "____.":"9","_____":"0","____":"del","...._.":"!","..__..":"?","_.__.":"(","_.__._":")","___...":":"}
    try:
        return morse_list[morse]
    except KeyError:
        return ""

def send_message(message):
    url = 'http://192.168.0.167:8000/api/messages/'
    powerdata = { 
        "fromUser" : 5,
        "toUser": 8,
        "message" : message
        }

    header = {'Content-Type' : 'application/json'}

    res = urequests.post(
        url,
		data = ujson.dumps(powerdata).encode("utf-8"),
		headers = header
	)

    print(res.json())
    res.close()

def send_animation():
    
    for i in range(3):
        oled.fill(0)
        pled.show()

        time.sleep(0.5)

        oled.text("Sending...",60,20)
        oled.show()

    oled.fill(0)
    oled.show()

def type_message():
 
    pressing_flag = False
    p_start = time.ticks_ms()
    p_end = time.ticks_ms()
    temp_text = ""
    show_text = ""
    while True:
        oled.fill(0)
        
        if s1.value() == 0 and pressing_flag == False:
            p_start = time.ticks_ms()
            pressing_flag = True
            print("PUSH!")
        elif s1.value() == 1 and pressing_flag == True:
            pressing_time = time.ticks_diff(time.ticks_ms(), p_start)
            p_end = time.ticks_ms()    
            pressing_flag = False
            print("No Push!")
            print("Pressing Time:",pressing_time)
            if pressing_time > 200:
                temp_text += "_"
            else:
                temp_text += "."

        release_time = time.ticks_diff(time.ticks_ms(), p_end)
        if release_time > 800:
            show_text += encode_morse(temp_text)
            temp_text = ""

        oled.text(show_text,10,10)
        oled.show()

        if s2.value() == 0:
            send_message(show_text)
            show_text = ""

def main():
    type_message()

if __name__ == "__main__":
    main()
