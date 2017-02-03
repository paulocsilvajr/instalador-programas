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

        print('    {0:0>{1}}: {2:.<50} INSTALAR( {3} )'.format(i, tamanho, chave,
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

    print('{}arcando todos os programas'.format('M' if marcar else 'Desm'))
    for i in range(len(check)):
        check[i] = marcar

    pausar()


def marcar_todos(dic_programas, diretorio, check):
    _marcar(check=check, marcar=1)


def desmarcar_todos(dic_programas, diretorio, check):
    _marcar(check=check, marcar=0)


def _definir_marca(dic_programas, check, codigo, simnao='[Y/n]'):
    if check[codigo] == 0:
        msg = 'Marcar'
        marca = 1
    else:
        msg = 'Desmarcar'
        marca = 0

    resposta = input("{0} '{1}' {2}: ".format(msg, list(dic_programas.keys())[codigo], simnao))

    if not resposta.lower().startswith('y'):
        marca = not marca

    check[codigo] = marca

    return resposta


def _marcar_item(dic_programas, diretorio, check):
    codigo = input('\nInforme o número do programa: ')

    if codigo.isdigit():
        codigo = int(codigo)
        if verificar_intervalo(codigo, 1, len(dic_programas)):
            _definir_marca(dic_programas=dic_programas,
                           check=check,
                           codigo=codigo-1)


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
         inicio=0,
         fim=2,
         dic_programas=dic_programas,
         diretorio=diretorio,
         check=check)


def marcar_em_lista(dic_programas, diretorio, check):
    limpar_tela()

    for i, chave in enumerate(dic_programas):
        retorno = _definir_marca(dic_programas=dic_programas,
                                 check=check,
                                 codigo=i,
                                 simnao='[Y/n/q]')

        if retorno.lower() == 'q':
            pausar()
            break


def instalar(dic_programas, diretorio, check, remover=False):
    limpar_tela()

    tarefa = "Instal" if not remover else "Desinstal"

    print('{}ando programas:'.format(tarefa), end='')

    for i, programa in enumerate(dic_programas):
        repositorio = ""
        if check[i]:
            for comando in dic_programas[programa]:
                msg = tarefa + "ando " + programa
                print('\n\n{}'.format(msg))

                return_code, repositorio = instalar_programa(comando, remover)

                print(return_code)

                if return_code:
                    print("Atenção", "{0} de {1} interrompida".format(tarefa + 'ação', programa))
        # Remoção do repositório, depois da desinstalação do programa, caso tenha sido adicionado.
        if repositorio:
            print("Removendo repositório %s\n" % repositorio)
            return_code = remover_repositorio(repositorio)
            print(return_code)

    pausar()


def desinstalar(dic_programas, diretorio, check):
    instalar(dic_programas, diretorio, check, remover=True)


def opcao_invalida(escolha):
    print('\nOpção inválida({})'.format(escolha))
    pausar()


def menu(texto, mensagem_fim, funcoes, inicio, fim, **kwargs):
    while True:
        limpar_tela()
        escolha = input(texto)

        if escolha.isdigit():
            escolha = int(escolha)

            if verificar_intervalo(escolha, inicio, fim):

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
         inicio=0,
         fim=8,
         dic_programas=dic_programas,
         diretorio=diretorio,
         check=check)


def instalador(dic_programas: OrderedDict, diretorio: str):
    main(dic_programas=dic_programas, diretorio=diretorio)
