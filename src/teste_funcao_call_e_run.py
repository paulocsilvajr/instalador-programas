#!/usr/bin/env python3
# coding: utf-8

from subprocess import call, run
import sys


def formatar_vermelho(texto: str) -> str:
    return f'\033[0;31m{texto}\033[0m'


def formatar_azul(texto: str) -> str:
    return f'\033[0;34m{texto}\033[0m'


def executar_comando(funcao, str_comando: str):
    largura = 80
    linha = largura * '-'
    linha_grossa = largura * '='

    print(formatar_azul(linha_grossa))
    str_funcao = f'{funcao.__name__}(\'{str_comando}\')'
    print(formatar_vermelho(str_funcao))
    print(linha)
    retorno = funcao(str_comando, shell=True)
    print(linha)
    print(f'Retorno do comando: {retorno}')
    print(formatar_azul(linha_grossa))


if __name__ == '__main__':
    comando = ' '.join(sys.argv[1:])
    if comando:
        print(f"Comando informado: {formatar_vermelho(comando)}")

        executar_comando(call, comando)
        print()
        executar_comando(run, comando)

        exit(0)
    exit(1)
