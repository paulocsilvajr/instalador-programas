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


def pausar(mensagem='\nENTER para continuar '):
    while True:
        entrada = input(mensagem)

        if not entrada:
            break


def listar(dic_programas, diretorio, check):
    limpar_tela()

    tamanho = len(str(len(dic_programas)))
    for i, chave in enumerate(dic_programas, start=1):
        if str(i).endswith('1'):
            print('LISTA DE PROGRAMAS({0}-{1}) de {2}:\n'.format(i, i+9, len(dic_programas)))

        print('    {0:0>{1}}: {2:.<50} INSTALAR({3})'.format(i, tamanho, chave,
                                                            'Y' if check[i-1] else 'n'))

        if not i % 10:
            entrada = input('\nENTER para mais 10 itens ou q+ENTER para finalizar lista ').lower()

            if entrada == 'q':
                break

            limpar_tela()

        if i == len(dic_programas):
            pausar()


def filtrar(dic_programas, diretorio, check):
    print('filtrando programas')


def _marcar(check, marcar):
    limpar_tela()

    print('Marcando todos os programas')
    for i in range(len(check)):
        check[i] = marcar

    pausar()


def marcar_todos(dic_programas, diretorio, check):
    _marcar(check=check, marcar=1)


def desmarcar_todos(dic_programas, diretorio, check):
    _marcar(check=check, marcar=0)


def _marcar_item(dic_programas, diretorio, check):
    codigo = input('\nInforme o número do programa: ')

    if codigo.isdigit():
        codigo = int(codigo)
        if verificar_intervalo(codigo, 1, len(dic_programas)):
            if check[codigo-1] == 0:
                msg = 'Marcar'
                marca = 1
            else:
                msg = 'Desmarcar'
                marca = 0

            resposta = input("{0} '{1}' [Y/n]: ".format(msg, list(dic_programas.keys())[codigo-1]))

            if not resposta.lower().startswith('y'):
                marca = not marca

            check[codigo-1] = marca


def marcar_especifico(dic_programas, diretorio, check):
    txt_menu = '''Marcar programas especificos:

    1 - Listar programas
    2 - Marcar
    0 - Voltar

    : '''

    funcoes = {1: listar, 2: _marcar_item}

    limpar_tela()

    menu(texto=txt_menu,
         mensagem_fim='',
         funcoes=funcoes,
         dic_programas=dic_programas,
         diretorio=diretorio,
         check=check)


def marcar_em_lista(dic_programas, diretorio, check):
    print('marcando em lista de programas')


def instalar(dic_programas, diretorio, check):
    print('instalando programas')


def desinstalar(dic_programas, diretorio, check):
    print('desinstalalando programas')


def opcao_invalida(escolha):
    print('\nOpção inválida({})'.format(escolha))
    pausar()


def menu(texto, mensagem_fim, funcoes, **kwargs):
    while True:
        limpar_tela()
        escolha = input(texto)

        if escolha.isdigit():
            escolha = int(escolha)

            if verificar_intervalo(escolha, 0, 6):

                if escolha == 0:
                    limpar_tela()
                    print(mensagem_fim)
                    break
                else:
                    funcoes[escolha](**kwargs)
            else:
                opcao_invalida(escolha)
        else:
            opcao_invalida(escolha)


def main(dic_programas: OrderedDict, diretorio: str):
    tela_inicial = '''INSTALADOR DE PROGRAMAS

    1 - Listar
    2 - Filtrar
    3 - Marcar todos
    4 - Desmarcar todos
    5 - Marcar específico
    6 - Marcar em lista
    7 - Instalar
    8 - Desinstalar
    0 - Sair

    : '''

    funcoes = {1: listar,
               2: filtrar,
               3: marcar_todos,
               4: desmarcar_todos,
               5: marcar_especifico,
               6: marcar_em_lista,
               7: instalar,
               8: desinstalar}

    check = [1] * len(dic_programas)

    menu(texto=tela_inicial,
         mensagem_fim='\n\nEND OF LINE.\n',
         funcoes=funcoes,
         dic_programas=dic_programas,
         diretorio=diretorio,
         check=check)


def instalador(dic_programas: OrderedDict, diretorio: str):
    main(dic_programas=dic_programas, diretorio=diretorio)

