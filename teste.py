import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Treeview in Tk")
treeview = ttk.Treeview(columns=("size", "lastmod"))
treeview.heading("#0", text="File")
treeview.heading("size", text="Size")
treeview.heading("lastmod", text="Last modification")
treeview.insert(
    "",
    tk.END,
    text="README.txt",
    values=("850 bytes", "18:30")
)
treeview.pack()
def limpar():
    treeview.delete(treeview.get_children())
btn_limpar = tk.Button(root, text="Limpar", command=limpar)
btn_limpar.pack()
root.mainloop()
