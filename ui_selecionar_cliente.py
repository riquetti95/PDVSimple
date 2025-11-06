"""
Diálogo para selecionar cliente
"""
import tkinter as tk
from tkinter import ttk
from clientes import Clientes

class SelecionarClienteWindow:
    def __init__(self, parent, clientes, callback):
        self.clientes = clientes
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Selecionar Cliente")
        self.window.geometry("800x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Busca
        frame_busca = tk.Frame(self.window)
        frame_busca.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_busca, text="Buscar:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(frame_busca, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_clientes())
        
        # Treeview
        frame_tree = tk.Frame(self.window)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nome', 'CPF/CNPJ', 'Telefone', 'Email')
        self.tree = ttk.Treeview(frame_tree, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<Double-1>', lambda e: self.selecionar())
        
        # Botões
        frame_buttons = tk.Frame(self.window)
        frame_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        btn_selecionar = tk.Button(frame_buttons, text="Selecionar", bg="#4CAF50", fg="white",
                                   command=self.selecionar, cursor="hand2")
        btn_selecionar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = tk.Button(frame_buttons, text="Cancelar", bg="#f44336", fg="white",
                                command=self.window.destroy, cursor="hand2")
        btn_cancelar.pack(side=tk.LEFT, padx=5)
        
        self.load_clientes()
    
    def load_clientes(self):
        """Carrega clientes"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search = self.search_entry.get()
        clientes = self.clientes.list_all(search)
        
        for cliente in clientes:
            self.tree.insert('', tk.END, values=cliente, tags=(cliente[0],))
    
    def selecionar(self):
        """Seleciona cliente"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        cliente_id = item['tags'][0]
        cliente = self.clientes.get_by_id(cliente_id)
        
        if cliente and self.callback:
            self.callback(cliente)
            self.window.destroy()

