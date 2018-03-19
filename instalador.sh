#!/bin/bash

CAMINHO=$0
CAMINHO="${CAMINHO%/*}"
CAMINHO=$CAMINHO/src/instalador.py

is_root(){
    # Verificação se o programa foi executado como root
    if [ "$(id -u)" != "0" ]; then
        echo "Execute esse programa como ROOT"
        exit 1
    fi
}

install_idle_python(){
    # Instalação do idle-python3 se necessário.
    verif_idle=$(dpkg --get-selections|grep "^idle-python3*"|grep "\binstall")

    if [[ -z $verif_idle ]]; then
        echo "Instalando idle-python3..."
        apt install idle-python3* -y
    fi
}

help(){
      echo "Instalador de programas para distribuições baseadas em Ubuntu."
      echo "Interface padrão: cli(terminal)"
      echo
      echo "Sintaxe: $0 [-h --help -g]"
      echo "-h --help      Ajuda"
      echo "-g             Interface gráfica"
      echo
      echo "Autor: Paulo C. Silva Junior"
      echo "Github: paulocsilvajr"
}

# Se parametro1 estiver vazio.
if [ -z $1 ]; then
    is_root
    install_idle_python

    python3 $CAMINHO
else
    case $1 in
        "-h"|"--help")
            help
            ;;
        "-g")
            is_root
            install_idle_python

            python3 $CAMINHO g
            ;;
        *)
            echo "Parâmetro inválido: $1, -h para ajuda."
            exit 1
            ;;
    esac
fi

