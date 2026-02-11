# TM1630 controll with MicroPython for Raspberry Pi
# modified fromTM1637 routine

__version__ = "1.0"    #

from gpiozero import LED
from time import sleep

DELAY = 0.0001        # 10us delay between clk/dio pulses

_null = 0x00
_num=(0x7E, 0x0C, 0xB6, 0x9E, 0xCC, 0xDA, 0xFA, 0x0E, 0xFE, 0xDE, 0xEE, 0xF8, 0x72, 0xBC, 0xF2, 0xE2)
_alfa = {'A':0x77, 'B':0x7C, 'C':0x39, 'D':0x5E, 'E':0x79, 'F':0x71, 'G':0x3D,
         'H':0x76, 'I':0x19, 'J':0x0E, 'L':0x38, 'N':0x54, 'O':0x5C, 'P':0x73, 'Q':0x67,
         'R':0x50, 'S':0x6D, 'T':0x78, 'U':0x3E, 'Y':0x6E, 'Z':0x1B, '-':0x40, '_':0x08}
_rot=(0x38, 0xB0, 0xA8, 0x98)
_adr = 0xC0
_error_msg = "parameter is out of range."

class TM1630(object):
    def __init__(self, dio, clk, stb, ndig):
        self.dio = LED(dio, initial_value=False)
        self.clk = LED(clk, initial_value=False)
        self.stb = LED(stb, initial_value=False)
        self.ndig = ndig    #num of digit
    
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
        self._stbL()
        for i in range(8):
            b = (data >> i) & 1
            if b==1:
                self.dio.on()
            else:
                self.dio.off()
            self._clkL()
            self._clkH()
        self._clkH()

    def sendData(self, code, adr):
        self.sendcmd(adr)
        self.sendcmd(code)
        self._stbH()
    
    def setDig(self, code, dig, dot=False):
        if not 0 < dig < self.ndig+1:
            raise ValueError("dig "+_error_msg)
        self.sendData(code, _adr+(dig-1)*2)
        if dot:
            self.set_dot(dig)
        else:
            self.out_dot(dig)

    def _start(self, conf=0x00, mode=0x44): #default of mode is fix address
        self.clk.on()
        sleep(DELAY)
        self.stb.on()
        sleep(DELAY)
        self.dio.off()
        self.sendcmd(conf)    # LED config 0x00:4dig8seg/0x01:5dig7seg
        self.stb.on()
        sleep(DELAY)
        self.sendcmd(mode)  #Only 0x44 is valid
        self._stbH()
        self.clearAll()
    
    def _stop(self):
        self.light_out()
        self._stbL()
        self._clkL()
        self.dio.off()

    def disp_blank(self, dig):
        self.setDig(_null, dig, False)

    def disp_num(self, num, dig, dot=False):
        ncode = self.get_code(num)
        self.setDig(ncode, dig, dot)
    
    def set_dot(self, dpos=0):
        self.sendData(0x20, _adr + 1 + dpos * 2)

    def out_dot(self, dpos=0):
        self.sendData(0x00, _adr + 1 + dpos * 2)

    def disp_alfa(self, alfa, dig, dot=False):
        code = self.get_alfa(alfa)
        if dot:
            code = code | 0x80
        self.setDig(code, dig)

    def set_brightness(self, brt):
        if not 0 <= brt <= 7:
            raise ValueError("Brightness "+_error_msg)
        self.sendcmd(0x88 | brt)
        self._stbH()

    def light_out(self):
        self.sendcmd(0x80)
        self._stbH()

    def clearAll(self):
        for i in range(self.ndig):
            self.disp_blank(i+1)

    def disp_rot(self, dig, tm, wt):
        if not 0 < dig < self.ndig+1:
            raise ValueError("dig "+_error_msg)
        for i in range(tm):
            self.setDig(_rot[i % 4], dig)
            sleep(wt/1000)
        self.disp_blank(dig)

if __name__ == '__main__':
    print("== start ==")
    dio = 21
    clk = 20
    stb = 19
    dig = 4
    led = TM1630(dio, clk, stb, dig)
    led._start(0x00, 0x44)   #use 4grid 8seg, fixed address mode
    led.set_brightness(4)
    for i in range(dig):
        led.disp_num(i, i+1)
        sleep(0.1)
    sleep(3)
    for i in range(4):
        led.set_dot(i)
        sleep(0.2)
        led.out_dot(i)
        sleep(0.1)
    sleep(2)
    led._stop()
    
