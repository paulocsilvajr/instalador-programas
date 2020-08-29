#!/usr/bin/env bash

USUARIO=$(users|awk ' {print $1} ');
HOME_USUARIO=/home/$USUARIO

git clone --depth=1 https://github.com/amix/vimrc.git $HOME_USUARIO/.vim_runtime &&
    su -c "sh $HOME_USUARIO/.vim_runtime/install_awesome_vimrc.sh" $USUARIO &&
    chown -R $USUARIO $(ls -d $HOME_USUARIO/.* | grep 'vim');