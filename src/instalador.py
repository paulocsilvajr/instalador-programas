# coding: utf-8

from sys import argv
try:
    from src.gerenciador_programas import gerar_dicionario_programas
    from src.interface_gui import Instalador as InstaladorGUI
    from src.interface_cli import instalador as InstaladorCLI
except ImportError:
    from gerenciador_programas import gerar_dicionario_programas
    from interface_gui import Instalador as InstaladorGUI
    from interface_cli import instalador as InstaladorCLI

__author__ = 'Paulo C. Silva Jr.'

__version__ = '0.3.2'

"""
Instalador de programas, desenvolvido: Ubuntu 16.04, Python3.5, Tkinter.
O arquivo programas deve ter entradas no seguinte formato:
#nome-programa
add-apt-repository ppa:repositorio -y; # incluido somente quando não está presente nos repositórios padrão.
apt install nome-programa -y; # 2 x ENTER
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
    dic_programas = gerar_dicionario_programas(diretorio + 'programas')

    if abrir_gui():
        InstaladorGUI(dic_programas, diretorio)
    else:
        InstaladorCLI(dic_programas, diretorio)

main()
