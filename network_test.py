import network
import time
import socket
import _thread
import re
from machine import Pin

def do_connect(ssid,password):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid,password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def ledLoop():
    led = Pin(13, Pin.OUT)
    while True:
        led.value(not led.value())
        time.sleep(LedDelaySec)

do_connect('HUMAX-E938C','MmdhdGR3LThFM')

LedDelaySec = 1.0
led = Pin(13, Pin.OUT)
#_thread.start_new_thread(ledLoop, ())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80)) # host,port
s.listen(5) # backlog

while True:
    conn, addr = s.accept()
    request = str(conn.recv(1024)).lower()
    print("request : "+  request)
    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    if led_on == 6:
        print('LED ON')
        led.value(1)
    elif led_off == 6:
        print('LED OFF')
        led.value(0)
    conn.send('HTTP/1.1 200 OK')
    conn.close()
