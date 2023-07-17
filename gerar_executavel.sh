#!/usr/bin/env bash

pip3 install pyinstaller

mkdir dist
cp -vu src/programas src/isinstalled.sh src/logo dist
pyinstaller --onefile src/instalador.py