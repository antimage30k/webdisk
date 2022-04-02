#!/usr/bin/env bash

chmod -R o+rwx /var/www/webdisk

cp /var/www/webdisk/deploy/webdisk.conf /etc/supervisor/conf.d/webdisk.conf

# 初始化
cd /var/www/webdisk
python3 manager.py db init || echo 'not first deploy'
python3 manager.py db migrate
python3 manager.py db upgrade

python manager.py add_admin

# 重启服务器
service supervisor restart

tail -f /dev/null