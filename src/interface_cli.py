# -*- coding: utf-8 -*-

from collections import OrderedDict
from os import system
try:
    from src.gerenciador_programas import verificar_programas_instalados, instalar_programa, remover_repositorio
except ImportError:
    from gerenciador_programas import verificar_programas_instalados, instalar_programa, remover_repositorio


def verificar_intervalo(valor: int, inicio: int, fim: int):
    if inicio <= valor <= fim:
        return True
    return False

def limpar_tela():
    system('clear')

def listar():
    print('listando programas')

def filtrar():
    print('filtrando programas')

def marcar_todos():
    print('marcando todos os programas')

def desmarcar_todos():
    print('desmarcando todos os programas')

def marcar_especifico():
    print('marcando programas especificos')

def marcar_em_lista():
    print('marcando em lista de programas')

def main():
    tela_inicial = '''INSTALADOR DE PROGRAMAS

    1 - Listar
    2 - Filtrar
    3 - Marcar todos
    4 - Desmarcar todos
    5 - Marcar específico
    6 - Marcar em lista
    0 - Sair

    : '''

    funcoes = {1: listar,
               2: filtrar,
               3: marcar_todos,
               4: desmarcar_todos,
               5: marcar_especifico,
               6: marcar_em_lista}

    while True:
        limpar_tela()
        escolha = input(tela_inicial)

        if escolha.isdigit():
            escolha = int(escolha)

            if verificar_intervalo(escolha, 0, 6):

                if escolha == 0:
                    limpar_tela()
                    print('\n\nEND OF LINE.\n')
                    break
                else:
                    funcoes[escolha]()

def instalador():
    main()


if __name__ == '__main__':
    instalador()
