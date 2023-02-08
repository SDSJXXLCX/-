import psutil
import GPUtil
import struct

# print(list(psutil.win_service_iter()))

class info():
    def __init__(self):
        cpu_count_logical = psutil.cpu_count()
        cpu_count = psutil.cpu_count(logical=False)
        self.cpu_percent = 0
        self.mem_percent = 0
        self.net_io = psutil.net_io_counters()
        self.send_bytes = 0
        self.recv_bytes = 0

    def print_info(self,t=1):
        # print(psutil.cpu_times())  # 获取CPU完整信息
        for i in range(20):
            send_bytes = self.net_io.bytes_sent
            recv_bytes = self.net_io.bytes_recv
            print('CPU使用率:{:3.1f}%'.format(psutil.cpu_percent(interval=t, percpu=False)))  # CPU使用率

            print('内存使用率:{:3.1f}%'.format(psutil.virtual_memory().percent))
            print('交换内存使用率：{:3.1f}%'.format(psutil.swap_memory().percent))
            print('网络信息：', psutil.net_io_counters())
            self.net_io =psutil.net_io_counters()
            send_bytes = self.net_io.bytes_sent - send_bytes
            recv_bytes = self.net_io.bytes_recv - recv_bytes
            self.print_net_io_rat(t,send_bytes,recv_bytes)

            #print('磁盘信息：', psutil.disk_partitions())
            for part in psutil.disk_partitions():
                mountpoint = str(part.mountpoint)
                percent = psutil.disk_usage(mountpoint).percent
                print('{}盘情况{:3.1f}%'.format(mountpoint,percent))

            # 传感器状态
            try:
                print("温度：",psutil.sensors_temperatures())
            except:
                print("无温度结果")
            try:
                print("风扇速度:",psutil.sensors_fans())
            except:
                print("无风扇结果")
            print("电池：",psutil.sensors_battery())

            # GPU信息
            for gpu in GPUtil.getGPUs():
                print(gpu.name,gpu.load,gpu.driver,gpu.temperature)

    def print_net_io_rat(self,t,send_bytes,recv_bytes):
        send_bytes/=t
        recv_bytes/=t
        print("send:",self.print_bytesps(send_bytes))
        print("recv:",self.print_bytesps(recv_bytes))

    def print_bytesps(self,bytes):
        bps = ['Bps','Kps','Mps','Gps','Tps']
        i=0
        while(bytes>=1024):
            bytes/=1024
            i+=1
        return '{:.1f}{}'.format(bytes,bps[i])

    def get_info(self,t=1):
        re = "#"
        return re.join([self.get_cpuinfo(t),
                        self.get_meminfo(),
                        self.get_diskinfo(),
                        self.get_net_ioinfo(t),
                        self.get_gpuinfo()])

    def get_cpuinfo(self,t):
        return 'CPU:{:2.1f}%'.format(psutil.cpu_percent(interval=t, percpu=False))

    def get_meminfo(self):
        return 'M:{:2.1f}%/SM:{:2.1f}%'.format(psutil.virtual_memory().percent,
                                                psutil.swap_memory().percent)
    def get_diskinfo(self):
        re = '/'
        infos = []
        for disk in psutil.disk_partitions():
            mountpoint = str(disk.mountpoint)
            percent = psutil.disk_usage(mountpoint).percent
            infos.append('{}:{:2.1f}%'.format(mountpoint[0],percent))
        return re.join(infos)

    def get_net_ioinfo(self,t):

        self.net_io = psutil.net_io_counters()
        send_bytes_delta = self.net_io.bytes_sent - self.send_bytes
        recv_bytes_delta = self.net_io.bytes_recv - self.recv_bytes
        self.send_bytes = self.net_io.bytes_sent
        self.recv_bytes = self.net_io.bytes_recv

        return 'Send:{}#Recv:{}'.format(
            self.print_bytesps(send_bytes_delta/t),
            self.print_bytesps(recv_bytes_delta/t))

    def get_gpuinfo(self):
        re = '/'
        infos = []
        for gpu in GPUtil.getGPUs():
            infos.append('GPU{}:{:2.1f}-M{:2.1f}-T:{:2.1f}'.format(
                gpu.id, gpu.load, gpu.memoryUtil ,gpu.temperature))
        return re.join(infos)


if __name__ == '__main__':
    I = info()
    #I.print_info(1)
    for i in range(12):

        print(I.get_info())

        print('-1-'*6)
