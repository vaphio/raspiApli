# MicroPython for Raspberry Pi Pico
# Need tm1627.py

import tm1627
from time import sleep, sleep_ms
dio = 15
clk = 16
stb = 17
dig = 6

led = tm1627.TM1627(dio, clk, stb, dig)

def disp_line(line, dp):
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

led._start(0x02, 0x44)    #initialise TM1627, fix address mode
led.set_brightness(5)   # set brightness 0 ... 7
for i in range(dig):
    led.disp_num(i, i+1)
    sleep_ms(100)
sleep(1)

disp_blink(10, 200)

for i in range(dig):
    led.disp_blank(dig-i)
    sleep(0.4)

for i in range(100):
    sn = '{:6}'.format(i+123456)
    disp_line(sn, 4)
    sleep_ms(10)
sleep(1)
msg = 'HELLO-'
disp_line(msg, 6)
sleep(5)

led._stop()   #finalize TM1627