from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sqlite3, re
import subprocess
import os
import platform
from datetime import datetime

def verificar(id_orcamento):
    dirtorio = 'relatorios'
    # print(os.listdir(dirtorio))
    contador = 0
    for file in os.listdir(dirtorio):
        v=re.findall(r'^' + str(id_orcamento) + r'_', file)
        if v:
            caminho = dirtorio + '/' + file
            return True, caminho
        else:
            return None

# Função para gerar o PDF do orçamento com imagem
def gerar_orcamento_pdf(orcamento_id, nome_arquivo):
    # Verificando pasta relatorios
    try:
        if os.path.exists(f'relatorios'):
            print("O arquivo existe")
        else:
            os.mkdir(f'relatorios')
            print("O arquivo nao existe")
    except:
        pass
    # Conectar ao banco de dados (aqui está como exemplo)
    conn = sqlite3.connect('orcamento.db')
    cursor = conn.cursor()
    
    # Obter os dados do orçamento (supondo que você já tenha isso)
    cursor.execute("SELECT * FROM orcamentos WHERE id = ?", (orcamento_id,))
    orcamento = cursor.fetchone()
    
    if not orcamento:
        print("Orçamento não encontrado!")
        return

    # Obter os itens do orçamento
    cursor.execute("SELECT * FROM itens_orcamento WHERE fk_orcamento_id = ?", (orcamento_id,))
    itens = cursor.fetchall()
    
    # Criar o PDF
    c = canvas.Canvas(f"relatorios/{orcamento_id}_{nome_arquivo}", pagesize=letter)
    
    # Definir algumas variáveis para o layout do PDF
    largura, altura = letter
    margem = 50
    y_pos = altura - margem

    # Inserir a imagem no topo da página
    c.drawImage("logo.png", margem, y_pos - 60, width=200, height=60)  # Ajuste o tamanho e a posição conforme necessário
    y_pos -= 100  # Ajuste a posição depois da imagem

    # Cabeçalho do orçamento
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margem, y_pos, f'Orçamento para: {orcamento[1]}')
    y_pos -= 30
    c.setFont("Helvetica", 12)
    c.drawString(margem, y_pos, f'Responsável: {orcamento[2]}')
    y_pos -= 20
    descricao = orcamento[3].replace('\n', ' ')
    descricao = re.sub(r'\s+', ' ', descricao)
    c.drawString(margem, y_pos, f'Descrição: {descricao}')
    y_pos -= 20
    data_formatada = datetime.strptime(orcamento[4], "%Y-%m-%d").strftime("%d/%m/%Y")
    c.drawString(margem, y_pos, f'Data: {data_formatada}')
    y_pos -= 30
    
    # Tabela de itens
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margem, y_pos, 'Item')
    c.drawString(margem + 200, y_pos, 'Quantidade')
    c.drawString(margem + 300, y_pos, 'Preço Unitário')
    c.drawString(margem + 450, y_pos, 'Total')
    y_pos -= 20
    
    c.setFont("Helvetica", 12)
    for item in itens:
        # Para garantir que item[4] e item[5] sejam formatados corretamente
        preco_unitario = float(item[4].replace(",", ".")) if isinstance(item[4], str) else item[4]
        total_item = float(item[5].replace(",", ".")) if isinstance(item[5], str) else item[5]

        c.drawString(margem, y_pos, item[2])  # Nome do item
        c.drawString(margem + 200, y_pos, str(item[3]))  # Quantidade
        c.drawString(margem + 300, y_pos, f'R${preco_unitario:.2f}')  # Preço unitário
        c.drawString(margem + 450, y_pos, f'R${total_item:.2f}')  # Total do item
        y_pos -= 20
        
        if y_pos < margem:
            c.showPage()
            y_pos = altura - margem
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margem, y_pos, 'Item')
            c.drawString(margem + 200, y_pos, 'Quantidade')
            c.drawString(margem + 300, y_pos, 'Preço Unitário')
            c.drawString(margem + 450, y_pos, 'Total')
            y_pos -= 20

    # Total do orçamento
    total_orcamento = sum(item[5] for item in itens)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margem + 300, y_pos, 'Total do Orçamento:')
    c.drawString(margem + 450, y_pos, f'R${total_orcamento:.2f}')
    
    # Salvar o arquivo PDF
    c.save()
    print(f'Orçamento {orcamento_id} gerado com sucesso: {nome_arquivo}')
    # Abrir o PDF automaticamente
    sistema = platform.system()
    if sistema == "Linux":
        subprocess.run(["xdg-open", f"relatorios/{orcamento_id}_{nome_arquivo}"])  # Abre no Linux (Debian)
    elif sistema == "Windows":
        os.startfile(f"relatorios/{orcamento_id}_{nome_arquivo}")  # Abre no Windows
    elif sistema == "Darwin":  # macOS
        subprocess.run(["open", f"relatorios/{orcamento_id}_{nome_arquivo}"])

# Exemplo de uso
# if __name__ == "__main__":
#     data_atual_BR= datetime.now() #.strftime("%d-%m-%Y")
#     datanome=str(data_atual_BR).replace(':','_').replace(' ','_')
#     datanome=re.sub(r'\.[0-9]*$', '', datanome)
#     gerar_orcamento_pdf(1, f'orcamento_{datanome}.pdf')
# rs=verificar(1)
# if rs:
#     print(rs[1])
#     # Abrir o PDF automaticamente
#     sistema = platform.system()
#     if sistema == "Linux":
#         subprocess.run(["xdg-open", rs[1]])  # Abre no Linux (Debian)
#     elif sistema == "Windows":
#         os.startfile(rs[1])  # Abre no Windows
#     elif sistema == "Darwin":  # macOS
#         subprocess.run(["open", rs[1]])