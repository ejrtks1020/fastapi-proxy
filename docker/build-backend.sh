#!/bin/bash
DOCKER_BUILDKIT=1 docker build --target=runtime -t proxy_server -f ./Dockerfile ..
