FROM ubuntu:18.04
# 这里要替换 your_name 为您的名字, 和your_email 为您的Email
MAINTAINER mercury <mercury@run.run>
# 更新源
RUN apt-get update
# 清除缓存
RUN apt-get autoclean
# 安装python
RUN apt-get install -y python3

# -i https://pypi.tuna.tsinghua.edu.cn/simple
# 装依赖
RUN apt install -y python3-pip
RUN python3 -m pip install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN apt-get install -y git supervisor mysql-server redis-server
RUN pip3 install jinja2 flask gevent gunicorn pymysql flask_sqlalchemy redis flask-cors

# 启动时运行这个命令
CMD ["/bin/bash"]