#!/usr/bin/env bash

USUARIO=$(users|awk ' {print $1} ');
HOME_USUARIO=/home/$USUARIO

GOLANG=go1.15.linux-amd64

wget https://dl.google.com/go/$GOLANG.tar.gz &&
    tar -C /usr/local/ -xzf $GOLANG.tar.gz &&
    mkdir $HOME_USUARIO/go $HOME_USUARIO/go/bin $HOME_USUARIO/go/pkg $HOME_USUARIO/go/src ||
    chown -R $USUARIO $HOME_USUARIO/go &&
    echo 'export PATH=$PATH:/usr/local/go/bin' >> $HOME_USUARIO/.profile &&
    echo 'export GOPATH=$HOME/go' >> $HOME_USUARIO/.profile &&
    echo 'export PATH=$PATH:$GOPATH/bin' >> $HOME_USUARIO/.profile &&
    rm -v $GOLANG.tar.gz &&
    echo 'Disponibilizado variável $GOPATH, diretório ~/go e finalizado instalação.' &&
    echo -e "Para usuários do ZSH, execute o comando abaixo para reconhecer o executável go:\ncp -v ~/.profile ~/.zprofile"
