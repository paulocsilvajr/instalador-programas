#!/usr/bin/python3
# coding: utf-8

import tkinter
from tkinter.messagebox import showerror, askyesno, showinfo
from tkinter import ttk
from collections import OrderedDict
from re import findall

try:
    from src.gerenciador_programas import verificar_programas_instalados, instalar_programa, remover_repositorio
except ImportError:
    from gerenciador_programas import verificar_programas_instalados, instalar_programa, remover_repositorio


class Instalador(tkinter.Tk):
    """ Interface gráfica do instaldor. """

    def __init__(self, dic_programas: OrderedDict, diretorio: str):
        # Construtor(classe pai: tkinter.Tk) e configurações da janela.
        super(Instalador, self).__init__()

        self.dic_programas = dic_programas
        self.diretorio = diretorio
        self.texto_pesquisa = tkinter.StringVar()
        self.checkbutton = []  # lista de checkbox para os programas

        self.fonte = 'Ubuntu 12'

        self._style()

        self.title('Instalador de programas')

        # Por padrão, quando inicializado, todos os programas estão marcados.
        # Para mudar o padrão, mude o atributo marcar_todos por 0.
        self.marcar_todos = 0  # default 1.

        # Componentes do formulário.
        self._label(master=self, text="Marque os programas que deseja instalar")

        # edit para pesquisa e botão pesquisar
        frame1 = self._frame(master=self, side=tkinter.TOP, fill=tkinter.X,
                             padx=2.5, pady=2.5)
        campo_pesquisa = self._edit(master=frame1, textvariable=self.texto_pesquisa)
        self.pesquisa_default = 'Filtre por um nome de programa'
        self.texto_pesquisa.set(self.pesquisa_default)

        self._button(master=frame1, text='Pesquisar', command=self.pesquisar, underline=0,
                     side=tkinter.LEFT, fill=tkinter.Y, padx=2.5, expand=0)


        # lista de programas com checkbuttons e scrollbar
        self.frame_programas, self.text_programas = \
            self._lista_programas(master=self, side=tkinter.TOP, fill=tkinter.BOTH, expand=1,
                                  padx=5, pady=2.5)

        # frame para botões reverter seleção e desmarcar seleção que ficam lado a lado
        frame2 = self._frame(master=self, side=tkinter.TOP, fill=tkinter.X,
                             padx=2.5, pady=2.5)

        # botões de seleção
        self._button(master=frame2, text='Reverter seleção', command=self.reverter,
                     side=tkinter.LEFT, fill=tkinter.X, padx=2.5, expand=1)

        txt_btn_marcar_todos = "Desmarcar todos" if self.marcar_todos else "Marcar todos"
        self.btn_marcar_todos = self._button(master=frame2, text=txt_btn_marcar_todos, command=self.selecionar,
                                             side=tkinter.RIGHT, fill=tkinter.X, padx=2.5, expand=1)

        # Botões de controle de instalação
        self._button(master=self, text="Desmarcar instalados",
                     command=self.desmarcar_instalados, style="C.TButton", underline=1,
                     side=tkinter.TOP, fill=tkinter.X, padx=5, pady=2.5)

        self._button(master=self, text="Instalar",
                     command=self.instalar, style="C.TButton", underline=0,
                     side=tkinter.TOP, fill=tkinter.X, padx=5, pady=2.5)

        self._button(master=self, text="Desinstalar",
                     command=self.desinstalar, style="D.TButton", underline=0,
                     side=tkinter.TOP, fill=tkinter.X, padx=5, pady=2.5)

        self.lbl_status = self._label(master=self, text="Sempre execute este programa como administrador.")

        # Centralizando formulário.
        dimensao = (500, 600)
        self.wm_geometry('%dx%d-%d-%d' % (dimensao[0], dimensao[1],
                                          (self.winfo_screenwidth() / 2) - (dimensao[0] / 2),
                                          self.winfo_screenheight()))

        # Definindo tamanho mínimo do formulário
        self.minsize(400, 525)

        # Eventos do formulário.
        self.bind('<Escape>', self.atalho_fechar)
        self.protocol('WM_DELETE_WINDOW', self.fechar)
        self.bind('<Alt-i>', self.atalho_instalar)
        self.bind('<Alt-d>', self.atalho_desintalar)
        self.bind('<Alt-e>', self.atalho_desmarcar_instalados)
        self.bind('<Alt-p>', self.atalho_pesquisar)
        campo_pesquisa.bind('<Return>', self.atalho_pesquisar)
        campo_pesquisa.bind('<Button-1>', self.limpar_pesquisa)

        # Loop do formulário.
        self.mainloop()

    def _posicao_programa(self, programa):
        for i, chave in enumerate(self.dic_programas.keys()):
            if chave == programa:
                return i

    def limpar_pesquisa(self, event=None):
        self.texto_pesquisa.set('')

    def pesquisar(self):
        filtro = self.texto_pesquisa.get()

        if filtro == self.pesquisa_default:
            filtro = ''

        self.text_programas.configure(state='normal')
        self.text_programas.delete('1.0', tkinter.END)

        if not filtro:
            filtro = 'Todos'

            self.adicionar_check_programas(self.frame_programas, self.text_programas, self.dic_programas.keys())
        else:
            pass
            dic_temp = []

            for programa in self.dic_programas.keys():
                if filtro in programa:
                    dic_temp.append(programa)

            self.adicionar_check_programas(self.frame_programas, self.text_programas, dic_temp)

        self.text_programas.configure(state='disabled')

        self.limpar_pesquisa()

        self.lbl_status['text'] = 'Filtro: ' + filtro

    def atalho_pesquisar(self, event):
        self.pesquisar()

    def clique_checkbutton(self, event):
        """ Função para marcar as dependências dos pacotes.
        :param event: Evento invocado, usado para identificar o componente(CheckButton) clicado.
        :return: None. """
        programa = event.widget['text']
        dependencias = programa.split(':')[:-1]

        # se o programa NÃO está marcado, verifica dependencias.
        if not self.checkbutton[self._posicao_programa(programa)].get():
            if dependencias:
                for i, chave in enumerate(self.dic_programas.keys()):
                    descricao = findall('\(.+\)', chave)
                    if descricao:
                        chave = chave.replace(descricao[0], '')

                    if chave in dependencias:
                        self.checkbutton[i].set(1)

    def fechar(self):
        """ Fecha o programa após confirmação.
        :return: None. """
        if askyesno("Confirmação", "Deseja realmente fechar o instalador?"):
            self.destroy()

    def atalho_fechar(self, event):
        """ Atalho para fechar o programa usado pelo .bind.
        :param event: evento invocado
        :return: None. """
        self.fechar()

    def instalar(self):
        """ Ação do botão instalar.
        :return: None. """
        self.instalacao()

    def desinstalar(self):
        """ Ação do botão desinstalar. Usa o parâmetro remover para ativar o recurso de desinstalação.
        :return: None. """
        self.instalacao(remover=True)

    def desmarcar_instalados(self):
        """ Ação do botão marcar instalados. Analiza o sistema e desmarca os programas instalados.
         :return: None. """

        self.lbl_status['text'] = "Desmarcando programas instalados."

        if askyesno("Atenção", "Este processo pode demorar dependendo da quantidade de programas listados,"
                               "\nContinuar?"):
            marcacoes = verificar_programas_instalados(self.dic_programas, self.diretorio)

            for i, marcar in enumerate(marcacoes):
                # marca ou desmarca o programa de acordo com a análise feita do laço.
                self.checkbutton[i].set(marcar)

    def instalacao(self, remover=False):
        """ Núcleo do programa instalador. Verifica quais programas estão marcados e instala/desinstala um a um.
        :param remover: Marcador para a função de desinstalar.
        :return: None. """
        tarefa = "Instal" if not remover else "Desinstal"

        # Variável temporária com os valores de self.checkbutton(status do chechbutton).
        temp = []
        for i in self.checkbutton:
            temp.append(i.get())

        # Verificação se existe pelo menos 1 item para instalar.
        if any(temp):
            if askyesno("Atenção", "Deseja realmente %sar todos os programas marcados?" % tarefa.lower()):
                for i, programa in enumerate(self.dic_programas):
                    repositorio = ""
                    if self.checkbutton[i].get():
                        for comando in self.dic_programas[programa]:
                            msg = tarefa + "ando " + programa
                            print(msg)
                            self.lbl_status['text'] = msg
                            # Sleep somente para atualizar self.lbl_status
                            # sleep(0.25)

                            return_code, repositorio = instalar_programa(comando, remover)

                            print(return_code)

                            if return_code:
                                showerror("Atenção", "%s de %s interrompida" %
                                          (tarefa + "ação", programa))
                            else:
                                self.lbl_status['text'] = "Finalizada a %s de %s" % (tarefa.lower() + "ação", programa)
                    # Remoção do repositório, depois da desinstalação do programa, caso tenha sido adicionado.
                    if repositorio:
                        print("Removendo repositório %s\n" % repositorio)
                        return_code = remover_repositorio(repositorio)
                        print(return_code)
        else:
            showinfo("Atenção", "Marque pelo menos um item para %sar" % tarefa.lower())

    def reverter(self):
        """ Reversão da marcação de programas.
        :return: None. """
        for i in range(len(self.checkbutton)):
            self.checkbutton[i].set(not self.checkbutton[i].get())

    def selecionar(self):
        """ Marcar ou desmarcar todos os programas.
        :return: None. """
        self.marcar_todos = not self.marcar_todos
        if self.marcar_todos:
            self.btn_marcar_todos['text'] = "Desmarcar todos"
        else:
            self.btn_marcar_todos['text'] = "Marcar todos "

        for i in range(len(self.checkbutton)):
            self.checkbutton[i].set(self.marcar_todos)

    def atalho_instalar(self, event):
        """ Atalho para instalação, usado pelo .bind.
        :param event: Evento invocado
        :return: None. """
        self.instalar()

    def atalho_desintalar(self, event):
        """ Atalho para desinstalação, usado pelo .bind.
        :param event: Evento invocado
        :return: None. """
        self.desinstalar()

    def atalho_desmarcar_instalados(self, event):
        self.desmarcar_instalados()

    def _style(self):
        self.style = ttk.Style()
        # self.style.theme_use('classic')
        self.style.theme_use('clam')

        cor_fundo = 'lightgray'
        # cor de fundo do tkinter.tk
        super().configure(background=cor_fundo)
        # self.style.configure('.', font=('Ubuntu', 12))  # ou
        self.style.configure('.', font=self.fonte, background=cor_fundo)  # cor de fundo do ttk
        # temas disponíveis
        # print(self.style.theme_names())

        # Para adicionar novos estilos personalizados, deve-se manter o nome do componente.
        # Ex: C.TButton, D.TButton
        self.style.map("C.TButton",
                       foreground=[('pressed', 'red'), ('active', 'blue')],
                       background=[('pressed', '!disabled', 'black'), ('active', 'darkgray')])
        self.style.map("D.TButton",
                       foreground=[('pressed', 'black'), ('active', 'red')],
                       background=[('pressed', '!disabled', 'red'), ('active', 'darkgray')])
        self.style.map("E.TCheckbutton",
                       background=[('active', 'darkgray'), ('!active', 'white')])

    def _edit(self, master, textvariable):
        edit = ttk.Entry(master=master, textvariable=textvariable, width=40, font=self.fonte)
        edit.pack(side=tkinter.LEFT, fill=tkinter.BOTH, padx=2.5)
        return edit

    def _label(self, master, text):
        label = ttk.Label(master=master, text=text)
        label.pack(side=tkinter.TOP, fill=tkinter.X, padx=5, pady=2.5)
        return label

    def _frame(self, master, side, fill, expand=0, padx=0.0, pady=0.0):
        frame = ttk.Frame(master=master)
        frame.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady)
        return frame

    def _button(self, master, command, text, side, fill, expand=0, underline=None, style='TButton', padx=0.0, pady=0.0):
        buttom = ttk.Button(master=master, text=text, command=command, style=style, underline=underline)
        buttom.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady)
        return buttom

    def _lista_programas(self, master, side, fill, expand=0, padx=0.0, pady=0.0):
        # frame, scrollbar e text que serão o container dos checkbutton
        frame = self._frame(master=master, side=side, fill=fill, expand=expand,
                            padx=padx, pady=pady)

        vsb = ttk.Scrollbar(master=frame, orient=tkinter.VERTICAL)
        text = tkinter.Text(master=frame, height=20, yscrollcommand=vsb.set)
        text.configure(background='white')
        text.configure(border=0)

        vsb.config(command=text.yview)
        vsb.pack(side=tkinter.RIGHT, fill=tkinter.Y, padx=2)
        text.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        # Criação dos checkbuttons para cada chave de dic_programas e inclusão no text
        self.adicionar_check_programas(frame, text, self.dic_programas.keys())

        text.configure(state='disabled')

        return frame, text

    def adicionar_check_programas(self, frame, text, programas):
        self.checkbutton = []
        for i, chave in enumerate(programas):
            self.checkbutton.append(tkinter.IntVar())
            self.checkbutton[i].set(self.marcar_todos)  # marcar checkbutton de acordo com atrib. marcar_todos.

            cb = ttk.Checkbutton(master=frame, text=chave, offvalue=0, onvalue=1, variable=self.checkbutton[i])
            cb['style'] = 'E.TCheckbutton'
            cb.bind('<Button-1>', self.clique_checkbutton)

            text.window_create(tkinter.END, window=cb)
            text.insert(tkinter.END, '\n')
