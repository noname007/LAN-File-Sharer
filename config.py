import os
# server 进程端口
server_port = 8886

# 扫描局域网 其他机器端口
scan_port = 8886

scan_server  = None

# 默认共享文件夹为当前文件夹
shared_folder = os.path.dirname(os.path.realpath(__file__))
# 默认传输的文件保存路径为主目录
default_save_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "download")

sleep_time = 0.5
