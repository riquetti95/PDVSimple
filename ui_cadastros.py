"""
Tela de Cadastros (Clientes e Produtos)
"""
import tkinter as tk
from tkinter import ttk, messagebox
from clientes import Clientes
from produtos import Produtos

class CadastrosWindow:
    def __init__(self, root, auth):
        self.root = root
        self.auth = auth
        self.clientes = Clientes()
        self.produtos = Produtos()
        
        self.window = tk.Toplevel(root)
        self.window.title("Cadastros")
        self.window.geometry("1000x700")
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
        # Notebook para abas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba Clientes
        frame_clientes = ttk.Frame(notebook)
        notebook.add(frame_clientes, text="Clientes")
        self.create_clientes_tab(frame_clientes)
        
        # Aba Produtos
        frame_produtos = ttk.Frame(notebook)
        notebook.add(frame_produtos, text="Produtos")
        self.create_produtos_tab(frame_produtos)
    
    def create_clientes_tab(self, parent):
        """Cria a aba de clientes"""
        # Frame de busca
        frame_busca = tk.Frame(parent)
        frame_busca.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_busca, text="Buscar:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.search_cliente = tk.Entry(frame_busca, font=("Arial", 10), width=30)
        self.search_cliente.pack(side=tk.LEFT, padx=5)
        self.search_cliente.bind('<KeyRelease>', lambda e: self.load_clientes())
        
        btn_novo_cliente = tk.Button(frame_busca, text="Novo Cliente", bg="#4CAF50", fg="white",
                                    command=self.novo_cliente, cursor="hand2")
        btn_novo_cliente.pack(side=tk.RIGHT, padx=5)
        
        # Treeview de clientes
        frame_tree = tk.Frame(parent)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nome', 'CPF/CNPJ', 'Telefone', 'Email', 'Cidade')
        self.tree_clientes = ttk.Treeview(frame_tree, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree_clientes.heading(col, text=col)
            self.tree_clientes.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)
        
        self.tree_clientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_clientes.bind('<Double-1>', lambda e: self.editar_cliente())
    
    def create_produtos_tab(self, parent):
        """Cria a aba de produtos"""
        # Frame de busca
        frame_busca = tk.Frame(parent)
        frame_busca.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_busca, text="Buscar:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.search_produto = tk.Entry(frame_busca, font=("Arial", 10), width=30)
        self.search_produto.pack(side=tk.LEFT, padx=5)
        self.search_produto.bind('<KeyRelease>', lambda e: self.load_produtos())
        
        btn_novo_produto = tk.Button(frame_busca, text="Novo Produto", bg="#4CAF50", fg="white",
                                    command=self.novo_produto, cursor="hand2")
        btn_novo_produto.pack(side=tk.RIGHT, padx=5)
        
        # Treeview de produtos
        frame_tree = tk.Frame(parent)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Código', 'Descrição', 'Categoria', 'Preço', 'Estoque', 'Unidade')
        self.tree_produtos = ttk.Treeview(frame_tree, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree_produtos.heading(col, text=col)
            self.tree_produtos.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_produtos.bind('<Double-1>', lambda e: self.editar_produto())
    
    def load_data(self):
        """Carrega os dados"""
        self.load_clientes()
        self.load_produtos()
    
    def load_clientes(self):
        """Carrega lista de clientes"""
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        search = self.search_cliente.get()
        clientes = self.clientes.list_all(search)
        
        for cliente in clientes:
            self.tree_clientes.insert('', tk.END, values=cliente)
    
    def load_produtos(self):
        """Carrega lista de produtos"""
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        search = self.search_produto.get()
        produtos = self.produtos.list_all(search)
        
        for produto in produtos:
            self.tree_produtos.insert('', tk.END, values=(
                produto[0], produto[1], produto[2], produto[3],
                f"R$ {produto[4]:.2f}", produto[5], produto[6]
            ))
    
    def novo_cliente(self):
        """Abre formulário de novo cliente"""
        from ui_form_cliente import FormClienteWindow
        FormClienteWindow(self.window, self.clientes, callback=self.load_clientes)
    
    def editar_cliente(self):
        """Edita cliente selecionado"""
        selection = self.tree_clientes.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar!")
            return
        
        item = self.tree_clientes.item(selection[0])
        cliente_id = item['values'][0]
        
        from ui_form_cliente import FormClienteWindow
        FormClienteWindow(self.window, self.clientes, cliente_id=cliente_id, callback=self.load_clientes)
    
    def novo_produto(self):
        """Abre formulário de novo produto"""
        from ui_form_produto import FormProdutoWindow
        FormProdutoWindow(self.window, self.produtos, callback=self.load_produtos)
    
    def editar_produto(self):
        """Edita produto selecionado"""
        selection = self.tree_produtos.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para editar!")
            return
        
        item = self.tree_produtos.item(selection[0])
        produto_id = item['values'][0]
        
        from ui_form_produto import FormProdutoWindow
        FormProdutoWindow(self.window, self.produtos, produto_id=produto_id, callback=self.load_produtos)

