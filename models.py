import sqlite3
from banco import conectar

class Orcamento:
    @staticmethod
    def adicionar(cliente, descricao, valor, data):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO orcamentos (cliente, descricao, valor, data) VALUES (?, ?, ?, ?)",
                       (cliente, descricao, valor, data))
        conexao.commit()
        conexao.close()

    @staticmethod
    def listar():
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM orcamentos")
        orcamentos = cursor.fetchall()
        conexao.close()
        return orcamentos

    @staticmethod
    def deletar(id_orcamento):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM orcamentos WHERE id=?", (id_orcamento,))
        conexao.commit()
        conexao.close()
