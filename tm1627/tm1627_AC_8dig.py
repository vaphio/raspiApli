# MicroPython for Raspberry Pi Pico
# Need tm1627.py
# This program is used for anode common LED 8dig
# dig 

import tm1627
from time import sleep, sleep_ms, localtime
dio = 21
clk = 20
stb = 19
dig = 7
adr = 0xC0
mode = 0x03
led_dig = 8

led = tm1627.TM1627(dio, clk, stb, dig)

def changeCode(code):   # change 7bit x led_dig code to led_dig bit x 7dig code
    res = []
    for i in range(dig):
        b = ''
        for j in range(led_dig):
            b = b + code[j][dig-1-i]
        c = int(b, 2)
        res.append(c)
#    print(res)
    return res

def get_line_code(line, drct=1):   # drct:dirction of digit. left=-1, right=1
    res = []
    for i in range(len(line)):
        if drct==1:
            cbuf = led.get_alfa(line[i])
        else:
            cbuf = led.get_alfa(line[led_dig-1-i])
        res.append(f"{cbuf:07b}")   #make 7binary string
    return res

def disp_line(line, drct=1):
    if len(line)<led_dig:
        line = line+' '*(led_dig-len(line))
    
    org_code = get_line_code(line, drct)
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

def shiftLeft(msg, wt, drct=1):
    line = msg + ' '*(led_dig+1)
    for i in range(len(msg)+1):
        d = line[i:i+led_dig]
        disp_line(d, drct)
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
    msg = '12345678'
    disp_line(msg, 0)
    sleep(5)
    
    disp_blink(5, 200)
    sleep(1)
    
    for i in range(10):
        line = f"{i*11111111:08}"
        disp_line(line, 0)
        sleep_ms(400)
    sleep(1)
    
    n = 0
    for i in range(led_dig):
        n = n*10+(i+1)
        line = f"{n:8}"
        disp_line(line, 0)
        sleep_ms(400)
    sleep(1)
    
    msg = "ABCDEFGHIJKLMNOPQRSTUVWXYZ-_"
    shiftLeft(msg, 100, 0)
    
    tm = localtime()
    msg = f"{tm[0]-2000:02}-{tm[1]:02}-{tm[2]:02}"
    disp_line(msg, 0)
    sleep_ms(500)
    
    for i in range(1000):
        tm = localtime()
        msg = f"{tm[3]:02}_{tm[4]:02}_{tm[5]:02}"
        disp_line(msg, 0)
        sleep_ms(200)

except KeyboardInterrupt:
    pass
finally:
    pass

disp_line("FINISHED", 0)
sleep(2)
led._stop()   #finalize TM1627    
led._stop()
