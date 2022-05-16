#!/usr/bin/env bash

chmod -R o+rwx /var/www/webdisk

cp /var/www/webdisk/deploy/webdisk.conf /etc/supervisor/conf.d/webdisk.conf

# 初始化
cd /var/www/webdisk
python3 manager.py create_db
python3 manager.py db init || echo 'not first deploy'
python3 manager.py db migrate
python3 manager.py db upgrade

python3 manager.py add_admin

# python3 manager.py set_environ
# 启动服务
# Subprocesses will inherit the environment of the shell used to start the supervisord program.
supervisord -c /etc/supervisor/supervisord.conf

tail -f /dev/null