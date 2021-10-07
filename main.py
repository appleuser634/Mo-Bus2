from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
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
                "____.":"9","_____":"0","...._.":"!","..__..":"?","_.__.":"(","_.__._":")","___...":":","........":"del"}
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

    send_animation()

def send_animation():
    
    for i in range(3):
        oled.fill(0)
        oled.show()

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
    
    buzzer = PWM(Pin(17), freq=0, duty=512)
    buzzer.deinit()             
    
    while True:
        oled.fill(0)
        
        if s1.value() == 0 and pressing_flag == False:
            p_start = time.ticks_ms()
            pressing_flag = True
            print("PUSH!")
            buzzer = PWM(Pin(17), freq=1600, duty=512) 
        elif s1.value() == 1 and pressing_flag == True:
            pressing_time = time.ticks_diff(time.ticks_ms(), p_start)
            p_end = time.ticks_ms()    
            pressing_flag = False
            buzzer.deinit()
            print("No Push!")
            print("Pressing Time:",pressing_time)
            if pressing_time > 200:
                temp_text += "_"
            else:
                temp_text += "."

        release_time = time.ticks_diff(time.ticks_ms(), p_end)
        if release_time > 800:
            if encode_morse(temp_text) == "del":
                show_text = show_text[:-1]
            else:
                show_text += encode_morse(temp_text)
            temp_text = ""

        oled.text(show_text,10,10)
        oled.show()

        if s2.value() == 0:
            send_message(show_text)
            show_text = ""

def mode_menu():
    
    mode_list = {"Internet":(10,10),"Local":(10,20),"Plactice":(10,30)}
    menu_index = 0

    while True:
        oled.fill(0)
        for i, mode in enumerate(mode_list):
            x = mode_list[mode][0]
            y = mode_list[mode][1]
            if i == 0: 
                oled.fill_rect(0, 9, 128, 10, 1)
                oled.text(mode, x, y, 0) 
            else:
                oled.text(mode,x,y)
        oled.show()


def main():
    mode_menu()
    type_message()

if __name__ == "__main__":
    main()
