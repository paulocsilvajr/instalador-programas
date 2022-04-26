#!/usr/bin/env bash

apt-get update &&
    apt-get -y install apt-transport-https ca-certificates curl software-properties-common &&
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - &&
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(. /etc/os-release; echo "$UBUNTU_CODENAME") stable" &&
    apt-get update &&
    apt-get -y install docker-ce docker-compose &&
    usermod -aG docker $USER