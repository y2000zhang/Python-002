
学习笔记
本次作业是选择使用多进程。
IP扫描用的os.popen('ping -c 1 %s' % ip),macOS和Linux用-c,在结果里find('TTL')才能拿到需要的信息。
端口扫描用到socket，是从网上临时查的，需要再多看看。
判断是否是合法IP和有效IP范围比较麻烦，判断是否是合法IP：[1] * 4 != [x.isdigit() and 0 <= int(x) <= 255 for x in start_ip.split(".")]
合法IP段：paddress.IPv4Address(start_ip)<paddress.IPv4Address(end_ip)
