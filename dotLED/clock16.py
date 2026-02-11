# Display current time using dotLEDs

from dotLEDsz import dotLed
import time

NUM = 'num_MS.txt'
UNI = 'tanni_MS.txt'

COM = 4
SIN1= 5
SIN2 = 6
CLK = 19
LATCH = 21
ENABL = 20

led = dotLed(COM, SIN1, SIN2, CLK, LATCH, ENABL)

fnum = led.readFile(NUM)        #0123456789
funi = led.readFile(UNI)        #年月時分秒

def getHNum(num):
    return fnum[num*8:num*8+8]

def getUnit(idx):
    return funi[idx*16:idx*16+16]

def getDate(fmt):
    sdate = time.strftime(fmt)
    res = []
    for i in range(len(sdate)):
        res = res + getHNum(int(sdate[i]))
    return res

# main

try:
    while True:
        yr = getDate('%Y')
        nen = getUnit(0)
        mon = getDate('%m')
        tuki = getUnit(1)
        dt = getDate('%d')
        hi = getUnit(2)
        date = yr + nen + mon + tuki + dt + hi

        hr = getDate('%H')
        ji = getUnit(3)
        mm = getDate('%M')
        fn = getUnit(4)
        sc = getDate('%S')
        by = getUnit(5)
        date = date + hr + ji + mm + fn + sc + by

        s1 = led.cutPattern(date, 0, 16)
        s2 = led.cutPattern(date, 16, 16)
        for i in range(len(date) - 32):
           s1 = led.cutPattern(date, i, 16)
           s2 = led.cutPattern(date, i+16, 16)
           led.dspLED(s1, s2, 3)
        led.dspLED(s1, s2, 50)
except KeyboardInterrupt:
    print("\nFinished")
    led.finish()

