# coding: utf-8

from collections import OrderedDict

dic_programas = OrderedDict()

dic_programas = OrderedDict()

diretorio = ''
with open(diretorio + 'programas') as f:
    for linha in f:
        # recortando laterais com espaços
        texto = linha.strip()

        if texto:
            # se inicia com #
            if texto.startswith('#'):
                chave = texto[1:]
                dic_programas[chave] = []
            else:
                dic_programas[chave].append(texto)

# ordenando o dicionário pela chave
dic_programas = OrderedDict(sorted(dic_programas.items()))

print(dic_programas, dic_programas.keys(), sep='\n')
