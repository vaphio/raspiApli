# MicroPython for Raspberry Pi Pico
# Need tm1627.py

import tm1627
import hankaku3
from time import sleep, sleep_ms
dio = 15
clk = 16
stb = 17
dig = 7

led = tm1627.TM1627(dio, clk, stb, dig)

def mkCode(str):
    code = []
    orgc = hankaku3.getStrCode(str)
    for i in range(len(orgc)):
        sorg = '{:05b}'.format(orgc[i])
        ncod = ''
        for j in range(5):
            ncod = ncod + sorg[4-j]
        code.append(int(ncod,2))
    return code

def dispDot(code):
    for i in range(dig):
        led.sendData(code[i], 0xC0+i*2)
        

def disp_blink(num, tm):
    for i in range(num):
        led.light_out()
        sleep_ms(tm)
        led.set_brightness(7)
        sleep_ms(tm)

led._start(0x03, 0x44)    #initialise TM1627, 7grid 10seg fix address mode
led.set_brightness(5)   # set brightness 0 ... 7

for i in range(dig):
    led.disp_blank(dig)
#    sleep(0.4)

for i in range(dig):
    led.sendData(0xff, 0xC0+i*2)
    sleep_ms(100)
sleep(1)

for i in range(10):
    scode = mkCode(str(i))
    dispDot(scode)
    sleep_ms(500)
sleep(1)    
alfa = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for i in range(len(alfa)):
    scode = mkCode(alfa[i])
    dispDot(scode)
    sleep_ms(500)
sleep(1)

alfa = 'abcdefghijklmnopqrstuvwxyz*/+-[]^='
for i in range(len(alfa)):
    scode = mkCode(alfa[i])
    dispDot(scode)
    sleep_ms(400)
sleep(2)

led._stop()   #finalize TM1627