#!/bin/bash

# Verificação se o programa foi executado como root
if [ "$(id -u)" != "0" ]; then
    echo "Execute esse programa como ROOT"
    exit 0
fi

# Instalação do idle-python3 se necessário.
verif_idle=$(dpkg --get-selections|grep "^idle-python3*"|grep "\binstall");
if [[ -z $verif_idle ]];
then
	echo "Instalando idle-python3...";
	apt install idle-python3* -y;
fi

path=$0;
path="${path%/*}";
path=$path/src/instalador.py;

# Se parametro1 estiver vazio.
if [ -z $1 ]; then
	python3 $path;
else
    case $1 in
        "-h") echo "Instalador de programas para distribuições baseadas em Ubuntu"
              echo "Interface padrão: cli(terminal)"
              echo "Sintaxe:" $0 "[-h -g]"
              echo "-h      Ajuda"
              echo "-g      Interface gráfica"
              echo
              echo "Autor: Paulo C. Silva Junior"
              echo "Github: paulocsilvajr";;
        "-g")
            # Não é mais necessário, pois foi obrigado executar o programa como root
            # Verificação se o gksu/gksudo está instalado, caso negativo, instala automaticamente.
#    		verif_gksu=$(dpkg --get-selections|grep "^gksu"|grep "\binstall");
#    		if [[ -z $verif_gksu ]];
#    		then
#    			echo "Instalando gksu...";
#    			apt install gksu -y;
#    		fi
#
#    		gksudo python3 $path g;
            python3 $path g;;
        *)
		    echo "Parâmetro inválido: $1";;
	esac
fi
