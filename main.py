import tkinter as tk
from interface import OrcamentoApp

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = OrcamentoApp(root)
#     root.mainloop()
root = tk.Tk()  # Criando a janela principal
app = OrcamentoApp(root)  # Passando root como argumento
root.mainloop()  # Iniciando o loop do Tkinter