# MicroPython for Raspberry Pi Pico
# Need tm1627.py

import tm1627
from time import sleep, sleep_ms, localtime
dio = 15
clk = 16
stb = 17
dig = 4

led = tm1627.TM1627(dio, clk, stb, dig)

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
led.set_brightness(5)   # set brightness 0 ... 7

for i in range(dig):
    led.disp_num(i, i+1)
    sleep_ms(30)
sleep(1)

#disp_blink(10, 200)

for i in range(dig):
    led.disp_blank(dig-i)
    sleep(0.1)

led.clearAll()

for i in range(100):
    tm = localtime()
    if 0 < i%6 < 3:
        disp_line(fmtTime(tm),2)
    else:
        disp_line(fmtTime(tm),0)
    if tm[5]>50:
        disp_line(f"{tm[5]:4}",2)
    sleep_ms(300)
    
led._stop()   #finalize TM1627