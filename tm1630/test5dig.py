# using tm1630.py
# set 5dig mode osl40391 4dig LED + colon

import tm1630
from time import sleep

dio = 21
clk = 20
stb = 19
ndig = 5

led = tm1630.TM1630(dio, clk, stb, ndig)
led._start(0x01, 0x44)  #5dig 7seg mode, fixed address mode
led.set_brightness(4)   #set brightness 11/16

base = 10

def getNumList(num, base):
    dig = []
    buf = num
    for i in range(4):
        bnum = base ** (3 - i)
        dig.append(buf // bnum)
        buf = buf % bnum
    return dig

def dispList(dig, ndot=0):
    for i in range(len(dig)):
        led.disp_num(dig[i], i+1)

count = 100
stnum = 1234
wait = 0.02
try:
    for i in range(count):
        dl = getNumList(i+stnum, base)
        dispList(dl, 2)
        sleep(wait)
    sleep(1)
    led.setDig(0x08, 5)     #disp '
    sleep(1)
    led.setDig(0x06, 5)     #disp colon
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
