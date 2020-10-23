import socket
import os
import multiprocessing as mp
import sys
import ipaddress
import json


# 自定义异常
class CustomizeError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


# 扫描IP段
IPList = []  # 存放存活的IP


def ping_ip(ip, file, lock):
    print(f"进程(ID:{os.getpid()})开始扫描" + ip)
    ret = os.popen('ping -c 1 %s' % ip).read()
    if ret.upper().find('TTL') >= 0:
        IPList.append(ip)
        try:
            lock.acquire()
            with open(file, "a+", encoding="utf-8") as json_file:
                json.dump(IPList, fp=json_file, ensure_ascii=False)
                json_file.write("\n")
                json_file.close()
        except IOError:
            print("文件操作失败")
        finally:
            lock.release()
        print("%s 能ping通:" % ip)
    else:
        print("%s 不能ping通" % ip)

    print("IPList:", IPList)


def tcp_port(ip, port, file, lock):
    print(f"进程(ID:{os.getpid()})开始扫描" + ip + f"端口: %s" % port)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        if result == 0:
            try:
                lock.acquire()
                portlist = {
                    "ip": ip,
                    "port": port,
                }
                with open(file, "a+", encoding="utf-8") as json_file:
                    print('%s :' % ip + '%s 端口open' % port)
                    json.dump(portlist, fp=json_file, ensure_ascii=False)
                    json_file.write("\n")
                    json_file.close()
            except IOError:
                print("文件操作失败")
            finally:
                lock.release()
        else:
            print("端口关闭")
    except Exception as err:
        print("err:", err)


if __name__ == '__main__':
    n = ""
    f = ""
    w = ""
    ip_list = []
    mutex = mp.Manager().RLock()
    cpu_count = mp.cpu_count()
    print("最大进程数:", cpu_count)
    # 获取s命令行参数列表
    args = sys.argv
    # 处理命令行参数
    for i in range(1, len(args)):
        arg = args[i]
        if arg == '-n':
            n = args[i + 1]
        elif arg == '-f':
            f = args[i + 1]
        elif arg == '-ip':
            ip_list = args[i + 1].split("-")
            if len(ip_list) == 1:
                start_ip = ip_list[0]
                if [1] * 4 != [x.isdigit() and 0 <= int(x) <= 255 for x in start_ip.split(".")]:
                    raise CustomizeError("不合法的IP")
            else:
                start_ip = ip_list[0]
                if [1] * 4 != [x.isdigit() and 0 <= int(x) <= 255 for x in start_ip.split(".")]:
                    raise CustomizeError("不合法的IP")
                end_ip = ip_list[1]
                start_addr = ipaddress.IPv4Address(start_ip)
                end_addr = ipaddress.IPv4Address(end_ip)
                if start_addr >= end_addr:
                    raise CustomizeError("IP范围不合法")
        elif arg == '-w':
            w = args[i + 1]
    if int(n) > cpu_count:
        raise CustomizeError("进程数过多，应小于 %s 个" % cpu_count)
    else:
        p = mp.Pool(int(n))

    if len(ip_list) == 1:
        if f == 'ping':
            w = 'result.json'
            p.apply_async(ping_ip, args=(start_ip, w, mutex))
        if f == 'tcp':
            for port in range(1, 1024):
                p.apply_async(tcp_port, args=(start_ip, port, w, mutex))
    elif len(ip_list) == 2:
        if f == 'ping':
            w = 'result.json'
            for i in range(int(start_ip.split(".")[-1]), int(end_ip.split(".")[-1]) + 1):
                ip = start_ip[:start_ip.rfind('.') + 1] + str(i)
                p.apply_async(ping_ip, args=(ip, w, mutex))
        if f == 'tcp':
            for i in range(int(start_ip.split(".")[-1]), int(end_ip.split(".")[-1]) + 1):
                ip = start_ip[:start_ip.rfind('.') + 1] + str(i)
                for port in range(1, 1024):
                    p.apply_async(tcp_port, args=(ip, port, w, mutex))
    p.close()
    p.join()

