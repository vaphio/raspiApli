# using tm1630.py
# set 3dig mode 3dig LED + colon OSL30391

import tm1630
from time import sleep

dio = 22
clk = 27
stb = 17
ndig = 4

led = tm1630.TM1630(dio, clk, stb, ndig)
led._start(0x00, 0x44)  #5dig 7seg mode, fixed address mode
led.set_brightness(4)   #set brightness 11/16

base = 10

def getNumList(num, base, dsp_dig=ndig):
    dig = []
    buf = num
    for i in range(dsp_dig):
        bnum = base ** (dsp_dig - i - 1)
        dig.append(buf // bnum)
        buf = buf % bnum
    return dig

def dispList(dig):
    for i in range(len(dig)):
        led.disp_num(dig[i], ndig-i)
    led.disp_blank(1)

count = 20 * base
stnum = 123
wait = 0.02
try:
    dl = getNumList(stnum, base, 3)
    print(dl)
    led.disp_num(dl[0], 4, False)
    led.disp_num(dl[1], 3, True)
    led.disp_num(dl[2], 2, False)
    led.disp_blank(1)
    sleep(2)

    for i in range(count):
        dl = getNumList(i+stnum, base, 3)
        dispList(dl)
        sleep(wait)
    sleep(1)
    led.setDig(0x08, 1)     #disp '
    sleep(1)
    led.setDig(0x06, 1)     #disp colon
    sleep(2)

    base = 16
    count = 20 * base
    for i in range(count):
        dl = getNumList(i+stnum, base, 3)
        dispList(dl)
        sleep(wait)

    sleep(2)
    led._stop()
except KeyboardInterrupt:
    led._stop()

print("\nStop")
