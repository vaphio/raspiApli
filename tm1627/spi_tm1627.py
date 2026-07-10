# TM1627 controll for Raspberry Pi
# using spidev for controlling SPI

__version__ = "1.0"    #spi version

from gpiozero import LED
import spidev
from time import sleep

DELAY = 0.0001        # 10us delay between clk/dio pulses

_null = 0x00
_num  = (0x3F, 0x6, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x27, 0x7F, 0x6F)
_alfa = {'A':0x77, 'B':0x7C, 'C':0x39, 'D':0x5E, 'E':0x79, 'F':0x71, 'G':0x3D,
         'H':0x76, 'I':0x19, 'J':0x0E, 'L':0x38, 'N':0x54, 'O':0x5C, 'P':0x73, 'Q':0x67,
         'R':0x50, 'S':0x6D, 'T':0x78, 'U':0x3E, 'Y':0x6E, 'Z':0x1B, '-':0x40, '_':0x08}
_rot = (0x4C, 0x1C, 0x58, 0x54)
_adr = 0xC0
_error_msg = "parameter is out of range."

class TM1627(object):
    def __init__(self, ndig):
#    def __init__(self, dio, clk, stb, ndig):
#        self.dio = LED(dio, initial_value=False)
#        self.clk = LED(clk, initial_value=False)
#        self.stb = LED(stb, initial_value=False)
        self.ndig = ndig
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 3
    
    def _wait(self):
        sleep(DELAY)

    def _stbH(self):
        self.stb.on()
        self._wait()

    def _stbL(self):
        self.stb.off()
        self._wait()

    def _clkH(self):
        self.clk.on()
        self._wait()

    def _clkL(self):
        self.clk.off()
        self._wait()

    def get_code(self, num):
        return _num[num]
    
    def get_alfa(self, alfa):
        if 47 < ord(alfa) < 59:
            res = self.get_code(int(alfa))
        else:
            res = _alfa.get(alfa, 0x00)
        return res
    
    def sendcmd(self, data):
#        self._stbL()
#        for i in range(8):
#            b = (data >> i) & 1
#            if b==1:
#                self.dio.on()
#            else:
#                self.dio.off()
#            self._clkL()
#            self._clkH()
#        self._clkH()
        self.spi.xfer([data])

    def sendData(self, code, adr):
        self.sendcmd(adr)
        self.sendcmd(code)
#        self._stbH()
    
    def setDig(self, code, dig):
        if not 0 < dig < self.ndig+1:
            raise ValueError("dig "+_error_msg)
        self.sendData(code, _adr+(dig-1)*2)
        self.sendData(0x00, _adr+(dig-1)*2+1)

    def _start(self, conf=0x03, mode=0x44):   #default of mode is fix address
#        self.clk.on()
#        sleep(DELAY)
#        self.stb.on()
#        sleep(DELAY)
#        self.dio.off()
        self.sendcmd(conf)    # LED config 0x00-0x03
#        self.stb.on()
#        sleep(DELAY)
        self.sendcmd(mode)
#        self._stbH()
        self.clearAll()
    
    def _stop(self):
        self.light_out()
#        self._stbL()
#        self._clkL()
#        self.dio.off()
        self.sendcmd(0x00)

    def disp_blank(self, dig):
        self.setDig(_null, dig)

    def disp_num(self, num, dig, dot=0):
        ncode = self.get_code(num) | (0x80 * dot)
        self.setDig(ncode, dig)
    
    def disp_alfa(self, alfa, dig, dot=0):
        code = self.get_alfa(alfa)
        if dot!=0:
            code = code | 0x80
        self.setDig(code, dig)

    def set_brightness(self, brt):
        if not 0 <= brt <= 7:
            raise ValueError("Brightness "+_error_msg)
        self.sendcmd(0x88 | brt)
#        self._stbH()

    def light_out(self):
        self.sendcmd(0x80)
#        self._stbH()

    def clearAll(self):
        for i in range(self.ndig):
            self.disp_blank(i+1)

    def disp_rot(self, dig, tm, wt):
        if not 0 < dig < self.ndig+1:
            raise ValueError("dig "+_error_msg)
        for i in range(tm):
            self.setDig(_rot[i % 4], dig)
            sleep_ms(wt)
        self.disp_blank(dig)

if __name__ == '__main__':
    print("== start ==")
#    dio = 21
#    clk = 20
#    stb = 19
    dig = 6
    led = TM1627(dig)
    led._start(0x02, 0x44)   #use 6grid 11seg, fixed address mode
    led.set_brightness(4)
    for i in range(dig):
        led.disp_num(i, i+1)
        sleep(0.1)
    sleep(3)
    led._stop()
    
