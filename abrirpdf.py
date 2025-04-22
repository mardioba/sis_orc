import webbrowser
import os

def abrir_pdf(caminho_pdf):
    # Caminho do arquivo PDF
    pdf_path = os.path.abspath(caminho_pdf)

    # Verifica se o caminho é absoluto
    if not os.path.isabs(pdf_path):
        pdf_path = os.path.abspath(pdf_path)

    # Abre o PDF no navegador padrão
    webbrowser.open(f"file://{pdf_path}")

# if __name__ == "__main__":
#     caminho_pdf = "relatorios/1_orcamento_2025-02-16_09_57_23.pdf"
#     abrir_pdf(caminho_pdf)