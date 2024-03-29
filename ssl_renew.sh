#!/bin/bash

COMPOSE="/usr/local/bin/docker-compose --no-ansi"
DOCKER="/usr/bin/docker"

cd /home/admin/api-dataviewer/
$COMPOSE run certbot renew && $COMPOSE kill -s SIGHUP nginx
$COMPOSE rm -s -v -f certbot
$DOCKER image rm -f api-dataviewer_certbot
