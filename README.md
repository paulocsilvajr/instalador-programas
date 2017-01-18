# Instalador de Programas
### Desenvolvido no Ubuntu 16.04, Python3.5, Tkinter.

Este repositório contém um software desenvolvido em python para instalar programas na distribuição Ubuntu. Seu objetivo é facilitar e agilizar o processo de instalar vários aplicativos ao mesmo tempo. Para isso, ele usa de uma lista previamente alimentada.

###Pré-requisitos
Conceder privilégio de execução ao script 'instalador.sh'.
Instalar o pacote do IDLE do python3. No Ubuntu 16.04 usar o comando abaixo.
```
$ apt install idle-python3*;
```
Quando executado o programa pelo script 'instalador.sh', é verificado se foi instalado o pacote idle-python3*, caso necessário é feito a instalação automática.
###Arquivos

```
instalador.sh: Executável do programa. Pede senha do administrador no início.
src/instalador.py: Arquivo python principal do programa.
src/programas: Arquivo contendo as entradas de instalação de programas. Informações sobre formato na docstring da módulo instalador.py.
src/isinstalled.sh: Script para verificar se pacote está instalado. Usado em instalador.py.
src/interface_grafica.py: Módulo contendo a interface gráfica do instalador.
src/gerenciador_programas.py: Módulo com funções para gerenciar os programas. Módulo base para o instalador.py.
```

###Licença

[Licença GPL](https://github.com/paulocsilvajr/instalador-programas/blob/master/license_gpl.txt), arquivo em anexo no repositório.

###Contato

Paulo Carvalho da Silva Junior - pauluscave@gmail.com
