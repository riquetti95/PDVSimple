"""
Painel de Estoque - Versão para exibir dentro da janela principal
"""
import tkinter as tk
from tkinter import ttk, messagebox
from estoque import Estoque
from produtos import Produtos

class EstoquePanel:
    def __init__(self, parent, auth):
        self.parent = parent
        self.auth = auth
        self.estoque = Estoque()
        self.produtos = Produtos()
        
        self.create_widgets()
        self.load_produtos()
        
        # Verificar estoque baixo
        produtos_baixo = self.estoque.get_produtos_estoque_baixo()
        if produtos_baixo:
            messagebox.showwarning("Atenção", f"{len(produtos_baixo)} produto(s) com estoque abaixo do mínimo!")
    
    def create_widgets(self):
        """Cria os widgets"""
        # Frame principal
        main_frame = tk.Frame(self.parent, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Título com botão voltar
        title_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.FLAT, bd=0)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_inner = tk.Frame(title_frame, bg="#ffffff")
        title_inner.pack(fill=tk.X, padx=20, pady=15)
        
        btn_voltar = tk.Button(title_inner, text="← Voltar",
                              font=("Segoe UI", 10, "bold"),
                              bg="#1976D2", fg="white",
                              activebackground="#1565C0",
                              activeforeground="white",
                              relief=tk.FLAT, cursor="hand2",
                              padx=15, pady=8,
                              command=self.voltar_dashboard)
        btn_voltar.pack(side=tk.LEFT, padx=(0, 15))
        
        title_label = tk.Label(title_inner, text="📊 Controle de Estoque",
                              font=("Segoe UI", 20, "bold"),
                              bg="#ffffff", fg="#333")
        title_label.pack(side=tk.LEFT)
        
        # Frame de busca
        frame_busca = tk.Frame(main_frame, bg="#ffffff", relief=tk.FLAT, bd=0)
        frame_busca.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        busca_inner = tk.Frame(frame_busca, bg="#ffffff")
        busca_inner.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(busca_inner, text="Buscar:", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(busca_inner, font=("Segoe UI", 10), width=30,
                                    relief=tk.FLAT, bd=1, highlightthickness=1,
                                    highlightbackground="#e0e0e0",
                                    highlightcolor="#2196F3",
                                    bg="#fafafa")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_produtos())
        
        btn_ajustar = tk.Button(busca_inner, text="Ajustar Estoque",
                               bg="#4CAF50", fg="white",
                               font=("Segoe UI", 10),
                               relief=tk.FLAT, cursor="hand2",
                               command=self.ajustar_estoque)
        btn_ajustar.pack(side=tk.RIGHT, padx=5)
        
        # Treeview
        frame_tree = tk.Frame(main_frame, bg="#ffffff", relief=tk.FLAT, bd=0)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        tree_inner = tk.Frame(frame_tree, bg="#ffffff")
        tree_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        columns = ('ID', 'Código', 'Descrição', 'Estoque Atual', 'Estoque Mínimo', 'Status')
        self.tree = ttk.Treeview(tree_inner, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_inner, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
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
        
        dialog = tk.Toplevel(self.parent.winfo_toplevel())
        dialog.title("Ajustar Estoque")
        dialog.geometry("300x200")
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Produto: {produto['descricao']}", font=("Segoe UI", 10)).pack(pady=10)
        tk.Label(dialog, text=f"Estoque Atual: {produto['estoque_atual']}", font=("Segoe UI", 9)).pack()
        
        tk.Label(dialog, text="Novo Estoque:", font=("Segoe UI", 10)).pack(pady=10)
        estoque_var = tk.StringVar(value=str(produto['estoque_atual']))
        entry = tk.Entry(dialog, textvariable=estoque_var, font=("Segoe UI", 12), width=15)
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
    
    def voltar_dashboard(self):
        """Volta para o dashboard"""
        if hasattr(self.parent, 'main_window'):
            self.parent.main_window.show_dashboard()

