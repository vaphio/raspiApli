# 32 x 16 dot matrix LED
# Using hankaku2.py which has 5x7dot charactors
# each char has 8x8dot but reduce 6x8dot
# ver.3.0 using bit map as strings

import RPi.GPIO as GPIO
import time
import hankaku2 as han      # 6 x 8 dot fonts

SIN1 = 4
SIN2 = 5
SIN3 = 6
CLK = 19
LATCH = 21
ENABL = 20

WTIME = 5
MSG1 = '1234567890'
MSG2 = 'ABCDEFGHIJKLM'

FMT_DATE = '%m/%d'
FMT_TIME1 = '%H:%M' # : shows
FMT_TIME2 = '%H %M' # no colon
MAX_DOT = 32

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class dotLed:
    def __init__(self, sin1, sin2, sin3, clk, latch, enable, itv=0.00001):
        self.sin1 = sin1
        self.sin2 = sin2
        self.sin3 = sin3
        self.clk  = clk
        self.latch = latch
        self.enable = enable
        self.itv = itv

        pins = [self.sin1, self.sin2, self.sin3, self.clk, self.latch, self.enable]
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def shift(self, data, sft):
        return (data >> sft) & 0x0001

    def set_data(self, dig1, dig2):
        GPIO.output(self.enable, GPIO.LOW)
        GPIO.output(self.latch, GPIO.LOW)
        GPIO.output(self.clk, GPIO.LOW)
        for i in range(len(dig1)):
            sel = 0x0001 << i
            for j in range(16):
                GPIO.output(self.clk, GPIO.LOW)
                com = (sel >> j) & 0x0001
                sg1 = int(dig1[i][15-j])
                sg2 = int(dig2[i][15-j])
                GPIO.output(self.sin1, com)
                GPIO.output(self.sin2, sg1)
                GPIO.output(self.sin3, sg2)
                GPIO.output(self.clk, GPIO.HIGH)
                time.sleep(self.itv)
            GPIO.output(self.clk, GPIO.HIGH)
            time.sleep(self.itv)
            GPIO.output(self.latch, GPIO.HIGH)
            time.sleep(self.itv)
            GPIO.output(self.clk, GPIO.LOW)
            time.sleep(self.itv)
            GPIO.output(self.latch, GPIO.LOW)

    def dspLED(self, code1, code2, wtime=10):
        for i in range(wtime):
            self.set_data(code1, code2)

    def dev_digit(self, code):
        dig1 = []
        dig2 = []
        result = []
        for s in code:
            ls = len(s)
            if ls<32:
                s = s+'0'*(32-ls)
            dig1.append(s[:16])
            dig2.append(s[16:32])
        result.append(dig1)
        result.append(dig2)
        return result
        
    def offSet(self, code):
        result = []
        diff = len(code[0])%32
        if diff != 0:
            for s in code:
                buf = s+'0'*(32-diff)
                result.append(buf)
        else:
            result = code
        return result

    def sumLines(self, code1, code2):
        result = []
        difCode = len(code1) - len(code2)
        filCode = ['0'*len(code1[0][0])]*len(code1[0])
        if difCode > 0:
            code2 = code2 + [filCode]*difCode
        elif difCode < 0:
            code1 = code1 + [filCode]*abs(difCode)
        for i in range(len(code1)):
            result.append(code1[i]+code2[i])
        return result
            
    def prnCode(self, code):
        for c in code:
            buf = ''
            for s in c:
                if s == '0':
                    s = '.'
                buf += s
            print(buf)

    def mkMsgCode(self, msg):
        result = []
        for s in msg:
            code = han.getStrCode(s)
            scode = han.mkCodeStr(code)
            result.append(scode)
        return result
            
    def bindCode(self, code):    # make bin code strings
        result = []
        lenMsg = len(code)
        lenLine = len(code[0])
        for i in range(lenLine):
            sline = ''
            for j in range(lenMsg):
                sline += code[j][i]
            result.append(sline)
        return result

    def shiftLeft(self, code):
        result = []
        for i in range(len(code)):
            lbit = code[i][0]
            nbit = code[i][1:]+lbit
            result.append(nbit)
        return result

    def shiftRight(self, code):
        result = []
        for i in range(len(code)):
            rbit = code[i][-1]
            nbit = rbit+code[i][:-1]
            result.append(nbit)
        return result

    def shiftDown(self, code):
        bline = code.pop()
        code.insert(0, bline)
        return code

    def shiftUp(self, code):
        fline = code.pop(0)
        code.append(fline)
        return code

    def expandV(self,code):
        result = []
        for i in range(8):
            result.append(code[i])
            result.append(code[i])
        return result

    def finish(self):
        GPIO.cleanup()

# main routine
if __name__ == "__main__":
    try:
        print("Start")
        
        dotled = dotLed(SIN1,SIN2,SIN3,CLK,LATCH,ENABL)
        msgCode1 = dotled.mkMsgCode(MSG1)
        msgCode2 = dotled.mkMsgCode(MSG2)
        fulCode = dotled.sumLines(msgCode1, msgCode2)
        # print(fulCode,len(fulCode))
        # dotled.prnCode(fulCode)
        allCode = dotled.bindCode(fulCode)
#        dotled.prnCode(allCode)
        dspCode = dotled.dev_digit(allCode)
        cnt = 0
        lvl = 0
        lmsg = len(allCode[0])
        while True:
            dotled.dspLED(dspCode[0], dspCode[1], 5)
            if lvl == 0:
                allCode = dotled.shiftLeft(allCode)
            elif lvl == 1:
                allCode = dotled.shiftRight(allCode)
            elif lvl == 2:
                allCode = dotled.shiftUp(allCode)
            elif lvl == 3:
                allCode = dotled.shiftDown(allCode)
            else:
                fulCode = dotled.bindCode(msgCode2)
                allCode = dotled.expandV(fulCode)
            cnt = (cnt+1)%lmsg
            if cnt == 0:
                lvl = (lvl+1)%5
#                dotled.prnCode(allCode)
            dspCode = dotled.dev_digit(allCode)
                
    except KeyboardInterrupt:
        print("Finished.")
    dotled.finish()