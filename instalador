#!/bin/bash

#Instalação do idle-python3 se necessário.
verif_idle=$(dpkg --get-selections|grep "^idle-python3*"|grep "\binstall");
if [[ -z $verif_idle ]];
then
	echo "Instalando idle-python3...";
	sudo apt install idle-python3* -y;
fi

path=$0;
path="${path%/*}";
path=$path/src/instalador.py;

#Se parametro1 estiver vazio.
if [ -z $1 ]; then
	sudo python3 $path;
else
	if [ $1 = "-gk" ];
	then
		#Verificação se o gksu/gksudo está instalado, caso negativo, instala automaticamente.
		verif_gksu=$(dpkg --get-selections|grep "^gksu"|grep "\binstall");
		if [[ -z $verif_gksu ]];
		then
			echo "Instalando gksu...";
			sudo apt install gksu -y;
		fi

		gksudo python3 $path;
	else
		echo "Parâmetro inválido: $1";
	fi
fi
