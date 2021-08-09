#!/bin/bash

COMPOSE="/usr/local/bin/docker-compose --no-ansi"
DOCKER="/usr/bin/docker"

cd /home/admin/api-dataviewer/

$DOCKER start update-db-lop-container
