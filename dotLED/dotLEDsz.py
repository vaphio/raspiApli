# 32 x 16 dot matrix LED
# minimum routine for just disp pattern
# using gpiozero instead of RPi.GPIO to be able to use pi5

import RPi.GPIO as GPIO
from time import sleep
import sys

COM = 4
SIN1= 5
SIN2 = 6
CLK = 19
LATCH = 21
ENABL = 20

WTIME = 2
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class dotLed:
    def __init__(self, com, sin1, sin2, clk, latch, enable, itv=0.000001):
        self.com = com
        self.sin1 = sin1
        self.sin2 = sin2
        self.clk  = clk
        self.latch = latch
        self.enable = enable
        self.itv = itv

        self.pins = [self.com, self.sin1, self.sin2, self.clk, self.latch, self.enable]
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def shift(self, data, sft):
        return (data >> sft) & 0x0001

    def set_data(self, dig1, dig2):
        GPIO.output(self.enable, 0)
        GPIO.output(self.latch, 0)
        GPIO.output(self.clk, 0)
        for i in range(len(dig1)):
            sel = 0x0001 << i
            for j in range(16):
                GPIO.output(self.clk, 0)
                com = (sel >> j) & 0x0001
                sg1 = int(dig1[i][15-j])
                sg2 = int(dig2[i][15-j])
                GPIO.output(self.com, com)
                GPIO.output(self.sin1, sg1)
                GPIO.output(self.sin2, sg2)
                GPIO.output(self.clk, 1)
                sleep(self.itv)
            GPIO.output(self.clk, 1)
            sleep(self.itv)
            GPIO.output(self.latch, 1)
            sleep(self.itv)
            GPIO.output(self.clk, 0)
            sleep(self.itv)
            GPIO.output(self.latch, 0)

    def dspLED(self, code1, code2, wtime=10):
        for i in range(wtime):
            self.set_data(code1, code2)

    def finish(self):
        GPIO.cleanup()

    def readFile(self, fn):
        print(fn)
        
        f = open(fn, 'r')
        result = []
        for line in f:
            line = line.rstrip()    # remove \n
            b = line.split(',')
            result.append(b)
        f.close()
        return result
    
    def cutPattern(self, data, idx, sl=16):
        buf = data[idx:idx+sl]
        result = []
        for i in range(16):
            hol = []
            for j in range(sl):
                hol.append(buf[j][i])
            result.append(hol)
        return result
    
    def prnPattern(self, data):
        buf = ''
        for i in range(16):
            for j in range(16):
                d1 = data[i][j]
                if d1 == '0':
                    buf = buf + '.'
                else:
                    buf = buf + '*'
            buf = buf + "\n"
        print(buf)

# main
if __name__ == "__main__":

    fname = sys.argv[1]

    led = dotLed(COM, SIN1, SIN2, CLK, LATCH, ENABL)
    data = []
    data = led.readFile(fname)
    
    try:
        while True:
            s1 = led.cutPattern(data, 0)
            s2 = led.cutPattern(data, 16)
            led.dspLED(s1, s2, 5)
            for i in range(len(data)-32):
                s1 = led.cutPattern(data, i)
                s2 = led.cutPattern(data, i+16)
                led.dspLED(s1, s2, 3)
            led.dspLED(s1,s2,50)
    
    except KeyboardInterrupt:
        led.finish()
        print("\nFinished")
