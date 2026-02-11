# using tm1630.py

import tm1630
from time import sleep

dio = 21
clk = 20
stb = 19
ndig = 4

led = tm1630.TM1630(dio, clk, stb, ndig)
led._start(0x00, 0x44)  #4dig 8seg mode, fixed address mode
led.set_brightness(4)   #set brightness 11/16

base = 10

def getNumList(num, base):
    dig = []
    buf = num
    for i in range(ndig):
        bnum = base ** (ndig - i -1)
        dig.append(buf // bnum)
        buf = buf % bnum
    return dig

def dispList(dig, ndot=0):
    for i in range(ndig):
        if ndot==i:
            led.disp_num(dig[i], i+1, True)
        else:
            led.disp_num(dig[i], i+1, False)

count = 100
stnum = 1234
wait = 0.02
try:
    for i in range(count):
        dl = getNumList(i+stnum, base)
        dispList(dl, 2)
        sleep(wait)
    sleep(1)
    base = 16
    for i in range(count):
        dl = getNumList(i+stnum, base)
        dispList(dl)
        sleep(wait)

    sleep(2)
    led._stop()
except KeyboardInterrupt:
    led._stop()

print("\nStop")
