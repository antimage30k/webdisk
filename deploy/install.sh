#!/usr/bin/env bash
set -ex

cp -r ../ /var/www/webdisk/

docker-compose up -f ./docker-compose.yml -d

cp ./webdisk.nginx /etc/nginx/conf.d/webdisk.conf

nginx -s reload
