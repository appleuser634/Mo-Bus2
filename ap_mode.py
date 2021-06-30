import framebuf
import network
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import socket
import time

import gc
gc.enable()

i2c = I2C(scl=Pin(4), sda=Pin(5))
oled = SSD1306_I2C(128, 64, i2c)
 
def setup_ap(ssid,password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    
    print(ap.ifconfig())    
    return ap

def load_image(filename):
    with open(filename, 'rb') as f:
        f.readline()
        f.readline()
        f.readline()
        data = bytearray(f.read())
    return framebuf.FrameBuffer(data, 62, 62, framebuf.MONO_HLSB)

def gen_html():
    
    gpio_state = "OFF"

    html = """
    <html>
    <head> 
    <title>ESP32 ESPDuino-32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> 
    <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}
    </style>
    <script type="text/javascript">
        function button_click() {
            var target = document.getElementById("searchLink");
            const ssidTextbox = document.getElementById("ssid")
            const ssid = ssidTextbox.value
            const passwordTextbox = document.getElementById("password")
            const password = passwordTextbox.value
            target.href = "/?ssid="+ssid+"?password="+password;
        }
    </script>
    </head>
    <body> 
    <h1>mimoc</h1>
    <h1>Mo-bus2 Setting</h1>
    <p>SSID:<br>
    <input type="text" id="ssid" size="30"></p>
    <p>Password:<br>
    <input type="text" id="password" size="30"></p> 
    </p><p>
    <a id="searchLink" href="/?">
    <button class="button" onclick="button_click();">Send</button>
    </a>
    </p>
    </body>
    </html>
    """

    return html

def start():
    oled.fill(0)
    oled.show()
    
    ap = setup_ap("MB2","")

    image = load_image('wifi_qr.pbm')
    oled.blit(image, 35, 0)
    oled.show()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        
        request = request.decode()
        temp_param = request.split("HTTP")
        temp_param = temp_param[0].split("GET")
        temp_param = temp_param[1].split(" ")
        temp_param = temp_param[1]
        if temp_param == "/":
            print("Pass...")
        else:
            print("///////////////TEMP PARAM////////////////")
            print(temp_param)
            ssid = temp_param.split("?")[1].split("ssid=")[1]
            password = temp_param.split("?")[2].split("password=")[1]
            print("/////////////SSID////////////")
            print(ssid)
            print("///////////Password///////////")
            print(password)
            ap.active(False)
            break

        response = gen_html()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()    
