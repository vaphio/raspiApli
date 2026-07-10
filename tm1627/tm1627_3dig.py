# MicroPython for Raspberry Pi Pico
# using TM1627 for 3seg OSL30391

import tm1627
from time import sleep, sleep_ms

dio = 15
clk = 16
stb = 17
dig = 4

led = tm1627.TM1627(dio, clk, stb, dig)
led._start(0x02)
led.set_brightness(5)

dnum = [4, 3, 2, 1]

def disp_line(line, dp):
    for i in range(dig-1):
        code = line[i]
        if i == dp-1:
            dot = 1
        else:
            dot = 0
        led.disp_alfa(code, dnum[i], dot)

num = '123'
disp_line(num, 4)
for i in range(10):
    led.setDig(0x03, dnum[3])
    sleep(0.5)
    led.setDig(0x00, dnum[3])
    sleep(0.3)
sleep(2)
num = '25C'
disp_line(num, 4)
led.setDig(0x04, dnum[3])

sleep(5)

led._stop()