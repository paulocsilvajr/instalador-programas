# coding: utf-8

from collections import OrderedDict
from sys import argv


def capturar_diretorio():
    return argv[0].replace('instalador.py', '')


diretorio = capturar_diretorio()
