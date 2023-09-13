#!/usr/bin/env bash

USUARIO=$(logname);
HOME_USUARIO=/home/$USUARIO

git clone --depth=1 https://github.com/amix/vimrc.git $HOME_USUARIO/.vim_runtime &&
    su -l $USUARIO -c "sh $HOME_USUARIO/.vim_runtime/install_awesome_vimrc.sh"

