# -*- coding: utf-8 -*-

from os import system

try:
    from src.gerenciador_programas import verifica_programas_instalados
except ImportError:
    from gerenciador_programas import verifica_programas_instalados

# Marcação inicial dos programas, quando 1, todos ficam marcados,
# enquanto 0, todos desmarcados.
MARCAR_TODOS = 0


def _definir_marca(lista_programas, check, codigo, simnao='[S/n]'):
    if check[codigo] == 0:
        msg = 'Marcar'
        marca = 1
    else:
        msg = 'Desmarcar'
        marca = 0

    resposta = input("{0} '{1}' {2}: ".format(msg, lista_programas[codigo], simnao))

    if not resposta.lower().startswith('s'):
        marca = not marca

    check[codigo] = marca

    return resposta


def _marcar_item(lista_programas, diretorio, check):
    codigo = input('\nInforme o número do programa: ')

    if codigo.isdigit():
        codigo = int(codigo)
        if verificar_intervalo(codigo, 1, len(lista_programas)):
            _definir_marca(lista_programas=lista_programas,
                           check=check,
                           codigo=codigo - 1)


def _marcar(check, marcar):
    """ Função usada em marcar_todos e desmarcar_todos para modificar o estado de cada posição de check. """
    limpar_tela()

    print('{}arcando todos os programas'.format('M' if marcar else 'Desm'))
    for i in range(len(check)):
        check[i] = marcar

    pausar()


def verificar_intervalo(valor: int, inicio: int, fim: int):
    if inicio <= valor <= fim:
        return True
    return False


def limpar_tela():
    system('clear')


def carregar_logo(diretorio):
    """ Carrega o logo em ASCII de acordo com arquivo logo.
    :param diretorio: Path default do arquivo.
    :return: logo em modo texto. """
    f = open(diretorio + 'logo', mode='r')
    logo = ''
    for linha in f:
        logo += linha

    return logo


def pausar(mensagem='\nENTER para continuar '):
    while True:
        entrada = input(mensagem)

        if not entrada:
            break


def listar(lista_programas, diretorio, check):
    """ Listagem de todos os programas com as check/marcação( Sim/no ) de cada um. """
    limpar_tela()

    somente_marcados = False
    if not all(check) and any(check):
        somente_marcados = True if input('Listar somente marcados[S/n]: ').lower() == 's' else False
        limpar_tela()

    tamanho = len(str(len(lista_programas)))
    quantidade = len(lista_programas)

    for i, programa in enumerate(lista_programas, start=1):
        if somente_marcados:
            if i == 1:
                print('LISTA DE PROGRAMAS MARCADOS({})'.format(sum(check)))

            if check[i - 1] == 1:
                print('    {0:0>{1}}: {2:.<50} INSTALAR( {3} )'.format(i, tamanho, programa.descricao,
                                                                       'S' if check[i - 1] else 'n'))
        else:
            if str(i).endswith('1'):
                ultimo = i + 9
                if ultimo > quantidade:
                    ultimo = quantidade

                print('LISTA DE PROGRAMAS({0}-{1}) de {2}:\n'.format(i, ultimo, quantidade))

            print('    {0:0>{1}}: {2:.<50} INSTALAR( {3} )'.format(i, tamanho, programa.descricao,
                                                                   'S' if check[i - 1] else 'n'))
            if not i % 10:
                entrada = input('\nENTER para mais 10 itens ou q+ENTER para finalizar lista ').lower()

                if entrada == 'q':
                    break

                limpar_tela()

        if i == len(lista_programas):
            pausar()


def marcar_por_filtro(lista_programas, diretorio, check):
    limpar_tela()

    filtro = input('Informe o nome do programa: ')

    programas_filtro = tuple(k.descricao.lower() for k in lista_programas if filtro.lower() in k.descricao.lower())

    for i, programa in enumerate(lista_programas):
        if programa.descricao.lower() in programas_filtro:
            retorno = _definir_marca(lista_programas=lista_programas,
                                     check=check,
                                     codigo=i,
                                     simnao='[S/n/q]')

            if retorno.lower() == 'q':
                break

    pausar()


def marcar_todos(lista_programas, diretorio, check):
    _marcar(check=check, marcar=1)


def desmarcar_todos(lista_programas, diretorio, check):
    _marcar(check=check, marcar=0)


def marcar_especifico(lista_programas, diretorio, check):
    """ Função para marcar um programa com código específico para instalar/remover. """
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
         lista_programas=lista_programas,
         diretorio=diretorio,
         check=check)


def marcar_em_lista(lista_programas, diretorio, check):
    """ Função para marcar quais programas serão instalados/removidos de acordo com a lista de programas. """
    limpar_tela()

    for i, programa in enumerate(lista_programas):
        retorno = _definir_marca(lista_programas=lista_programas,
                                 check=check,
                                 codigo=i,
                                 simnao='[S/n/q]')

        if retorno.lower() == 'q':
            pausar()
            break


def desmarcar_instalados(lista_programas, diretorio, check):
    limpar_tela()

    print("Desmarcando programas instalados.")

    if input("Este processo pode demorar dependendo da quantidade de programas listados,"
             "\nContinuar[S/n]? ").lower() == 's':
        marcacoes = verifica_programas_instalados(lista_programas, diretorio)

        for i, marcar in enumerate(marcacoes):
            # marca ou desmarca o programa de acordo com a análise feita do laço.
            check[i] = marcar

        pausar()


def instalar(lista_programas, diretorio, check, remover=False):
    """ Função para instalar/desinstalar os programas. """
    limpar_tela()

    tarefa = "Instal" if not remover else "Desinstal"

    quant_programas = sum(check)
    if quant_programas:
        if input('Deseja realmente {0}ar {1} marcados[S/n]: '.
                 format(tarefa.lower(),
                        'os {} programas'.format(quant_programas) if quant_programas > 1 else 'o programa')) \
                .lower() == 's':

            print('{}ando programas:'.format(tarefa))

            for i, programa in enumerate(lista_programas):
                if check[i]:
                    if remover:
                        return_code = programa.remove()
                    else:
                        return_code = programa.install()

                    if any(return_code):
                        print("Atenção", "{0} de {1} com erro(s)\nVerifique o log".format(tarefa + 'ação', programa))
                    else:
                        check[i] = 0

            pausar()
    else:
        print('Marque programas para {}ar'.format(tarefa.lower()))
        pausar()


def desinstalar(lista_programas, diretorio, check):
    """ Função para desinstalar os programas. Usa a função instalar com o parametro remover=True. """
    instalar(lista_programas, diretorio, check, remover=True)


def opcao_invalida(escolha):
    print('\nOpção inválida({})'.format(escolha))
    pausar()


def menu(texto, mensagem_fim, funcoes, inicio, fim, **kwargs):
    """ Função para apresentar os menus da interface, com verificação de intervalo.
    :param texto: Opção para o menu, usar números para representar-las.
    :param mensagem_fim: Mensagem quando vai para a opção 0(sair).
    :param funcoes: Lista de funções que serão invocadas.
    :param inicio: Menor valor as opções, geralmente o 0.
    :param fim: Maior valor das opçoes.
    :param kwargs: Parâmetros das funções:
                        lista_programas,
                        diretorio,
                        check
    :return: None. """
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


def main(lista_programas: list, diretorio: str):
    """ Função inicial e principal do CLI, contendo as opções de manipulação dos programas. """
    logo = carregar_logo(diretorio)
    tela_inicial = logo + '''\nInterface para o apt para facilitar a instalação de programas 
em distribuições baseadas no Ubuntu.

Desenvolvido por Paulo C. Silva Jr

    1 - Listar
    2 - Marcar todos
    3 - Desmarcar todos
    4 - Marcar por filtro
    5 - Marcar específico
    6 - Marcar em lista
    7 - Desmarcar programas instalados
    8 - Instalar
    9 - Desinstalar
    0 - Sair

    : '''

    funcoes = {1: listar,
               2: marcar_todos,
               3: desmarcar_todos,
               4: marcar_por_filtro,
               5: marcar_especifico,
               6: marcar_em_lista,
               7: desmarcar_instalados,
               8: instalar,
               9: desinstalar}

    # variável que representa os programas marcados
    check = [MARCAR_TODOS] * len(lista_programas)

    menu(texto=tela_inicial,
         mensagem_fim='\n\nEND OF LINE.\n',
         funcoes=funcoes,
         inicio=0,
         fim=9,
         lista_programas=lista_programas,
         diretorio=diretorio,
         check=check)


def instalador(lista_programas: list, diretorio: str):
    """ Função que captura as variáveis enviadas pelo instalador.py
    :param lista_programas: Lista de programas ordenado.
    :param diretorio: Diretório usado pela função desmarcar_intalados.
    :return: None. """
    main(lista_programas=lista_programas, diretorio=diretorio)
