FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    qemu-system-arm \
    wget \
    unzip \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /qemu

RUN wget -O romulus.zip \
    "https://jenkins.openbmc.org/job/ci-openbmc/lastSuccessfulBuild/distro=ubuntu,label=docker-builder,target=romulus/artifact/openbmc/build/tmp/deploy/images/romulus/*zip*/romulus.zip" \
    && unzip romulus.zip \
    && rm romulus.zip

COPY start-qemu.sh /qemu/start-qemu.sh
RUN chmod +x /qemu/start-qemu.sh

EXPOSE 2222 2443 2623

CMD ["/qemu/start-qemu.sh"]