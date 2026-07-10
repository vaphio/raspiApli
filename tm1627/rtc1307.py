from machine import Pin, I2C
from time import sleep, localtime

#DS1307 connect
# clk = I2C(0, scl=Pin(sclPin), sda=Pin(sdaPin), freq=200000)

addr = 0x68    #RTC address
regi = 0x00

wk = ['MON','TUE','WED','THU','FRI','SAT','SUN']

class RTC(object):
    def __init__(self, i2c):
        self.i2c = i2c

    def getTime(self):
        tm = self.i2c.readfrom_mem(int(addr), int(regi), 8)
        res = []
        res.append(self.bcd_to_num(tm[6])+2000)   #year
        res.append(self.bcd_to_num(tm[5]&0x1F))   #month
        res.append(self.bcd_to_num(tm[4]&0x3F))   #day
        res.append(self.bcd_to_num(tm[2]&0x3F))   #hour
        res.append(self.bcd_to_num(tm[1]&0x7F))   #minute
        res.append(self.bcd_to_num(tm[0]&0x7F))   #sec
        res.append(self.bcd_to_num(tm[3]&0x07))   #week
        return res

    def bcd_to_num(self, num):
        b = num>>4
        c = num&0x0f
        return b*10+c

    def num_to_bcd(self, num):
        return (num // 10 * 16 + (num % 10))


    def getAdr(self):
        return self.i2c.scan()

    def initRTC(self):
        self.i2c.writeto_mem(int(addr),0x00,b'\00')

    def setTime(self):
        lt = localtime()
        y = self.num_to_bcd(lt[0]-2000)
        m = self.num_to_bcd(lt[1])
        d = self.num_to_bcd(lt[2])
        w = self.num_to_bcd(lt[6])
        h = self.num_to_bcd(lt[3])
        n = self.num_to_bcd(lt[4])
        s = self.num_to_bcd(lt[5])
        self.i2c.writeto_mem(int(addr), int(regi), s.to_bytes(1,'big'))
        self.i2c.writeto_mem(int(addr), int(regi+1), n.to_bytes(1,'big'))
        self.i2c.writeto_mem(int(addr), int(regi+2), h.to_bytes(1,'big'))
        self.i2c.writeto_mem(int(addr), int(regi+3), w.to_bytes(1,'big'))
        self.i2c.writeto_mem(int(addr), int(regi+4), d.to_bytes(1,'big'))
        self.i2c.writeto_mem(int(addr), int(regi+5), m.to_bytes(1,'big'))
        self.i2c.writeto_mem(int(addr), int(regi+6), y.to_bytes(1,'big'))
    
#    clk.writeto_mem(int(addr), int(regi),tf.encode())
if __name__ == "__main__":
    
    i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=200000)
    print(i2c.scan())
    clk = RTC(i2c)
#    clk.setTime()

    try:
        while(True):
            tm = clk.getTime()
            print(tm, wk[tm[6]])
            sleep(1)
    except KeyboardInterrupt:
        pass
