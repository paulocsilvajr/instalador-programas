#!/bin/bash

path=$0
path="${path%/*}"
path=$path/src/instalador.py

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

# Se parametro1 estiver vazio.
if [ -z $1 ]; then
    is_root

    python3 $path
else
    case $1 in
        "-h"|"--help")
              echo "Instalador de programas para distribuições baseadas em Ubuntu."
              echo "Interface padrão: cli(terminal)"
              echo
              echo "Sintaxe: $0 [-h --help -g]"
              echo "-h --help      Ajuda"
              echo "-g             Interface gráfica"
              echo
              echo "Autor: Paulo C. Silva Junior"
              echo "Github: paulocsilvajr"
              ;;
        "-g")
            is_root
            
            install_idle_python

            python3 $path g
            ;;
        *)
            echo "Parâmetro inválido: $1, -h para ajuda."
            exit 1
            ;;
    esac
fi

