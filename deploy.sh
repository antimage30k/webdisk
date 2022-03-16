#!/usr/bin/env bash

set -ex

# 系统设置
apt-get install -y zsh curl ufw
# sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 465
ufw allow 8080
ufw allow 31116
ufw allow 7777
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# 装依赖
apt install python3-pip
python3 -m pip install --upgrade pip
pip3 install --upgrade setuptools
apt-get install -y git supervisor nginx python3-pip mysql-server redis-server
pip3 install jinja2 flask gevent gunicorn pymysql flask_sqlalchemy redis flask-cors

# 删除测试用户和测试数据库
# 删除测试用户和测试数据库并限制关闭公网访问
mysql -u root -ptest -e "DELETE FROM mysql.user WHERE User='';"
mysql -u root -ptest -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
mysql -u root -ptest -e "DROP DATABASE IF EXISTS test;"
mysql -u root -ptest -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
# 设置密码并切换成密码验证
mysql -u root -ptest -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'test';"

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default
# 不要再 sites-available 里面放任何东西
cp /var/www/webdisk/webdisk.nginx /etc/nginx/sites-enabled/webdisk
chmod -R o+rwx /var/www/webdisk

cp /var/www/webdisk/webdisk.conf /etc/supervisor/conf.d/webdisk.conf


# 初始化
cd /var/www/webdisk
python3 reset.py

# 重启服务器
service supervisor restart
service nginx restart

echo 'succsss'
echo 'ip'
hostname -I