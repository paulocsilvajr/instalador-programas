# Instalador de Programas
### Desenvolvido no Ubuntu 16.04, Python3.5, Tkinter.

Este repositório contém um software desenvolvido em python para instalar programas na distribuição Ubuntu. Seu objetivo é facilitar e agilizar o processo de instalar vários aplicativos ao mesmo tempo. Para isso, ele usa de uma lista previamente alimentada.

###Pré-requisitos
Conceder privilégio de execução ao script 'instalador'.
Instalar o pacote do IDLE do python3. No Ubuntu 16.04 usar o comando abaixo.
```
$ apt install idle-python3*;
```
Quando executado o programa pelo script 'instalador', é verificado se foi instalado o pacote idle-python3*, caso necessário é feito a instalação automática.
###Arquivos

```
instalador: Executável do programa. Pede senha do administrador no início.
instalador.py: Arquivo python do programa. Para usá-lo como executável, deve-se executar com privilégios de adminstrador para o funcionamento correto.
programas: Arquivo contendo as entradas de instalação de programas. Informações sobre formato na docstring da classe Instalador.
isinstalled.sh: Script para verificar se pacote está instalado. Usado em instalador.py.
```

###Licença

[Licença GPL](https://github.com/paulocsilvajr/instalador-programas/blob/master/license_gpl.txt), arquivo em anexo no repositório.

###Contato

Paulo Carvalho da Silva Junior - pauluscave@gmail.com
