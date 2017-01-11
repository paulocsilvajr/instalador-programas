# coding: utf-8

from collections import OrderedDict
from sys import argv
from src.gerenciador_programas import gerar_dicionario_programas
from src.interface_grafica import Instalador


def capturar_diretorio():
    return argv[0].replace('instalador.py', '')


def main():
    # diretorio = capturar_diretorio()
    diretorio = '/home/paulo/pc/python/instalador-programas/src/'
    dic_programas = gerar_dicionario_programas(diretorio + 'programas')
    Instalador(dic_programas, diretorio)


main()


