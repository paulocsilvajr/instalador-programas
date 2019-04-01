#!/usr/bin/env bash

verif=$(dpkg --get-selections|grep "^$1\s"|grep "\sinstall");

if [[ -n $verif ]];
then
	echo "$1 está instalado";

	if [ -z $2 ];
	then
		echo "";
	else
		if [ $2 = "-p" ];
		then
			echo "Pacotes:"

			for item in $verif;
			do
				if [ $item != "install" ];
				then
					echo $item;
				fi
			done
		else
			echo "Paramentro inválido $2"
		fi
	fi
fi
