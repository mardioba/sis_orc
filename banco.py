import sqlite3

def conectar():
    return sqlite3.connect("orcamento.db")

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    # Habilitar suporte a chaves estrangeiras no SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Criar tabela de orçamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orcamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            responsavel TEXT NOT NULL,
            descricao TEXT NOT NULL,
            data TEXT NOT NULL
        )
    ''')

    # Criar tabela de itens do orçamento com chave estrangeira e total do item
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_orcamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fk_orcamento_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            total_item REAL GENERATED ALWAYS AS (quantidade * preco_unitario) VIRTUAL,
            FOREIGN KEY (fk_orcamento_id) REFERENCES orcamentos (id) ON DELETE CASCADE
        )
    ''')

    conexao.commit()
    conexao.close()

# Criar tabelas ao rodar o script
criar_tabelas()
