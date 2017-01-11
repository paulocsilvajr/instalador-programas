# coding: utf-8

from collections import OrderedDict


def verificar_arquivo(nome_arquivo: str,
                      comandos_gerenciadores: tuple=('apt', 'umake', 'pip2', 'pip3', 'add-apt-repository', 'sh')):
    """ Verificador das entradas usados para instalar programas.
    :param nome_arquivo: nome do arquivo com lista de programas.
    :param comandos_gerenciadores: Nome dos gerenciadores de pacote, gerenciador de repositório e outros.
    :return: ValueError: caso encontre algum erro, None: caso arquivo esteja correto. """
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
    assert isinstance(nome_arquivo, str), 'Parametro nome_arquivo requer uma string.'

    # verificação do arquivo base
    verificar_arquivo(nome_arquivo)

    dic_programas = OrderedDict()

    with open(nome_arquivo) as f:
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

if __name__ == '__main__':
    DIRETORIO = ''
    DIC_PROGRAMAS = gerar_dicionario_programas(DIRETORIO + 'programas')
    print(DIC_PROGRAMAS, DIC_PROGRAMAS.keys(), sep='\n')
