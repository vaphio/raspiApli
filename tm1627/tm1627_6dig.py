# test app for Raspberry Pi 
# Need tm1627.py

import tm1627
from time import sleep
dio = 21
clk = 20
stb = 19
dig = 6

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
        sleep(tm)
        led.set_brightness(7)
        sleep(tm)

def shiftLeft(msg, wt):
    line = msg + ' '*(dig+1)
    for i in range(len(msg)+1):
        d = line[i:i+dig]
        disp_line(d)
        sleep(wt)

led._start(0x02, 0x44)    #initialise TM1627, fix address mode
led.set_brightness(5)   # set brightness 0 ... 7

for i in range(dig):
    led.disp_num(i, i+1)
    sleep(0.1)
sleep(1)

#disp_blink(10, 200)

for i in range(dig):
    led.disp_blank(dig-i)
    sleep(0.1)

msg = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123"
shiftLeft(msg, 0.3)

sleep(1)
msg = 'HELLO-'
disp_line(msg, 6)
sleep(1)
msg = 'ERROR_'
disp_line(msg)
sleep(1)

led.clearAll()

for i in range(dig):
    led.disp_rot(i+1, 10, 100)
sleep(1)
    
led._stop()   #finalize TM1627
