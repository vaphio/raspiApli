# MicroPython for Raspberry Pi Pico
# Need tm1627.py
# This program is used for anode common LED

import tm1627
from time import sleep, sleep_ms, localtime
dio = 21
clk = 20
stb = 19
dig = 7
adr = 0xC0
mode = 0x03
led_dig = 4

led = tm1627.TM1627(dio, clk, stb, dig)

def changeCode(code):   # change 7bit x led_dig code to led_dig bit x 7dig code
    res = []
    for i in range(dig):
        b = ''
        for j in range(led_dig):
            b = b + code[j][dig-1-i]
        c = int(b, 2)
        res.append(c)
    return res

def get_line_code(line):
    res = []
    for i in range(len(line)):
        cbuf = led.get_alfa(line[i])
        res.append(f"{cbuf:07b}")   #make 7binary string
    return res

def disp_line(line):
    org_code = get_line_code(line)
    chg_code = changeCode(org_code)
    for i in range(dig):
        led.sendData(chg_code[i], adr+i*2)

def disp_blink(num, tm):
    for i in range(num):
        led.light_out()
        sleep_ms(tm)
        led.set_brightness(7)
        sleep_ms(tm)

def num(dig, num):
    nc = led.get_code(num)
    bn = '{:08b}'.format(nc)
    for i in range(7):
        if bn[7-i]=='1':
            led.sendData(2**(dig-1), 0xC0+i*2)
        else:
            led.sendData(0x00, 0xC0+i*2)

def shiftLeft(msg, wt):
    line = msg + ' '*(dig+1)
    for i in range(len(msg)+1):
        d = line[i:i+dig]
        disp_line(d)
        sleep_ms(wt)

def prnBin(code, bn):
    for i in range(len(code)):
        fmt = "{:0"+str(bn)+"b}"
        print(fmt.format(code[i]), end=", ")
    print('')

# === Main ===

led._start(mode, 0x44)    #initialise TM1627, fix address mode
led.set_brightness(7)   # set brightness 0 ... 7

try:
    msg = '1234'
    disp_line(msg)
    sleep(1)
    
    disp_blink(5, 200)
    sleep(1)
    
    for i in range(100):
        line = f"{i:04}"
        disp_line(line)
        sleep_ms(20)
    sleep(1)
    
    msg = "ABCDEFGHIJKLMNOPQRSTUVWXYZ-_"
    shiftLeft(msg, 400)
    
    for i in range(3):
        tm = localtime()
        msg = f"{tm[0]:04}-{tm[1]:02}-{tm[2]:02}"
        msg = msg+"  "+f"{tm[3]:02}_{tm[4]:02}_{tm[5]:02}"
        shiftLeft(msg, 200)
    
finally:
    sleep(1)

    led._stop()   #finalize TM1627