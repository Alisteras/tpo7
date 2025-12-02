#!/bin/bash

cd ./docker/qemu
docker rm qemu-openbmc
docker build -t openbmc-qemu .
docker run -d \
  --name qemu-openbmc \
  --privileged \
  -p 2222:2222 \
  -p 2443:2443 \
  -p 2623:2623 \
  openbmc-qemu