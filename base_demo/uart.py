import serial
import serial.tools.list_ports
import time
from ctypes import c_uint8,c_uint16,c_float
import struct
class uart(object):
    def __init__(self,uart_dict=None):
        self.uart_dict = uart_dict
        self.portslist = []
        self.port = None
        self.pds = 0
        self.portconnected = False
        self.S = None
        self.isopen = False

        self.updata()

    def updata(self,uart_dict=None):
        self.t = time.gmtime()
        self.tform = time.strftime('%H:%M:%S %Y-%m-%d',self.t)
        if uart_dict:
            ##
            try:
                self.close()
                self.S = None
            except:
                print('串口异常 建议重启')
            self.uart_dict = uart_dict
            print('更改于 {}'.format(self.tform))

    def connect(self):
        self.updata()
        try:
            self.S = serial.Serial(self.uart_dict['port'],self.uart_dict['pds'])
            self.portconnected = True
            print('串口连接成功 {}'.format(self.tform))
            self.isopen = True
        except:
            self.portconnected = False
            print('连接失败 串口异常 {}'.format(self.tform))

    def sendtest(self,testbyte = 255):
        #
        testbyte = c_uint8(testbyte)
        result = self.S.write(testbyte)
        if result:
            print("成功发送")
        else:
            print("发送失败")
        self.readtest()
        print('-'*12)
        return result

    def readtest(self):
        res = self.S.read(1)
        print("读一个字(ord):",ord(res))
        print("读一个字:", res)

    def send_uint16(self,num):
        num = c_uint16(num)
        result = self.S.write(num)
        self.endsend()
        if result == 2:
            print("uint16发送成功")
        else:
            print("uint16发送失败")
        return result

    def send_float(self,num):
        """

        :param num:
        :return:
        """
        # num = c_float(num)
        num = struct.pack('f', num) # 将python的float转换 成bytes 4字节
        result = self.S.write(num)
        print("num:",num)
        self.endsend()
        if result == 4:
            print("float 发送成功")
        else:
            print('float 发送失败')
        return result

    def read_float_test(self):
        res = self.S.read(4)
        #print("读一个字(ord):", ord(res))
        print("read a float:", res)

    def endsend(self):
        """
        根据下位机（STM32）编程串口接收到
        0x0d（'\r'） 0x0a('\n')
        结束接收
        """
        self.S.write('\r\n'.encode())
        #self.S.write(c_char(ord('\r')))
        #self.S.write(c_char(ord('\n')))

    def close(self):
        self.updata()
        if self.S and self.isopen:
            self.S.close()
            print('串口关闭 {}'.format(self.tform))
            self.isopen = False

    def open(self):
        self.updata()
        if self.S and not self.isopen:
            self.S.open()
            self.isopen = True

    def search(self):
        self.portslist = list(serial.tools.list_ports.comports())

    def __str__(self):
        self.search()
        print('-'*12)
        print('可用串口 {} 个'.format(len(self.portslist)))
        for i in range(len(self.portslist)):
            info = '{:2d}-'+str(self.portslist[i])
            print(info.format(i))
        print('_'*12)
        print(self.uart_dict)
        print('_'*12)
        if self.portconnected:
            print('Serial信息:')
            print(self.S)
        else:
            print('串口未连接')
        print('_'*12)
        t = time.gmtime()
        return '串口信息'+time.strftime('%H:%M:%S %Y-%m-%d',t)

    def sent_info(self,info):
        result = self.S.write(info.encode())
        #if result:
        #    print('发送成功')
        self.endsend()
        return result

dict = {
    'port':'COM7',
    'pds':9600,
}

if __name__ == '__main__':
    S = uart()
    # print(S)
    S.search()
    print(S)
    S.updata(dict)
    print(S)
    S.connect()
    S.close()
    print(S)
    # s = serial.Serial('COM7',9600)
    # print(s)
    S.open()
    # while S.sendtest(int(input('0-255:'))):
    #     pass
    # while S.send_uint16(int(input('a number:'))):
    #     pass

    #while S.send_float(float(input('a float:'))):
    #    pass

    while S.sent_info(input('输入任意')):
        pass