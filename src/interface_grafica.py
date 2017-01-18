#!/usr/bin/python3
# coding: utf-8

import tkinter
from tkinter.messagebox import showerror, askyesno, showinfo
from tkinter import ttk
from collections import OrderedDict
try:
    from src.gerenciador_programas import verificar_programas_instalados, instalar_programa, remover_repositorio
except:
    from gerenciador_programas import verificar_programas_instalados, instalar_programa, remover_repositorio


class Instalador(tkinter.Tk):
    """ Interface gráfica do instaldor. """
    def __init__(self, dic_programas: OrderedDict, diretorio: str):
        # Construtor(classe pai: tkinter.Tk) e configurações da janela.
        super(Instalador, self).__init__()

        self.dic_programas = dic_programas
        self.diretorio = diretorio

        style = ttk.Style()
        style.theme_use('clam')

        # Para adicionar novos estilos personalizados, deve-se manter o nome do componente.
        # Ex: C.TButton, D.TButton
        style.map("C.TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'), ('active', 'darkgray')])
        style.map("D.TButton",
                  foreground=[('pressed', 'black'), ('active', 'red')],
                  background=[('pressed', '!disabled', 'red'), ('active', 'darkgray')])
        style.map("E.TCheckbutton",
                  background=[('active', 'darkgray'), ('!active', 'white')])

        self.title('Instalador programas')

        # Por padrão, quando inicializado, todos os programas estão marcados.
        # Para mudar o padrão, mude o atributo marcar_todos por 0.
        self.marcar_todos = 1  # default 1.

        # Componentes do formulário.
        lbl_mensagem = ttk.Label(master=self, text="Marque os programas que deseja instalar")
        lbl_mensagem.pack(side=tkinter.TOP, fill=tkinter.X, padx=5, pady=2.5)

        # frame, scrollbar e text que serão o container dos checkbutton
        frame1 = ttk.Frame(master=self)
        frame1.pack(side=tkinter.TOP, fill=tkinter.BOTH, padx=5, pady=2.5, expand=1)

        vsb = ttk.Scrollbar(master=frame1, orient=tkinter.VERTICAL)
        text = tkinter.Text(master=frame1, height=20, yscrollcommand=vsb.set)
        text.configure(background='white')

        vsb.config(command=text.yview)
        vsb.pack(side=tkinter.RIGHT, fill=tkinter.Y, padx=2)
        text.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        # Criação dos checkbuttons para cada chave de dic_programas e inclusão no text
        self.checkbutton = []
        for i, ch in enumerate(self.dic_programas.keys()):
            self.checkbutton.append(tkinter.IntVar())
            self.checkbutton[i].set(self.marcar_todos)  # marcar checkbutton de acordo com atrib. marcar_todos.
            cb = ttk.Checkbutton(master=frame1, text=ch, offvalue=0, onvalue=1, variable=self.checkbutton[i])
            cb['style'] = 'E.TCheckbutton'
            text.window_create(tkinter.END, window=cb)
            text.insert(tkinter.END, '\n')

        text.configure(state='disabled')

        # frame para botões reverter seleção e desmarcar seleção que ficam lado a lado
        frame2 = ttk.Frame(master=self)
        frame2.pack(side=tkinter.TOP,
                    fill=tkinter.X,
                    padx=2.5,
                    pady=2.5)

        ttk.Button(master=frame2, text='Reverter seleção', command=self.reverter).pack(side=tkinter.LEFT,
                                                                                       fill=tkinter.X,
                                                                                       padx=2.5,
                                                                                       expand=1)

        # Botões
        txt_btn_marcar_todos = "Desmarcar todos" if self.marcar_todos else "Marcar todos"
        self.btn_marcar_todos = ttk.Button(master=frame2, text=txt_btn_marcar_todos, command=self.selecionar)
        self.btn_marcar_todos.pack(side=tkinter.RIGHT,
                                   fill=tkinter.X,
                                   padx=2.5,
                                   expand=1)

        ttk.Button(master=self, text="Desmarcar instalados", style="C.TButton", underline=0,
                   command=self.desmarcar_instalados).pack(side=tkinter.TOP,
                                                           fill=tkinter.X,
                                                           padx=5,
                                                           pady=2.5)

        ttk.Button(master=self, text="Instalar", style="C.TButton", underline=0,
                   command=self.instalar).pack(side=tkinter.TOP,
                                               fill=tkinter.X,
                                               padx=5,
                                               pady=2.5)

        ttk.Button(master=self, text="Desinstalar", style="D.TButton", underline=0,
                   command=self.desinstalar).pack(side=tkinter.TOP,
                                                  fill=tkinter.X,
                                                  padx=5,
                                                  pady=2.5)

        self.lbl_status = ttk.Label(self, text="Sempre execute este programa como administrador.")
        self.lbl_status.pack(side=tkinter.TOP,
                             fill=tkinter.X,
                             padx=5,
                             pady=2.5)

        # Centralizando formulário.
        dimensao = (500, 600)
        self.wm_geometry('%dx%d-%d-%d' % (dimensao[0], dimensao[1],
                                          (self.winfo_screenwidth() / 2) - (dimensao[0] / 2),
                                          self.winfo_screenheight()))

        # Definindo tamanho mínimo do formulário
        self.minsize(400, 500)

        # Eventos do formulário.
        self.bind('<Escape>', self.atalho_fechar)
        self.protocol('WM_DELETE_WINDOW', self.fechar)
        self.bind('<Alt-i>', self.atalho_instalar)
        self.bind('<Alt-d>', self.atalho_desintalar)

        # Loop do formulário.
        self.mainloop()

    def fechar(self):
        if askyesno("Confirmação", "Deseja realmente fechar o instalador?"):
            self.destroy()

    def atalho_fechar(self, event):
        self.fechar()

    def instalar(self):
        """ Ação do botão instalar.
        :return: none. """
        self.instalacao()

    def desinstalar(self):
        """ Ação do botão desinstalar. Usa o parâmetro remover para ativar o recurso de desinstalação.
        :return: none. """
        self.instalacao(remover=True)

    def desmarcar_instalados(self):
        """ Ação do botão marcar instalados. Analiza o sistema e desmarca os programas instalados.
         :return: none. """

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
        :return: none. """
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
        :return: none. """
        for i in range(len(self.checkbutton)):
            self.checkbutton[i].set(not self.checkbutton[i].get())

    def selecionar(self):
        """ Marcar ou desmarcar todos os programas.
        :return: none. """
        self.marcar_todos = not self.marcar_todos
        if self.marcar_todos:
            self.btn_marcar_todos['text'] = "Desmarcar todos"
        else:
            self.btn_marcar_todos['text'] = "Marcar todos "

        for i in range(len(self.checkbutton)):
            self.checkbutton[i].set(self.marcar_todos)

    def atalho_instalar(self, event):
        self.instalar()

    def atalho_desintalar(self, event):
        self.desinstalar()
