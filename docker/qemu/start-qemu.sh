#!/bin/bash
echo "Starting QEMU with OpenBMC..."

IMAGE_FILE=$(ls -t /romulus/obmc-phosphor-image-romulus-*.static.mtd | head -1)

echo "Using image: $IMAGE_FILE"

qemu-system-arm \
  -m 256 \
  -M romulus-bmc \
  -nographic \
  -drive file="$IMAGE_FILE",format=raw,if=mtd \
  -net nic \
  -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu
