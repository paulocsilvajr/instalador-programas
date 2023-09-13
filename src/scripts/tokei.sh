#!/usr/bin/env bash

USUARIO=$(logname);

su -l $USUARIO -c "cargo install tokei"
