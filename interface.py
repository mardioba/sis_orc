import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3, re
import banco


class OrcamentoApp():
    def __init__(self):
        pass
        self.janela = tk.Tk()
        self.janela.title("Exemplo de LabelFrame")
        self.janela.geometry("600x550")
        self.janela.resizable(False, False)
        self.centralizar_janela()  # Chama a função para centralizar a janela
        self.divisorias()
        # self.servicos()
        self.tree_itens()
        self.componentes()
        self.janela.mainloop()
    def centralizar_janela(self):
        """ Centraliza a janela no meio da tela """
        self.janela.update_idletasks()  # Atualiza para pegar tamanho real

        largura = self.janela.winfo_width()
        altura = self.janela.winfo_height()
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()

        # Calcula a posição central
        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2

        self.janela.geometry(f"+{pos_x}+{pos_y}")  # Aplica a posição
    def divisorias(self):
        # Criando um LabelFrame com legenda e borda
        self.lblf_gerais = ttk.LabelFrame(self.janela, text="Informações Gerais", padding=10)
        self.lblf_gerais.pack(fill="x")
        self.lblf_servicos = ttk.LabelFrame(self.janela, text="Serviços", padding=10)
        self.lblf_servicos.pack(fill="x")
        self.lblf_itens = ttk.LabelFrame(self.janela, text="Itens", padding=10)
        self.lblf_itens.pack(fill="x")
        # Adicionando um exemplo de widget dentro do frame
    def componentes(self):
        # Adicionando um exemplo de widget dentro do frame gerais
        self.lbl_cliente = ttk.Label(self.lblf_gerais, text="Cliente:")
        self.lbl_cliente.grid(row=0, column=0, padx=5, pady=5)
        self.lbl_responsavel = ttk.Label(self.lblf_gerais, text="Responsável:")
        self.lbl_responsavel.grid(row=0, column=2, padx=5, pady=5)
        self.lbl_data = ttk.Label(self.lblf_gerais, text="Data:")
        self.lbl_data.grid(row=1, column=0, padx=5, pady=5)
        self.ent_data = DateEntry(self.lblf_gerais, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.ent_data.set_date(datetime.now())
        self.ent_data.grid(row=1, column=1, padx=5, pady=5)
        self.lbl_descricao = ttk.Label(self.lblf_gerais, text="Descricão:")
        self.lbl_descricao.grid(row=2, column=0, padx=5, pady=5)
        self.ent_cliente = ttk.Entry(self.lblf_gerais)
        self.ent_cliente.grid(row=0, column=1, padx=5, pady=5)
        self.ent_responsavel = ttk.Entry(self.lblf_gerais)
        self.ent_responsavel.grid(row=0, column=3, padx=5, pady=5)
        # Criando a área de texto
        self.txt_descricao = tk.Text(self.lblf_gerais, height=3, width=50)
        self.txt_descricao.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.btn_iniciarOrcamento = ttk.Button(self.lblf_gerais, text="Iniciar Orcamento", command=self.iniciarOrcamento)
        self.btn_iniciarOrcamento.grid(row=3, column=2, padx=5, pady=5)
    def iniciarOrcamento(self):
        cliente = self.ent_cliente.get()
        descricao = self.txt_descricao.get("1.0", "end")
        responsavel = self.ent_responsavel.get()
        data = self.ent_data.get_date()

        conn = sqlite3.connect('orcamento.db')
        c = conn.cursor()
        if not cliente or not responsavel or not data:
            messagebox.showwarning("Erro", "Por favor, preencha todos os campos")
        else:
            c.execute("INSERT INTO orcamentos (cliente, descricao, responsavel, data) VALUES (?, ?, ?, ?)",
                    (cliente, descricao, responsavel, data))
            conn.commit()
            # Obtendo o ID da última linha inserida
            self.ultimo_id = c.lastrowid
            print(f"Último ID inserido: {self.ultimo_id}")
            messagebox.showinfo("Sucesso", f"Orcamento iniciado com sucesso agora você pode adicionar os serviços\n\n*** NAO ESQUEÇA DE SALVAR O RELATORIO DEPOIS DE ADICIONAR OS SERVIÇOS ***")
            conn.close()
            self.servicos()
            self.tree_itens()
    def servicos(self):
    # Adicionando um exemplo de widget dentro do frame de serviços
        self.lbl_servicos = ttk.Label(self.lblf_servicos, text="Serviços:")
        self.lbl_servicos.grid(row=0, column=0, padx=5, pady=5)
        self.ent_servicos = ttk.Entry(self.lblf_servicos)
        self.ent_servicos.grid(row=0, column=1, padx=5, pady=5)
        self.lbl_quantidade = ttk.Label(self.lblf_servicos, text="Quantidade:")
        self.lbl_quantidade.grid(row=0, column=3, padx=5, pady=5)
        self.ent_quantidade = ttk.Entry(self.lblf_servicos, width=10)
        self.ent_quantidade.grid(row=0, column=4)
        self.lbl_valor = ttk.Label(self.lblf_servicos, text="Valor Unitario:")
        self.lbl_valor.grid(row=1, column=0, padx=5, pady=5)
        self.ent_valor = ttk.Entry(self.lblf_servicos)
        self.ent_valor.grid(row=1, column=1, padx=5, pady=5)
        self.btn_adicionar = ttk.Button(self.lblf_servicos, text="+ Adicionar", command=self.validar_servicos)
        self.btn_adicionar.grid(row=1, column=2, padx=5, pady=5)
        self.ent_idorcamento = ttk.Entry(self.lblf_servicos)
        self.ent_idorcamento.grid(row=0, column=5, padx=5, pady=5)
        self.ent_idorcamento.delete(0, "end")
        self.ent_idorcamento.insert(0, self.ultimo_id)
        self.ent_idorcamento.config(state="readonly")
    def tree_itens(self):
        """ Adicionando Treeview e widgets no frame """
        self.lbl_itens = ttk.Label(self.lblf_itens, text="Itens:")
        self.lbl_itens.grid(row=0, column=0, padx=5, pady=5)
        
        # Adicionando a barra de rolagem vertical
        self.scrollbar = ttk.Scrollbar(self.lblf_itens, orient="vertical")
        self.scrollbar.grid(row=0, column=2, sticky="ns", padx=5)  # Lateral à direita do Treeview

        # Criando o Treeview com as colunas
        self.tv_itens = ttk.Treeview(self.lblf_itens, columns=("ID Orc","servico", "quantidade", "valor"), show="headings", yscrollcommand=self.scrollbar.set)
        self.tv_itens.heading("ID Orc", text="ID Orc")
        self.tv_itens.heading("servico", text="Serviço")
        self.tv_itens.heading("quantidade", text="Qtd")
        self.tv_itens.heading("valor", text="Valor U.")
        
        # Ajustando a largura das colunas
        self.tv_itens.column("ID Orc", width=80)
        self.tv_itens.column("servico", width=100)
        self.tv_itens.column("quantidade", width=60)
        self.tv_itens.column("valor", width=100)

        # Colocando o Treeview na grid
        self.tv_itens.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Expande a última coluna
        self.lblf_itens.grid_columnconfigure(1, weight=1, uniform="equal")

        # Expande o frame do Treeview
        self.lblf_itens.grid_rowconfigure(0, weight=1, uniform="equal")

        # Conectando o Scrollbar ao Treeview
        self.scrollbar.config(command=self.tv_itens.yview)
        self.btn_excluir = ttk.Button(self.lblf_itens, text="Excluir Item", command=self.excluir_linha)
        self.btn_excluir.grid(row=1, column=0, padx=5, pady=5)
        self.btn_editar = ttk.Button(self.lblf_itens, text="Editar Item", command=self.editar_linha)
        self.btn_editar.grid(row=1, column=1, padx=5, pady=5)
        self.btn_salvar = ttk.Button(self.lblf_itens, text="Salvar", compound="left", command=self.salvar_banco)
        self.btn_salvar.grid(row=1, column=2, padx=5, pady=5)

    def excluir_linha(self):
        item_selecionado = self.tv_itens.selection()
        if not item_selecionado:
            messagebox.showwarning("Atenção", "Selecione na tabela um item para excluir.")
            return
        
        for item in item_selecionado:
            self.tv_itens.delete(item)

    def editar_linha(self):
        item_selecionado = self.tv_itens.selection()

        if not item_selecionado:
            messagebox.showwarning("Atenção", "Selecione na tabela um item para editar.")
            return

        item = item_selecionado[0]  # Pega o primeiro item selecionado
        valores_atuais = self.tv_itens.item(item, "values")
        servico=valores_atuais[1]
        quantidade=valores_atuais[2]
        valor=valores_atuais[3]
        self.ent_servicos.delete(0, "end")
        self.ent_servicos.insert(0, servico)
        self.ent_quantidade.delete(0, "end")
        self.ent_quantidade.insert(0, quantidade)
        self.ent_valor.delete(0, "end")
        self.ent_valor.insert(0, valor)
        self.excluir_linha()

    def adicionar_item(self):
        """ Adiciona os dados dos campos ao Treeview """
        id_orcamento = self.ent_idorcamento.get()
        servico = self.ent_servicos.get()
        quantidade = self.ent_quantidade.get()
        valor = self.ent_valor.get()
        self.tv_itens.insert("", "end", values=(id_orcamento,servico, quantidade, valor))
        
        # Limpa os campos após adicionar
        self.ent_servicos.delete(0, "end")
        self.ent_quantidade.delete(0, "end")
        self.ent_valor.delete(0, "end")
        self.ent_servicos.focus_set()

    def validar_servicos(self):
        def validar_decimal(numero):
            padrao = r"^-?\d+(?:[.,]\d+)?$"
            return bool(re.match(padrao, numero))
        #validar campos
        servico = self.ent_servicos.get()
        quantidade = self.ent_quantidade.get()
        valor = self.ent_valor.get()
        if not all([servico, quantidade, valor]):  
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")  
            self.ent_servicos.focus_set()  
        elif not quantidade.isnumeric():  
            messagebox.showwarning("Atenção", "Quantidade deve ser um número.")  
            self.ent_quantidade.focus_set()  
        elif not validar_decimal(valor):  
            messagebox.showwarning("Atenção", "Valor deve ser um número.")  
            self.ent_valor.focus_set()
        else:
            self.adicionar_item()

    def salvar_banco(self):
            """ Salva todos os dados da Treeview no banco de dados """
            conn = sqlite3.connect('orcamento.db')
            c = conn.cursor()


            # Itera sobre as linhas da Treeview e insere os dados no banco
            for item in self.tv_itens.get_children():
                values = self.tv_itens.item(item, "values")
                c.execute("INSERT INTO itens_orcamento (fk_orcamento_id, item, quantidade, preco_unitario) VALUES (?, ?, ?, ?)", 
                        (values[0], values[1], values[2], values[3]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso no banco de dados.")


OrcamentoApp()