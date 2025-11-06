"""
Painel de Orçamentos - Versão para exibir dentro da janela principal
"""
import tkinter as tk
from tkinter import ttk, messagebox
from orcamentos import Orcamentos
from produtos import Produtos
from clientes import Clientes

class OrcamentosPanel:
    def __init__(self, parent, auth):
        self.parent = parent
        self.auth = auth
        self.orcamentos = Orcamentos()
        self.produtos = Produtos()
        self.clientes = Clientes()
        
        self.carrinho = []
        self.cliente_id = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
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
        
        title_label = tk.Label(title_inner, text="📋 Novo Orçamento",
                              font=("Segoe UI", 20, "bold"),
                              bg="#ffffff", fg="#333")
        title_label.pack(side=tk.LEFT)
        
        # Container do conteúdo
        content_frame = tk.Frame(main_frame, bg="#f5f5f5")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame esquerdo
        left_frame = tk.Frame(content_frame, bg="#ffffff", relief=tk.FLAT, bd=0)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Cliente
        frame_cliente = tk.LabelFrame(left_frame, text="Cliente",
                                     font=("Segoe UI", 11, "bold"),
                                     bg="#ffffff", fg="#333",
                                     relief=tk.FLAT, bd=1)
        frame_cliente.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        self.cliente_label = tk.Label(frame_cliente, text="Nenhum cliente selecionado",
                                     font=("Segoe UI", 10),
                                     bg="#ffffff", fg="#757575")
        self.cliente_label.pack(padx=10, pady=10)
        
        btn_selecionar_cliente = tk.Button(frame_cliente, text="Selecionar Cliente",
                                          font=("Segoe UI", 9),
                                          bg="#2196F3", fg="white",
                                          relief=tk.FLAT, cursor="hand2",
                                          command=self.selecionar_cliente)
        btn_selecionar_cliente.pack(pady=(0, 10))
        
        # Busca de produtos
        frame_busca = tk.LabelFrame(left_frame, text="Buscar Produto",
                                    font=("Segoe UI", 11, "bold"),
                                    bg="#ffffff", fg="#333",
                                    relief=tk.FLAT, bd=1)
        frame_busca.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.search_entry = tk.Entry(frame_busca, font=("Segoe UI", 11),
                                     relief=tk.FLAT, bd=1, highlightthickness=1,
                                     highlightbackground="#e0e0e0",
                                     highlightcolor="#2196F3",
                                     bg="#fafafa")
        self.search_entry.pack(fill=tk.X, padx=10, pady=10, ipady=8)
        self.search_entry.bind('<KeyRelease>', lambda e: self.buscar_produto_auto())
        
        # Lista de produtos
        frame_produtos = tk.LabelFrame(left_frame, text="Produtos",
                                      font=("Segoe UI", 11, "bold"),
                                      bg="#ffffff", fg="#333",
                                      relief=tk.FLAT, bd=1)
        frame_produtos.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        columns = ('Código', 'Descrição', 'Preço', 'Estoque')
        self.tree_produtos = ttk.Treeview(frame_produtos, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree_produtos.heading(col, text=col)
            self.tree_produtos.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(frame_produtos, orient=tk.VERTICAL, command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        self.tree_produtos.bind('<Double-1>', lambda e: self.adicionar_produto())
        
        # Frame direito - Carrinho
        right_frame = tk.Frame(content_frame, bg="#ffffff", relief=tk.FLAT, bd=0)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Carrinho
        frame_carrinho = tk.LabelFrame(right_frame, text="Itens do Orçamento",
                                      font=("Segoe UI", 11, "bold"),
                                      bg="#ffffff", fg="#333",
                                      relief=tk.FLAT, bd=1)
        frame_carrinho.pack(fill=tk.BOTH, expand=True, padx=15, pady=(15, 10))
        
        columns_carrinho = ('Produto', 'Qtd', 'Preço Unit.', 'Subtotal')
        self.tree_carrinho = ttk.Treeview(frame_carrinho, columns=columns_carrinho, show='headings', height=15)
        
        for col in columns_carrinho:
            self.tree_carrinho.heading(col, text=col)
            self.tree_carrinho.column(col, width=120)
        
        scrollbar_carrinho = ttk.Scrollbar(frame_carrinho, orient=tk.VERTICAL, command=self.tree_carrinho.yview)
        self.tree_carrinho.configure(yscrollcommand=scrollbar_carrinho.set)
        
        self.tree_carrinho.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar_carrinho.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Validade
        frame_validade = tk.LabelFrame(right_frame, text="Validade",
                                      font=("Segoe UI", 11, "bold"),
                                      bg="#ffffff", fg="#333",
                                      relief=tk.FLAT, bd=1)
        frame_validade.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        tk.Label(frame_validade, text="Dias de validade:", font=("Segoe UI", 10),
                bg="#ffffff", fg="#333").pack(pady=10)
        self.validade_entry = tk.Entry(frame_validade, font=("Segoe UI", 10), width=15)
        self.validade_entry.insert(0, "30")
        self.validade_entry.pack(pady=5)
        
        # Total
        self.total_label = tk.Label(frame_validade, text="Total: R$ 0,00",
                                   font=("Segoe UI", 16, "bold"),
                                   bg="#ffffff", fg="#2196F3")
        self.total_label.pack(pady=10)
        
        # Botões
        frame_buttons = tk.Frame(right_frame, bg="#ffffff")
        frame_buttons.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        btn_salvar = tk.Button(frame_buttons, text="Salvar Orçamento",
                              bg="#2196F3", fg="white",
                              font=("Segoe UI", 11, "bold"),
                              relief=tk.FLAT, cursor="hand2",
                              padx=20, pady=12,
                              command=self.salvar_orcamento)
        btn_salvar.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        btn_limpar = tk.Button(frame_buttons, text="Limpar",
                              bg="#FF9800", fg="white",
                              font=("Segoe UI", 11),
                              relief=tk.FLAT, cursor="hand2",
                              padx=20, pady=12,
                              command=self.limpar_carrinho)
        btn_limpar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.load_produtos()
    
    def load_produtos(self):
        """Carrega produtos"""
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        produtos = self.produtos.list_all()
        for produto in produtos:
            self.tree_produtos.insert('', tk.END, values=(
                produto[1], produto[2], f"R$ {produto[4]:.2f}", produto[5]
            ), tags=(produto[0],))
    
    def buscar_produto_auto(self):
        """Busca automática"""
        search = self.search_entry.get()
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        produtos = self.produtos.list_all(search)
        for produto in produtos:
            self.tree_produtos.insert('', tk.END, values=(
                produto[1], produto[2], f"R$ {produto[4]:.2f}", produto[5]
            ), tags=(produto[0],))
    
    def selecionar_cliente(self):
        """Seleciona cliente"""
        from ui_selecionar_cliente import SelecionarClienteWindow
        root_window = self.parent.winfo_toplevel()
        SelecionarClienteWindow(root_window, self.clientes, callback=self.set_cliente)
    
    def set_cliente(self, cliente):
        """Define cliente"""
        self.cliente_id = cliente['id']
        self.cliente_label.config(text=f"{cliente['nome']} - {cliente.get('cpf_cnpj', '')}")
    
    def adicionar_produto(self):
        """Adiciona produto ao carrinho"""
        selection = self.tree_produtos.selection()
        if not selection:
            return
        
        item = self.tree_produtos.item(selection[0])
        produto_id = int(item['tags'][0])
        produto = self.produtos.get_by_id(produto_id)
        
        if not produto:
            return
        
        quantidade = self.pedir_quantidade(produto)
        if quantidade <= 0:
            return
        
        for item_carrinho in self.carrinho:
            if item_carrinho['produto_id'] == produto_id:
                item_carrinho['quantidade'] += quantidade
                item_carrinho['subtotal'] = item_carrinho['quantidade'] * item_carrinho['preco_unitario']
                self.atualizar_carrinho()
                return
        
        self.carrinho.append({
            'produto_id': produto_id,
            'descricao': produto['descricao'],
            'quantidade': quantidade,
            'preco_unitario': produto['preco_venda'],
            'subtotal': quantidade * produto['preco_venda']
        })
        
        self.atualizar_carrinho()
    
    def pedir_quantidade(self, produto):
        """Solicita quantidade"""
        dialog = tk.Toplevel(self.parent.winfo_toplevel())
        dialog.title("Quantidade")
        dialog.geometry("300x150")
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Produto: {produto['descricao']}", font=("Segoe UI", 10)).pack(pady=10)
        
        quantidade_var = tk.StringVar(value="1")
        entry = tk.Entry(dialog, textvariable=quantidade_var, font=("Segoe UI", 12), width=10)
        entry.pack(pady=10)
        entry.focus()
        
        resultado = {'quantidade': 0}
        
        def confirmar():
            try:
                qtd = float(quantidade_var.get().replace(',', '.'))
                if qtd > 0:
                    resultado['quantidade'] = qtd
                    dialog.destroy()
            except:
                messagebox.showerror("Erro", "Quantidade inválida!")
        
        btn_ok = tk.Button(dialog, text="OK", command=confirmar, cursor="hand2")
        btn_ok.pack(pady=5)
        entry.bind('<Return>', lambda e: confirmar())
        
        dialog.wait_window()
        return resultado['quantidade']
    
    def atualizar_carrinho(self):
        """Atualiza carrinho"""
        for item in self.tree_carrinho.get_children():
            self.tree_carrinho.delete(item)
        
        for item in self.carrinho:
            self.tree_carrinho.insert('', tk.END, values=(
                item['descricao'][:30],
                item['quantidade'],
                f"R$ {item['preco_unitario']:.2f}",
                f"R$ {item['subtotal']:.2f}"
            ))
        
        total = sum(item['subtotal'] for item in self.carrinho)
        self.total_label.config(text=f"Total: R$ {total:.2f}")
    
    def limpar_carrinho(self):
        """Limpa o carrinho"""
        if messagebox.askyesno("Confirmar", "Deseja limpar o carrinho?"):
            self.carrinho = []
            self.atualizar_carrinho()
    
    def salvar_orcamento(self):
        """Salva orçamento"""
        if not self.cliente_id:
            messagebox.showwarning("Aviso", "Selecione um cliente!")
            return
        
        if not self.carrinho:
            messagebox.showwarning("Aviso", "Adicione produtos ao orçamento!")
            return
        
        try:
            validade_dias = int(self.validade_entry.get())
        except:
            validade_dias = 30
        
        usuario_id = self.auth.get_current_user()['id']
        
        try:
            orcamento_id = self.orcamentos.create(
                self.cliente_id,
                usuario_id,
                self.carrinho,
                validade_dias
            )
            
            messagebox.showinfo("Sucesso", f"Orçamento criado com sucesso!\nNúmero: {orcamento_id}")
            
            # Limpar carrinho
            self.carrinho = []
            self.cliente_id = None
            self.cliente_label.config(text="Nenhum cliente selecionado")
            self.validade_entry.delete(0, tk.END)
            self.validade_entry.insert(0, "30")
            self.atualizar_carrinho()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar orçamento: {str(e)}")
    
    def voltar_dashboard(self):
        """Volta para o dashboard"""
        if hasattr(self.parent, 'main_window'):
            self.parent.main_window.show_dashboard()

