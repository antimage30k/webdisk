#!/usr/bin/env bash
set -ex

# 删除测试用户和测试数据库
# 删除测试用户和测试数据库并限制关闭公网访问
mysql -u root -ptest -e "DELETE FROM mysql.user WHERE User='';"
mysql -u root -ptest -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
mysql -u root -ptest -e "DROP DATABASE IF EXISTS test;"
mysql -u root -ptest -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
# 设置密码并切换成密码验证
mysql -u root -ptest -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'test';"

cp /var/www/webdisk/webdisk.nginx /etc/nginx/sites-enabled/webdisk
chmod -R o+rwx /var/www/webdisk

cp /var/www/webdisk/webdisk.conf /etc/supervisor/conf.d/webdisk.conf

# 初始化
cd /var/www/webdisk
python3 reset.py

# 重启服务器
service supervisor restart
service nginx restart

tail -f /dev/null