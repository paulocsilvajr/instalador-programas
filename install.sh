#!/bin/bash

destino=/usr/bin/
nome_programa="instalador-programas"

is_root(){
    if [ "$(id -u)" != "0" ]; then
        echo "Execute esse programa como ROOT, -h para ajuda."
        exit 1
    fi
}

make_program(){
    echo $PWD/instalador.sh '$1' > $nome_programa 

    # move o programa para /usr/bin, definição de permissão e 
    # mensagem de confirmação
    mv -vi $nome_programa $destino$nome_programa && chmod 755 /$destino$nome_programa && echo "Reinicie o terminal para utilizar o programa" $nome_programa
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

