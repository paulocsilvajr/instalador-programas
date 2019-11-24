#!/usr/bin/env bash

DESTINO=/usr/bin/
NOME_PROGRAMA="instalador-programas"

is_root(){
    if [ "$(id -u)" != "0" ]; then
        echo "Execute esse programa como ROOT, -h para ajuda."
        exit 1
    fi
}

make_program(){
    echo $PWD/instalador.sh '$1' > $NOME_PROGRAMA

    # move o programa para /usr/bin, definição de permissão e
    # mensagem de confirmação
    mv -vi $NOME_PROGRAMA $DESTINO$NOME_PROGRAMA && chmod 755 -v $DESTINO$NOME_PROGRAMA && echo "Reinicie o terminal para utilizar o programa" $NOME_PROGRAMA
}

help(){
    echo "Instalador para o programa ser executado diretamente pelo terminal."
    echo "Necessário um usuário administrador para executar."
    echo "Sintaxe: $0 [ -h | --help ]"
    echo "-h --help      Ajuda"
    exit 0
}

if [ "$1" == "-h" ] || [ "$1" == "--help" ];
then
    help
fi

is_root

make_program

