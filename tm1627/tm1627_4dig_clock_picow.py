# MicroPython for Raspberry Pi Pico
# Need tm1627.py

import tm1627
import rtc1307
from machine import Pin, I2C
from time import sleep, sleep_ms, localtime
dio = 21
clk = 20
stb = 19
dig = 4
csda = 16
cscl = 17

led = tm1627.TM1627(dio, clk, stb, dig)
i2c = I2C(0, sda=Pin(csda), scl=Pin(cscl), freq=200000)
clk = rtc1307.RTC(i2c)
print(i2c.scan())

def disp_line(line, dp=0):
    for i in range(dig):
        code = line[i]
        if i == dp-1:
            dot = 1
        else:
            dot = 0
        led.disp_alfa(code, i+1, dot)

def disp_blink(num, tm):
    for i in range(num):
        led.light_out()
        sleep_ms(tm)
        led.set_brightness(7)
        sleep_ms(tm)

def shiftLeft(msg, wt):
    line = msg + ' '*(dig+1)
    for i in range(len(msg)+1):
        d = line[i:i+dig]
        disp_line(d)
        sleep_ms(wt)

def fmtDate(tm):
    return f"{tm[1]:02}{tm[2]:02}"

def fmtTime(tm):
    return f"{tm[3]:02}{tm[4]:02}"

led._start(0x02, 0x44)    #initialise TM1627, fix address mode
led.set_brightness(2)   # set brightness 0 ... 7


try:
    i = 0
    while True:
        lt = clk.getTime()
#        print(lt)
        tm = fmtTime(lt)
        if lt[5]>55:
            tm = f"{lt[5]:4}"
        
        if i < 3:
            disp_line(tm,2)
        else:
            disp_line(tm,0)
        i = (i + 1) % 6
        sleep_ms(300)
except KeyboardInterrupt:
    pass
    
led._stop()   #finalize TM1627