# Instalador de Programas
### Desenvolvido no Ubuntu 16.04, Python3.5, Tkinter.

Este repositório contém um software desenvolvido em python para instalar programas na distribuição Ubuntu. Seu objetivo é facilitar e agilizar o processo de instalar vários aplicativos ao mesmo tempo. Para isso, ele usa de uma lista previamente alimentada.

###Pré-requisitos
Conceder privilégio de execução ao script 'instalador.sh'.
Instalar os pacotes: IDLE do python3 e gksu.
No Ubuntu 16.04 usar os comandos abaixo:
```
# apt install idle-python3*;
# apt install gksu;
```
Quando executado o programa pelo script 'instalador.sh', é verificado se os programas informados nos requisitos foram instalados, caso necessário é feito a instalação automática.

###Arquivos

```
instalador.sh: Executável do programa. Pede senha do administrador no início. Usar parâmetro -g para GUI.
src/instalador.py: Arquivo python principal do programa.
src/programas: Arquivo contendo as entradas de instalação de programas. Informações sobre formato na docstring da módulo instalador.py.
src/isinstalled.sh: Script para verificar se pacote está instalado. Usado em instalador.py.
src/interface_gui.py: Módulo contendo a interface gráfica do instalador.
src/interface_cli.py: Módulo contendo a interface de linha de comando do instalador.
src/gerenciador_programas.py: Módulo com funções para gerenciar os programas. Módulo base para o instalador.py.
```

###Licença

[Licença GPL](https://github.com/paulocsilvajr/instalador-programas/blob/master/license_gpl.txt), arquivo em anexo no repositório.

###Contato

Paulo Carvalho da Silva Junior - pauluscave@gmail.com
