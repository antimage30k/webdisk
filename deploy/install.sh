#!/usr/bin/env bash
set -ex

docker-compose -f ./docker-compose.yml up -d

cp ./webdisk.nginx /etc/nginx/conf.d/webdisk.conf

nginx -s reload
