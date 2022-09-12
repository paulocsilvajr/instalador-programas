#!/usr/bin/env bash

USUARIO=$(logname)
HOME_USUARIO=/home/$USUARIO

# https://go.dev/dl/go1.18.4.linux-amd64.tar.gz
GOLANG=go1.18.4.linux-amd64
LINK=https://go.dev/dl/$GOLANG.tar.gz

if [ -d "/usr/local/go" ]; then
    versao=$(/usr/local/go/bin/go version)
    echo "Removendo versão anterior do GO[$versao]"
    rm -rf /usr/local/go
fi

adicionar_go_em_profile() {
    if grep "/usr/local/go/bin" $1 > /dev/null; then
        echo "Arquivo $1 - OK"
    else
        echo 'export PATH=$PATH:/usr/local/go/bin' >> $1 &&
        echo 'export GOPATH=$HOME/go' >> $1 &&
        echo 'export PATH=$PATH:$GOPATH/bin' >> $1 &&
        echo "Atualizado PATH e criado variável de ambiente GOPATH"
    fi
}

wget -c $LINK &&
    sudo tar -C /usr/local/ -xzf $GOLANG.tar.gz &&
    mkdir $HOME_USUARIO/go $HOME_USUARIO/go/bin $HOME_USUARIO/go/pkg $HOME_USUARIO/go/src ||
    chown -R $USUARIO $HOME_USUARIO/go &&
    adicionar_go_em_profile $HOME_USUARIO/.profile &&
    rm -v $GOLANG.tar.gz &&
    echo -e "\nDisponibilizado variável $GOPATH, diretório ~/go e finalizado instalação.\n" &&
    echo -e "\nPara usuários do ZSH, execute o comando abaixo para reconhecer o executável go:\ncp -v ~/.profile ~/.zprofile\n" &&
    echo -e "\nReinicie a sessão para poder usar o GO\n"
