# coding: utf-8

from collections import OrderedDict
from os import popen
from subprocess import call


def verificar_arquivo(nome_arquivo: str,
                      comandos_gerenciadores: tuple=('apt', 'umake', 'pip2', 'pip3', 'add-apt-repository',
                                                     'sh', 'update-rc.d', 'service', 'chown')):
    """ Verificador das entradas usados para instalar programas.
    :param nome_arquivo: nome do arquivo com lista de programas.
    :param comandos_gerenciadores: Nome dos gerenciadores de pacote, gerenciador de repositório e outros.
    :return: ValueError: caso encontre algum erro, None: caso arquivo esteja correto. """
    assert isinstance(nome_arquivo, str), 'Parâmetro nome_arquivo requer uma string.'

    with open(nome_arquivo) as f:
        cont_linha = 0
        cont_linha_cabecalho = 0
        cont = {'cabecalho': 0, 'conteudo': 0}
        for linha in f:
            cont_linha += 1
            linha = linha.strip()

            if linha.startswith('#'):
                cont['cabecalho'] += 1
                cont_linha_cabecalho = cont_linha
            elif linha.startswith(comandos_gerenciadores) and linha.endswith(';'):
                cont['conteudo'] += 1
            else:
                if cont['cabecalho'] != 1 and cont['conteudo'] < 1:
                    raise ValueError('Conteúdo do arquivo {0} está inválido, linha {1} à {2}'.
                                     format(nome_arquivo, cont_linha_cabecalho, cont_linha))
                else:
                    cont['cabecalho'] = 0
                    cont['conteudo'] = 0


def gerar_dicionario_programas(nome_arquivo: str):
    """ Gerador de dicionário de programas baseado no arquivo informado.
    :param nome_arquivo: Nome do arquivo com lista de programas.
    :return: Dicionário usado para instalação de programas. """
    assert isinstance(nome_arquivo, str), 'Parâmetro nome_arquivo requer uma string.'

    # verificação do arquivo base
    verificar_arquivo(nome_arquivo)

    dic_programas = OrderedDict()

    with open(nome_arquivo) as f:
        chave = ''
        for linha in f:
            # recortando laterais com espaços
            linha = linha.strip()

            if linha:
                # se inicia com #
                if linha.startswith('#'):
                    chave = linha[1:]
                    dic_programas[chave] = []
                else:
                    dic_programas[chave].append(linha)

    # ordenando o dicionário pela chave
    return OrderedDict(sorted(dic_programas.items()))


def verificar_programas_instalados(dic_programas: OrderedDict, diretorio: str=''):
    """ Verifica se os programas informados em dic_programas estão instalados.
    :param dic_programas: Dicionário de programas.
    :param diretorio: diretorio para execução do script isinstalled.sh.
    :return: Lista com valores booleano. True: programa desintalado, False: programa instalado.
             Usado para marcar checkbox de instalação. """
    assert isinstance(dic_programas, (OrderedDict)), 'Parâmentro dic_programas requer um OrderedDict'

    resultado = []

    for i, programa in enumerate(dic_programas):
        marcar_para_instalar = True

        for comando in dic_programas[programa]:
            if 'apt install' in comando:
                pacote = comando.replace('apt install ', '').replace(' -y;', '')

                if popen(diretorio + 'isinstalled.sh ' + pacote).readlines():
                    marcar_para_instalar = False
                    print('Instalado:   ', pacote)
                else:
                    # caso algum pacote não esteja instalado, deixa marcado o combobox e sai do laço de
                    # verificação dos pacotes referentes ao programa.
                    marcar_para_instalar = True

                    print('Desinstalado:', pacote)
                    break

        # marca ou desmarca o programa de acordo com a análise feita do laço.
        resultado.append(marcar_para_instalar)

    return resultado


def executar_comando(comando: str, shell=True):
    """ Executa comandos no terminal linux.
    :param comando: comando que será executado.
    :param shell: retorno no shell.
    :return: código de retorno da função call(). """
    assert isinstance(comando, str), 'Parâmentro comando requer uma string.'

    return call(comando, shell=shell)


def instalar_programa(comando: str, remover=False):
    """ Função para instalar e remover programas.
    :param comando: instrução para instalação.
    :param remover: True quando deseja remover ao invés de instalar.
    :return: código de retorno e comando para remoção do repositório. """
    repositorio = ''
    return_code = 0

    if not remover:
        # Instalação
        print(comando)
        return_code = executar_comando(comando)
    else:
        # Desinstalação
        if 'add-apt-repository' in comando:
            repositorio = comando[:-1] + " --remove;"
            comando = ""
        elif 'apt install' in comando:
            comando = comando.replace('apt install', 'apt remove')
        else:
            comando = ""

        if comando:
            print(comando)
            return_code = executar_comando(comando)

    return return_code, repositorio


def remover_repositorio(repositorio: str):
    """ Função para remover repositório.
    :param repositorio: repositório gerado no retorno de instalar_programa.
    :return: código de retorno. """
    return executar_comando(repositorio)


if __name__ == '__main__':
    # testes
    DIRETORIO = ''
    DIC_PROGRAMAS = gerar_dicionario_programas(DIRETORIO + 'programas')
    print(DIC_PROGRAMAS, DIC_PROGRAMAS.keys(), len(DIC_PROGRAMAS.keys()), sep='\n')
    resultado = verificar_programas_instalados(DIC_PROGRAMAS, '/home/paulo/pc/python/instalador-programas/src/')
    print(resultado, len(resultado), sep='\n')
