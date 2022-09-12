#!/usr/bin/env bash

PORT='3001'

snap install wekan &&
    snap set wekan port=$PORT && 
    systemctl restart snap.wekan.wekan &&
    echo "Wekan rodando via SNAP em porta $PORT"
