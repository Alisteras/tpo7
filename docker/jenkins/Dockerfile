FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y \
        docker.io \
        python3 \
        python3.13-venv \
        python3-pip \
        curl \
        wget \
        git \
        unzip \
        chromium && \
    npm install -g chromedriver && \
    ln -sf /usr/bin/chromium /usr/bin/google-chrome && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
