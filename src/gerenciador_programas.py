from subprocess import call
from datetime import datetime
from os import popen
from operator import attrgetter

DESCRICAO = '#'
PACOTE = 'pacote'
APT = 'apt'
EXTRA_INSTALL = 'install'
EXTRA_REMOVE = 'remove'
PPA = 'ppa'
DEPENDENCIA = 'dependencia'

SEPARADOR = '::'

LISTA_CHAVES = [
    DESCRICAO,
    PACOTE,
    APT,
    EXTRA_INSTALL,
    EXTRA_REMOVE,
    PPA,
    DEPENDENCIA
]

ARQUIVO_LOG = 'log'


def log(pacote: str, comando: str, codigo):
    agora = datetime.now().strftime("%Y%m%d:%H%M%S")
    mensagem = '{} {}: {} [{}]'.format(agora, pacote, comando, codigo)

    with open(ARQUIVO_LOG, 'a') as f:
        f.write(mensagem + '\n')


def executa_comando(pacote: str, comando: str, shell: bool) -> int:
    print("{}: {}".format(pacote, comando))
    # codigo = call(comando, shell=shell)
    codigo = 0

    log(pacote, comando, codigo)

    return codigo


def gera_lista_programas(nome_arquivo: str) -> list:
    lista_programas = list()

    with open(nome_arquivo) as f:
        programa = Programa()

        for linha in f:
            linha = linha.strip().split(SEPARADOR)

            chave = linha[0]

            if chave.startswith(DESCRICAO):
                descricao = chave[1:]

                programa.descricao = descricao

            elif chave == PACOTE:
                if linha[1] == APT:
                    apt = True
                    pacote = linha[2]
                else:
                    apt = False
                    pacote = linha[1]

                programa.apt = apt
                programa.pacote = pacote

            elif chave == DEPENDENCIA:
                for pacote in linha[1:]:
                    dep_programa = list(filter(lambda prog: prog.pacote == pacote, lista_programas))[0]
                    programa.dependencias = dep_programa

            elif chave == EXTRA_INSTALL:
                programa.extra_install = linha[1]

            elif chave == EXTRA_REMOVE:
                programa.extra_remove = linha[1]

            elif chave == PPA:
                programa.ppa = linha[1]

            elif not chave:
                lista_programas.append(programa)
                programa = Programa()

    lista_programas.sort(key=attrgetter('descricao'))

    return lista_programas


def verifica_programas_instalados(lista_programas: list, diretorio: str = ''):
    """ Verifica se os programas informados em dic_programas estão instalados.
    :param dic_programas: Dicionário de programas.
    :param diretorio: diretorio para execução do script isinstalled.sh.
    :return: Lista com valores booleano. True: programa desintalado, False: programa instalado.
             Usado para marcar checkbox de instalação. """
    assert isinstance(lista_programas, list), 'Parâmentro lista_programas requer uma lista contendo Programas'

    resultado = []

    for programa in lista_programas:
        pacote = programa.pacote

        if popen(diretorio + 'isinstalled.sh ' + pacote).readlines():
            marcar_para_instalar = False
            print('Instalado:   ', pacote)
        else:
            # caso algum pacote não esteja instalado, deixa marcado o combobox e sai do laço de
            # verificação dos pacotes referentes ao programa.
            marcar_para_instalar = True

            print('Desinstalado:', pacote)

        # marca ou desmarca o programa de acordo com a análise feita do laço.
        resultado.append(marcar_para_instalar)

    return resultado


class Programa:
    def __init__(self):
        self.__descricao = ''
        self.__pacote = ''
        self.__install = list()
        self.__remove = list()
        self.__ppa = str()
        self.__dependencias = list()
        self.__apt = False

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def pacote(self) -> str:
        return self.__pacote

    @pacote.setter
    def pacote(self, pacote: str):
        self.__pacote = pacote

        if self.__apt:
            self.__install.append(self._apt_install())
            self.__remove.append(self._apt_remove())

    @property
    def apt(self) -> bool:
        return self.__apt

    @apt.setter
    def apt(self, apt: bool):
        self.__apt = apt

    @property
    def dependencias(self):
        return self.__dependencias[:]

    @dependencias.setter
    def dependencias(self, dependencia):
        self.__dependencias.append(dependencia)

    @property
    def ppa(self) -> str:
        return self.__ppa

    @ppa.setter
    def ppa(self, ppa):
        self.__ppa = ppa

    @property
    def extra_install(self):
        return self.__install[:]

    @extra_install.setter
    def extra_install(self, extra: str):
        self.__install.append(extra)

    @property
    def extra_remove(self):
        return self.__remove[:]

    @extra_remove.setter
    def extra_remove(self, extra: str):
        self.__remove.append(extra)

    def _apt_install(self) -> str:
        return 'apt install {} -y;'.format(self.__pacote)

    def _apt_remove(self) -> str:
        return 'apt remove {} -y;'.format(self.__pacote)

    def _apt_update(self) -> str:
        return 'apt update;'

    def _add_ppa(self) -> str:
        return 'add-apt-repository {} -y;'.format(self.__ppa)

    def _del_ppa(self) -> str:
        return 'add-apt-repository {} -r -y;'.format(self.__ppa)

    def install(self, shell=True) -> list:
        cod_retorno = list()

        if self.__dependencias:
            for programa in self.__dependencias:
                codigo = programa.install()
                cod_retorno.extend(codigo)

        if self.__ppa:
            codigo = executa_comando(self.__pacote, self._add_ppa(), shell)
            cod_retorno.append(codigo)

            codigo = executa_comando(self.__pacote, self._apt_update(), shell)
            cod_retorno.append(codigo)

        for comando in self.__install:
            codigo = executa_comando(self.__pacote, comando, shell)
            cod_retorno.append(codigo)

        return cod_retorno

    def remove(self, shell=True) -> list:
        cod_retorno = list()

        for comando in reversed(self.__remove):
            codigo = executa_comando(self.__pacote, comando, shell)
            cod_retorno.append(codigo)

        if self.__ppa:
            codigo = executa_comando(self.__pacote, self._del_ppa(), shell)
            cod_retorno.append(codigo)

            codigo = executa_comando(self.__pacote, self._apt_update(), shell)
            cod_retorno.append(codigo)

        return cod_retorno

    def __str__(self):
        return self.__descricao


if __name__ == '__main__':
    lista = gera_lista_programas('../programas.novo')

    for i in lista:
        i.install()
        print()
        i.remove()
        print('----------------------------')

    pass
