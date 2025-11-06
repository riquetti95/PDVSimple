"""
Tela de Controle de Estoque
"""
import tkinter as tk
from tkinter import ttk, messagebox
from estoque import Estoque
from produtos import Produtos

class EstoqueWindow:
    def __init__(self, root, auth):
        self.root = root
        self.auth = auth
        self.estoque = Estoque()
        self.produtos = Produtos()
        
        self.window = tk.Toplevel(root)
        self.window.title("Controle de Estoque")
        self.window.geometry("1000x600")
        
        self.create_widgets()
        self.load_produtos()
    
    def create_widgets(self):
        """Cria os widgets"""
        # Frame de busca
        frame_busca = tk.Frame(self.window)
        frame_busca.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_busca, text="Buscar:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(frame_busca, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_produtos())
        
        btn_ajustar = tk.Button(frame_busca, text="Ajustar Estoque", bg="#4CAF50", fg="white",
                               command=self.ajustar_estoque, cursor="hand2")
        btn_ajustar.pack(side=tk.RIGHT, padx=5)
        
        # Treeview
        frame_tree = tk.Frame(self.window)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Código', 'Descrição', 'Estoque Atual', 'Estoque Mínimo', 'Status')
        self.tree = ttk.Treeview(frame_tree, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Verificar estoque baixo
        produtos_baixo = self.estoque.get_produtos_estoque_baixo()
        if produtos_baixo:
            messagebox.showwarning("Atenção", f"{len(produtos_baixo)} produto(s) com estoque abaixo do mínimo!")
    
    def load_produtos(self):
        """Carrega produtos"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search = self.search_entry.get()
        produtos = self.produtos.list_all(search)
        
        for produto in produtos:
            estoque = produto[5]
            minimo = produto[6] if len(produto) > 6 else 0
            status = "OK" if estoque > minimo else "BAIXO"
            
            self.tree.insert('', tk.END, values=(
                produto[0], produto[1], produto[2], estoque, minimo, status
            ), tags=(produto[0],))
    
    def ajustar_estoque(self):
        """Ajusta estoque de um produto"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return
        
        item = self.tree.item(selection[0])
        produto_id = item['tags'][0]
        produto = self.produtos.get_by_id(produto_id)
        
        if not produto:
            return
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Ajustar Estoque")
        dialog.geometry("300x200")
        dialog.transient(self.window)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Produto: {produto['descricao']}", font=("Arial", 10)).pack(pady=10)
        tk.Label(dialog, text=f"Estoque Atual: {produto['estoque_atual']}", font=("Arial", 9)).pack()
        
        tk.Label(dialog, text="Novo Estoque:", font=("Arial", 10)).pack(pady=10)
        estoque_var = tk.StringVar(value=str(produto['estoque_atual']))
        entry = tk.Entry(dialog, textvariable=estoque_var, font=("Arial", 12), width=15)
        entry.pack(pady=5)
        entry.focus()
        entry.select_range(0, tk.END)
        
        def confirmar():
            try:
                novo_estoque = float(estoque_var.get().replace(',', '.'))
                if novo_estoque >= 0:
                    usuario_id = self.auth.get_current_user()['id']
                    self.estoque.registrar_movimentacao(
                        produto_id, 'Ajuste', novo_estoque,
                        observacao='Ajuste manual de estoque',
                        usuario_id=usuario_id
                    )
                    messagebox.showinfo("Sucesso", "Estoque ajustado com sucesso!")
                    self.load_produtos()
                    dialog.destroy()
            except:
                messagebox.showerror("Erro", "Valor inválido!")
        
        btn_ok = tk.Button(dialog, text="OK", command=confirmar, cursor="hand2")
        btn_ok.pack(pady=10)
        entry.bind('<Return>', lambda e: confirmar())

class MovimentacoesWindow:
    def __init__(self, root, auth):
        self.root = root
        self.auth = auth
        self.estoque = Estoque()
        
        self.window = tk.Toplevel(root)
        self.window.title("Movimentações de Estoque")
        self.window.geometry("1000x600")
        
        # Frame de filtros
        frame_filtros = tk.Frame(self.window)
        frame_filtros.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_filtros, text="Data Início:").pack(side=tk.LEFT, padx=5)
        self.data_inicio = tk.Entry(frame_filtros, width=12)
        self.data_inicio.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_filtros, text="Data Fim:").pack(side=tk.LEFT, padx=5)
        self.data_fim = tk.Entry(frame_filtros, width=12)
        self.data_fim.pack(side=tk.LEFT, padx=5)
        
        btn_buscar = tk.Button(frame_filtros, text="Buscar", command=self.load_movimentacoes, cursor="hand2")
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        # Treeview
        frame_tree = tk.Frame(self.window)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Data', 'Produto', 'Tipo', 'Quantidade', 'Observação', 'Usuário')
        self.tree = ttk.Treeview(frame_tree, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_movimentacoes()
    
    def load_movimentacoes(self):
        """Carrega movimentações"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        data_inicio = self.data_inicio.get() or None
        data_fim = self.data_fim.get() or None
        
        movimentacoes = self.estoque.list_movimentacoes(data_inicio=data_inicio, data_fim=data_fim)
        for mov in movimentacoes:
            self.tree.insert('', tk.END, values=mov)

