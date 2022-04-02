docker network create --driver bridge --subnet 192.168.1.0/16 --gateway 192.168.1.0 disknet
docker-compose up -f docker-compose_mariadb.yml -d