# import time
#
# tempTime = time.time()
# print(tempTime)
# tempTimeLocal = time.localtime(tempTime)
# print(tempTimeLocal)
# rq = time.strftime('%Y%m%d%H%M', tempTimeLocal)
# print(rq)
#
# rq = time.strftime('%Y%m%d%H%M%S', tempTimeLocal)
# print(rq)
#
# rq = time.strftime('%Y%m%d%H%M%s', tempTimeLocal)
# print(rq)
#
# rq = time.strftime('%s', tempTimeLocal)
# print(rq)

"""
from copy import deepcopy


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def setName(self, name):
        self.name = name

    def setAge(self, age):
        self.age = age

    def detail(self):
        print(str(self.name) + str(self.age))


user = User("via", "27")
user.detail()
print(user)
userBackup1 = user
userBackup1.detail()
print(userBackup1)
userDeepCopy = deepcopy(user)
userDeepCopy.detail()
print(userDeepCopy)
user.setName("yie")

userBackup2 = user
userBackup2.detail()
print(userBackup2)

print("_____________________")
user.detail()
userBackup1.detail()
userDeepCopy.detail()
userBackup2.detail()

"""

# from torch.cuda import amp
# scaler = amp.GradScaler(enabled=cuda)

# import torch
# import torch.distributed as dist   # ！！！！！！！！！！！！！！！！！！！！！！！！
# from torch.utils.data.distributed import DistributedSampler  # ！！！！！！！！！！！！！！！！！！！
#
# dist.init_process_group(backend='nccl', init_method='env://')  # ！！！！！！！！！！！！！！！！！！！！！
# batch_size = 12  # 主卡上的batchsize      # ！！！！！！！！！！！！！！！！！！！！！！！！！！
# data_size = 25  # 总共的batchsize   # ！！！！！！！！！！！！！！！！！！！
# local_rank = torch.distributed.get_rank()
# print(local_rank)

"""
Hi ,
#1、安装pptp-linux
sudo apt-get install pptp-linux binutils
#2、建立pptp连接
sudo pptpsetup --create testvpn --server 207.148.109.43 --username via --password yie --encrypt --start
#2.1ifconfig查看pptp建立后的通信ip和网关， eg: inet 192.168.0.111  netmask 255.255.255.255  destination 192.168.0.1
#3、添加默认路由(备注:对应的网关地址和默认路由按自己的配置)
sudo route add default gw 192.168.0.1
#4、删除默认路由
sudo route del default gw 10.66.79.254
#5、恢复原有路由
sudo route add default gw 10.66.79.254


sudo pptpsetup --create testvpn --server 207.148.109.43 --username via --password yie --encrypt --start
sudo route add default gw 192.168.0.1
sudo route del default gw 10.66.79.254



sudo route add default gw 10.66.79.254
sudo route del default gw 192.168.0.1

smb://192.168.110.16/westwell-alpha/	westwell-alpha	Alpha-WWL	alpha组使用


"""

from tqdm import tqdm
import time
for char in tqdm(["a", "b", "c", "d"]):
    #do something
    time.sleep(2)
    pass