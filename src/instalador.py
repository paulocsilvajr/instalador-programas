# coding: utf-8

from sys import argv
try:
    from src.gerenciador_programas import gera_lista_programas
    from src.interface_gui import Instalador as InstaladorGUI
    from src.interface_cli import instalador as InstaladorCLI
except ImportError:
    from gerenciador_programas import gera_lista_programas
    from interface_gui import Instalador as InstaladorGUI
    from interface_cli import instalador as InstaladorCLI

__author__ = 'Paulo C. Silva Jr.'

__version__ = '0.4.0'

"""
Instalador de programas, desenvolvido: Ubuntu 18.04, Python3.7, Tkinter.
O arquivo programas deve ter entradas no seguinte formato:
+------ Exemplo de entrada em programas ------+
|#Descrição do pacote                         |
|package::apt::nome_pacote                     |
|dependency::nome_pacote_necessário          |
|ppa::ppa:repositorio                         |
|install::apt install pacote_complementar     |
|remove::apt remove pacote_complementar       |
|                                             |
+---------------------------------------------+
# Cada entrada de programa deve terminar com uma nova linha para separa-las.
# Os caracteres :: são os separadores, portando devem ser mantidos.
# apt pode ser omitido, mas deve-se descrever nas chaves install e remove o comando que se deseja executar para essas operações.
# O nome_pacote deve ser sempre informado, pois é usado para indicar dependências. 
# Quando informado apt, deve-se informar obrigatoriamente o nome de pacote pertencente aos repositórios do Ubuntu. 
# Quando informado dependency, deve-se declarar a entrada do pacote pai anteriormente.
# Para pacotes do repositório oficial do Ubuntu(informados com apt) e ppas o programa conhece a rotina de instalação e remoção.
# dependency, ppa, install e remove são opcionais.
"""


def capturar_diretorio():
    return argv[0].replace('instalador.py', '')


def abrir_gui():
    if len(argv) > 1:
        if argv[1] == 'g':
            return True
    return False


def main():
    diretorio = capturar_diretorio()
    lista_programas = gera_lista_programas(diretorio=diretorio, nome_arquivo='programas')

    if abrir_gui():
        InstaladorGUI(lista_programas, diretorio)
    else:
        InstaladorCLI(lista_programas, diretorio)


main()
