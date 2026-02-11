# 32 x 16 dot matrix LED
# minimum routine for just disp pattern
# using gpiozero instead of RPi.GPIO to be able to use pi5

from gpiozero import LED
from time import sleep
import sys

COM = 4
SIN1= 5
SIN2 = 6
CLK = 19
LATCH = 21
ENABL = 20

WTIME = 2

class dotLed:
    def __init__(self, com, sin1, sin2, clk, latch, enable, itv=0.000001):
        self.com = LED(com, initial_value = False)
        self.sin1 = LED(sin1, initial_value = False)
        self.sin2 = LED(sin2, initial_value = False)
        self.clk  = LED(clk)
        self.latch = LED(latch)
        self.enable = LED(enable)
        self.itv = itv

        self.pins = [self.com, self.sin1, self.sin2, self.clk, self.latch, self.enable]

    def shift(self, data, sft):
        return (data >> sft) & 0x0001

    def set_data(self, dig1, dig2):
        self.enable.off()
        self.latch.off()
        self.clk.off()
        for i in range(len(dig1)):
            sel = 0x0001 << i
            for j in range(16):
                self.clk.off()
                com = (sel >> j) & 0x0001
                sg1 = int(dig1[i][15-j])
                sg2 = int(dig2[i][15-j])
                self.com.value = com
                self.sin1.value = sg1
                self.sin2.value = sg2
                self.clk.on()
                sleep(self.itv)
            self.clk.on()
#            sleep(self.itv)
            self.latch.on()
#            sleep(self.itv)
            self.clk.off()
#            sleep(self.itv)
            self.latch.off()

    def dspLED(self, code1, code2, wtime=10):
        for i in range(wtime):
            self.set_data(code1, code2)

    def finish(self):
        for pin in self.pins:
            pin.off()

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
    
    def cutPattern(self, data, idx, wsize=16):
        buf = data[idx:idx+wsize]
        result = []
        for i in range(16):
            hol = []
            for j in range(wsize):
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
            led.dspLED(s1, s2, 10)
            for i in range(len(data)-32):
                s1 = led.cutPattern(data, i)
                s2 = led.cutPattern(data, i+16)
                led.dspLED(s1, s2, 3)
            led.dspLED(s1,s2,50)
    
    except KeyboardInterrupt:
        print("\nFinished")
