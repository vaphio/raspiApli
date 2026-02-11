# Clock display application
# using tm1630.py
# for osl40391 4dig+colon LED
# set 5dig mode osl40391 4dig LED + colon

from tm1630 import TM1630
from time import sleep, localtime

dio = 21
clk = 20
stb = 19
ndig = 5

class Clock:
    def __init__(self, tm_instance):
        self.tm = tm_instance
        self.show_colon = False

    def getNumList(self, num):
        dig = []
        buf = num
        for i in range(4):
            bnum = 10**(3-i)
            dig.append(buf // bnum)
            buf = buf % bnum
        return dig

    def run(self):
        while True:
            t = localtime()
            hm = t.tm_hour*100+t.tm_min
            tl = self.getNumList(hm)
            self.show_colon = not self.show_colon
            for i in range(4):
                self.tm.disp_num(tl[i], i+1, False)
            self.colon(self.show_colon)
            sleep(1)

    def colon(self, isshow=False):
        if isshow:
            self.tm.setDig(0x06, 5)
        else:
            self.tm.setDig(0x00, 5)

if __name__=='__main__':
    tm = TM1630(dio, clk, stb, ndig)
    tm._start(0x01, 0x44)
    tm.set_brightness(4)

    clock = Clock(tm)

    try:
        clock.run()

    except KeyboardInterrupt:
        tm.disp_num(8888,False)
        sleep(1)
        tm._stop()
        print("\nFinished")

