#/bin/bash

docker swarm leave --force > /dev/null
docker swarm init > /dev/null

docker compose -f stack.yml build
docker stack deploy -c stack.yml tema3 --detach=false