import logging  # 引入logging模块
import os
import os.path
import time
from pathlib import Path


print("Path:"+str(Path))
# 获取当前目录
current_path = Path.cwd()
print("current_path:"+str(current_path))
home_path = Path.home()
print("home_path:"+str(home_path))
print("os.getcwd():"+str(os.getcwd()))
print("os.path.dirname(os.getcwd()):"+str(os.path.dirname(os.getcwd())))


# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/logs/'
if not os.path.exists(log_path):
    os.makedirs(log_path)
log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
# 日志
logger.debug('this is a logger debug message')
logger.info('this is a logger info message')
logger.warning('this is a logger warning message')
logger.error('this is a logger error message')
logger.critical('this is a logger critical message')