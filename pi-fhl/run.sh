#!/bin/sh

docker-compose run -w /data runner python main.py "$@"
