# MicroPython for Raspberry Pi Pico
# using tm1627.py

import tm1627
from time import localtime, sleep, sleep_ms

dio = 15
clk = 16
stb = 17
dig = 4
dnum = [4, 3, 2, 1]

led = tm1627.TM1627(dio, clk, stb, dig)
#print(localtime())

led._start(0x02, 0x44)
led.set_brightness(7)

def fmtTime(tm):
    hr = '{:1}'.format(tm[3] % 12)
    min = '{:02}'.format(tm[4])
#    sec = '{:02}'.format(tm[5])
    return hr+min

def disp_line(line, dp):
    for i in range(dig-1):
        code = line[i]
        if i == dp-1:
            dot = 1
        else:
            dot = 0
        led.disp_alfa(code, dnum[i], dot)

try:
    c = 0
    while True:
        t = localtime()
        hm = fmtTime(t)
        sc = ' {:02}'.format(t[5])
        if int(sc)>55:
            disp_line(sc, 7)
        else:
            disp_line(hm, 7)
        c = (c+1) % 10
        if c > 5:
            led.setDig(0x03, 1)
        else:
            led.setDig(0x00, 1)
        sleep_ms(100)

except KeyboardInterrupt:
    led._stop()