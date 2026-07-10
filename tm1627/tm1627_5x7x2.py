# MicroPython for Raspberry Pi Pico
# Need tm1627.py

import tm1627
import han4 as han
#import hankaku3 as han
from time import sleep, sleep_ms, localtime
dio = 15
clk = 16
stb = 17
dig = 7

led = tm1627.TM1627(dio, clk, stb, dig)
adr = 0xC0

def dispDot2(code1, code2):   #code1=right, code2=left
    alcode = []
    for i in range(dig):
        sb1 = '{:05b}'.format(code1[i])
        sb2 = '{:05b}'.format(code2[i])
        alcode.append(sb1+sb2)
    dispSCode(alcode)

def dispSCode(scode):    #scode is >=10bit x 7 str list
    for i in range(dig):
        dc1 = int(scode[i][2:10], 2)
        dc2 = int(scode[i][:2], 2)
        led.sendData(dc1, adr+i*2)
        led.sendData(dc2, adr+1+i*2)
        
def dispLine(strs, wt):
    code = appendStr(strs)
    dispSCode(code)
    sleep_ms(wt)

def shiftLine(strs, wt):
    if len(strs)<3:
        strs = strs+'  '
    for i in range(len(strs)-2):
        sb1 = han.getStrCode(strs[i])
        sb2 = han.getStrCode(strs[i+1])
        sb3 = han.getStrCode(strs[i+2])
        sall = appendCode(sb1, sb2, sb3)
        for j in range(5):
            dispSCode(sall)
            buf = []
            for k in range(dig):
                buf.append(sall[k][1:])
            sall = buf
            sleep_ms(wt)

def appendCode(code1, code2, code3):
    res = []
    for i in range(dig):
        sc1 = '{:05b}'.format(code1[i])
        sc2 = '{:05b}'.format(code2[i])
        sc3 = '{:05b}'.format(code3[i])
        sall = sc1+sc2+sc3
        res.append(sall)
    return res

def appendStr(s):    # return binary string list
    res = ['']*dig
    for i in range(len(s)):
        bcode = han.getStrCode(s[i])
        for j in range(dig):
            scode = '{:05b}'.format(bcode[j])
            res[j] = res[j]+scode
    return res

def disp_blink(num, tm):
    for i in range(num):
        led.light_out()
        sleep_ms(tm)
        led.set_brightness(7)
        sleep_ms(tm)

try:
    led._start(0x03, 0x44)    #initialise TM1627, 7grid 10seg fix address mode
    led.set_brightness(5)   # set brightness 0 ... 7

    for i in range(dig):
        led.disp_blank(dig)
#    sleep(0.4)

    for i in range(dig):
        n1 = 0b10101
        n2 = 0b01010
        scode1 = [n1, n2, n1, n2, n1, n2, n1]
        scode2 = [n2, n1, n2, n1, n2, n1, n2]
        dispDot2(scode2, scode1)
        sleep_ms(100)
    sleep(0.5)
    

    for i in range(100):
        snum = '{:02}'.format(i)
        dispLine(snum, 50)
    sleep(1)
    
    alfa = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    shiftLine(alfa, 20)
    sleep(0.5)

#    alfa = 'abcdefghijklmnopqrstuvwxyz*/+-[]^='
#    dispLine(alfa, 300)
#    sleep(2)
    for i in range(3):
        alfa = '   Hello, World!   '
        shiftLine(alfa, 10)
    sleep(2)
    
    for i in range(100):
        t = localtime()
        stm = '   {:02}/{:02}/{:02} {:02}:{:02}:{:02}   '.format(t[0],t[1],t[2],t[3],t[4],t[5])
        shiftLine(stm, 20)
    sleep(2)

finally:
    led._stop()   #finalize TM1627