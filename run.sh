#/bin/bash

docker swarm leave --force 2> /dev/null
docker compose -f stack.yml build
docker swarm init 2> /dev/null
docker stack deploy -c stack.yml tema3 --detach=false
