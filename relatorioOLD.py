import sqlite3,re
from datetime import datetime

def obter_itens_orcamento(orcamento_id, db_path="orcamento.db"):
    """Obtém os itens de um orçamento e calcula o total geral."""
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Consulta SQL
        cursor.execute("""
            SELECT id, item, quantidade, preco_unitario, total_item, 
                   (SELECT SUM(total_item) FROM itens_orcamento WHERE fk_orcamento_id = ?) AS total_geral
            FROM itens_orcamento
            WHERE fk_orcamento_id = ?;
        """, (orcamento_id, orcamento_id))

        # Buscar os resultados
        resultados = cursor.fetchall()
        # print(resultados)

        # Fechar conexão
        conn.close()

        return resultados

    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
        return None
def todos_orcamentos(db_path="orcamento.db"):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Consulta SQL
        cursor.execute("SELECT * FROM orcamentos")

        # Buscar os resultados
        resultados = cursor.fetchall()

        # Fechar conexão
        conn.close()

        return resultados

    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
        return None
    
# Exemplo de uso
# orcamento_id = 1  # Substitua pelo ID desejado
# itens = obter_itens_orcamento(orcamento_id)

# # Exibir os resultados
# if itens:
#     for item in itens:
#         print(item)
resultado = todos_orcamentos()
# print(resultado)
for id, cliente, responsavel, descricao, data in resultado:
    data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
    descricao= descricao.replace('\n', ' ')
    descricao= re.sub(r'\s+', '', descricao)
    print(f"ID: {id},\nCliente: {cliente},\nResponsável: {responsavel},\nDescricao: {descricao},\nData: {data_formatada}")
