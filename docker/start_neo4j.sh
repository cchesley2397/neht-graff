#!/bin/bash

sudo docker run --name neht-neo4j -p7687:7687 -p7474:7474 -p7473:7473 -v /home/dev/PycharmProjects/neht-graff/data/csv:/var/lib/neo4j/import --network=host --env NEO4J_AUTH=neo4j/nehtgraff  --rm neo4j