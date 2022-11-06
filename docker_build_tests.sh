#!/bin/bash

docker build . -f docker_docs/Dockerfile_postgresql_test -t postgresql_docker_test
docker run --name database_test -d -v pgdata_test:/var/lib/postgresql/data -p 6432:5432 postgresql_docker_test

docker build . -f docker_docs/Dockerfile_python_test -t python_docker_test
docker run --name app_test -d -p 5001:5000 --link database_test:postgresql python_docker_test
