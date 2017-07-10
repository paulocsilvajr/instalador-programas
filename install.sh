#!/bin/bash

destino=/usr/bin/
nome_programa="instalador-programas"

if [ "$(id -u)" != "0" ]; then
    echo "Execute esse programa como ROOT";
else
    echo $PWD/instalador.sh '$1' > $nome_programa 

    # move o programa para /usr/bin, definição de permissão e 
    # mensagem de confirmação
    mv -vi $nome_programa $destino$nome_programa && chmod 755 /$destino$nome_programa && echo "Reinicie o terminal para utilizar o programa" $nome_programa
fi
