# coding: utf-8

#!/usr/bin/python3
# coding: utf-8

import tkinter
from tkinter.messagebox import showerror, askyesno, showinfo
from tkinter import ttk
from collections import OrderedDict
from src.gerenciador_programas import verificar_programas_instalados, instalar_programa, remover_repositorio


class Instalador(tkinter.Tk):
    """ Instalador de programas, desenvolvido: Ubuntu 16.04, Python3.5, Tkinter.
        O arquivo programas deve ter entradas no seguinte formato:
        #nome-programa
        add-apt-repository ppa:repositorio -y; # incluido somente quando não está presente nos repositórios padrão.
        apt install nome-programa -y; # 2 x ENTER"""
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

        self.title('Instalador programas')

        # Por padrão, quando inicializado, todos os programas estão marcados.
        # Para mudar o padrão, mude o atributo marcar_todos por 0.
        self.marcar_todos = 1  # default 1.

        # Componentes do formulário.
        lbl_mensagem = ttk.Label(self, text="Marque os programas que deseja instalar")
        lbl_mensagem.grid(row=0, column=0, padx=5)

        # Criação e posicionamento dos checkbuttons para cada chave de dic_programas.
        coluna = 0
        linha = 0
        maior_linha = 0
        self.checkbutton = []
        for i, ch in enumerate(self.dic_programas.keys()):
            linha += 1

            if linha % 20 == 0:
                coluna += 1
                linha = 1

            if linha > maior_linha:
                maior_linha = linha

            self.checkbutton.append(tkinter.IntVar())
            self.checkbutton[i].set(self.marcar_todos)  # marcar checkbutton de acordo com atrib. marcar_todos.
            ttk.Checkbutton(self, text=ch, offvalue=0, onvalue=1,
                            variable=self.checkbutton[i]).grid(row=linha, column=coluna,
                                                               sticky=tkinter.W,
                                                               padx=5)

        ttk.Button(text="Reverter seleção", command=self.reverter).grid(row=maior_linha + 1, column=0,
                                                                        sticky=tkinter.W + tkinter.E,
                                                                        columnspan=coluna if coluna else 1,
                                                                        padx=2.5, pady=2.5)

        # Se coluna == 0, portando uma única coluna de programas.
        if not coluna:
            maior_linha += 1

        self.item = 1

        txt_btn_marcar_todos = "Desmarcar todos" if self.marcar_todos else "Marcar todos"
        self.btn_marcar_todos = ttk.Button(text=txt_btn_marcar_todos, command=self.selecionar)
        self.btn_marcar_todos.grid(row=maior_linha + self.item,
                                   column=coluna,
                                   sticky=tkinter.W + tkinter.E,
                                   padx=2.5, pady=2.5)

        self.item += 1
        ttk.Button(text="Desmarcar instalados", style="C.TButton", underline=0,
                   command=self.desmarcar_instalados).grid(row=maior_linha + self.item,
                                                           column=0,
                                                           columnspan=coluna + 1,
                                                           sticky=tkinter.W + tkinter.E,
                                                           padx=2.5, pady=2.5)

        self.item += 1
        ttk.Button(text="Instalar", style="C.TButton", underline=0,
                   command=self.instalar).grid(row=maior_linha + self.item,
                                               column=0,
                                               columnspan=coluna + 1,
                                               sticky=tkinter.W + tkinter.E,
                                               padx=2.5, pady=2.5)

        self.item += 1
        ttk.Button(text="Desinstalar", style="D.TButton", underline=0,
                   command=self.desinstalar).grid(row=maior_linha + self.item,
                                                  column=0,
                                                  columnspan=coluna + 1,
                                                  sticky=tkinter.W + tkinter.E,
                                                  padx=2.5, pady=2.5)

        self.item += 1
        self.lbl_status = ttk.Label(self, text="Sempre execute este programa como administrador.")
        self.lbl_status.grid(row=maior_linha + self.item, column=0, columnspan=coluna + 1, sticky=tkinter.W + tkinter.E,
                             padx=5, pady=5)

        # Atualização necessária para o método bbox() retornar a dimensão e posição do formulário correta.
        self.update_idletasks()
        # Centralizando formulário. Deve ser invocado depois da declaração dos componentes para
        # que a dimensão esteja apropriada. A dimensão está sendo gerada automaticamente para portar os
        # componentes na grade(grid).
        dimensao = self.bbox()  # dimensao[2]: width, dimensao[3]: height
        self.wm_geometry('%dx%d-%d-%d' % (dimensao[2], dimensao[3],
                                          (self.winfo_screenwidth() / 2) - (dimensao[2] / 2),
                                          self.winfo_screenheight()))

        # Bloqueio de redimensionamento.
        self.resizable(width=False, height=False)

        # Eventos do formulário.
        self.bind('<Escape>', self.fechar)
        self.bind('<Alt-i>', self.atalho_instalar)

        # Loop do formulário.
        self.mainloop()

    def fechar(self, event):
        self.destroy()

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
