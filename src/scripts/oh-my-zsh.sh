#!/usr/bin/env bash

USUARIO=$(users|awk ' {print $1} ');
HOME_USUARIO=/home/$USUARIO

su -c "sh -c \"\$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)\"" $USUARIO &&
    chown -R $USUARIO $(ls -d $HOME_USUARIO/.* | grep 'zsh');