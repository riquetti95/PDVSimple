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
        # Frame principal com mesmo estilo da venda
        main_frame = tk.Frame(self.parent, bg="#f0f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header moderno azul
        header_frame = tk.Frame(main_frame, bg="#2196F3", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg="#2196F3")
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Botão voltar no header
        btn_voltar = tk.Button(header_content, text="← Voltar",
                              font=("Segoe UI", 11, "bold"),
                              bg="#1976D2", fg="white",
                              activebackground="#1565C0",
                              activeforeground="white",
                              relief=tk.FLAT, cursor="hand2",
                              padx=20, pady=10,
                              command=self.voltar_dashboard)
        btn_voltar.pack(side=tk.LEFT, padx=(0, 20))
        
        # Título com ícone
        title_container = tk.Frame(header_content, bg="#2196F3")
        title_container.pack(side=tk.LEFT)
        
        icon_label = tk.Label(title_container, text="📋", font=("Segoe UI", 28),
                             bg="#2196F3", fg="white")
        icon_label.pack(side=tk.LEFT, padx=(0, 12))
        
        title_label = tk.Label(title_container, text="Novo Orçamento",
                              font=("Segoe UI", 24, "bold"),
                              bg="#2196F3", fg="white")
        title_label.pack(side=tk.LEFT)
        
        # Container do conteúdo
        content_frame = tk.Frame(main_frame, bg="#f0f4f8")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Frame esquerdo
        left_frame = tk.Frame(content_frame, bg="#ffffff", relief=tk.FLAT, bd=0)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Card Cliente
        card_cliente = tk.Frame(left_frame, bg="#ffffff", relief=tk.FLAT, bd=1,
                               highlightbackground="#e0e0e0", highlightthickness=1)
        card_cliente.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        cliente_header = tk.Frame(card_cliente, bg="#f5f5f5", height=40)
        cliente_header.pack(fill=tk.X)
        cliente_header.pack_propagate(False)
        
        tk.Label(cliente_header, text="👤 Cliente", font=("Segoe UI", 12, "bold"),
                bg="#f5f5f5", fg="#333").pack(side=tk.LEFT, padx=15, pady=10)
        
        cliente_body = tk.Frame(card_cliente, bg="#ffffff")
        cliente_body.pack(fill=tk.X, padx=15, pady=15)
        
        self.cliente_label = tk.Label(cliente_body, text="Nenhum cliente selecionado",
                                     font=("Segoe UI", 11),
                                     bg="#ffffff", fg="#757575")
        self.cliente_label.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_selecionar_cliente = tk.Button(cliente_body, text="Selecionar Cliente",
                                          font=("Segoe UI", 10, "bold"),
                                          bg="#2196F3", fg="white",
                                          relief=tk.FLAT, cursor="hand2",
                                          padx=20, pady=8,
                                          activebackground="#1976D2",
                                          activeforeground="white",
                                          command=self.selecionar_cliente)
        btn_selecionar_cliente.pack(side=tk.LEFT)
        
        # Card Busca
        card_busca = tk.Frame(left_frame, bg="#ffffff", relief=tk.FLAT, bd=1,
                             highlightbackground="#e0e0e0", highlightthickness=1)
        card_busca.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        busca_header = tk.Frame(card_busca, bg="#f5f5f5", height=40)
        busca_header.pack(fill=tk.X)
        busca_header.pack_propagate(False)
        
        tk.Label(busca_header, text="🔍 Buscar Produto", font=("Segoe UI", 12, "bold"),
                bg="#f5f5f5", fg="#333").pack(side=tk.LEFT, padx=15, pady=10)
        
        busca_body = tk.Frame(card_busca, bg="#ffffff")
        busca_body.pack(fill=tk.X, padx=15, pady=15)
        
        self.search_entry = tk.Entry(busca_body, font=("Segoe UI", 11),
                                     relief=tk.FLAT, bd=1, highlightthickness=1,
                                     highlightbackground="#e0e0e0",
                                     highlightcolor="#2196F3",
                                     bg="#fafafa")
        self.search_entry.pack(fill=tk.X, ipady=8)
        self.search_entry.bind('<KeyRelease>', lambda e: self.buscar_produto_auto())
        
        # Card Produtos
        card_produtos = tk.Frame(left_frame, bg="#ffffff", relief=tk.FLAT, bd=1,
                                highlightbackground="#e0e0e0", highlightthickness=1)
        card_produtos.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        produtos_header = tk.Frame(card_produtos, bg="#f5f5f5", height=40)
        produtos_header.pack(fill=tk.X)
        produtos_header.pack_propagate(False)
        
        tk.Label(produtos_header, text="📦 Produtos Disponíveis", font=("Segoe UI", 12, "bold"),
                bg="#f5f5f5", fg="#333").pack(side=tk.LEFT, padx=15, pady=10)
        
        produtos_body = tk.Frame(card_produtos, bg="#ffffff")
        produtos_body.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('Código', 'Descrição', 'Preço', 'Estoque')
        self.tree_produtos = ttk.Treeview(produtos_body, columns=columns, show='headings', height=15)
        
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        
        for col in columns:
            self.tree_produtos.heading(col, text=col)
            if col == 'Descrição':
                self.tree_produtos.column(col, width=200)
            else:
                self.tree_produtos.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(produtos_body, orient=tk.VERTICAL, command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_produtos.bind('<Double-1>', lambda e: self.adicionar_produto())
        
        # Frame direito - Carrinho
        right_frame = tk.Frame(content_frame, bg="#ffffff", relief=tk.FLAT, bd=0)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Card Carrinho
        card_carrinho = tk.Frame(right_frame, bg="#ffffff", relief=tk.FLAT, bd=1,
                                highlightbackground="#e0e0e0", highlightthickness=1)
        card_carrinho.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        carrinho_header = tk.Frame(card_carrinho, bg="#FF9800", height=50)
        carrinho_header.pack(fill=tk.X)
        carrinho_header.pack_propagate(False)
        
        tk.Label(carrinho_header, text="🛒 Itens do Orçamento", font=("Segoe UI", 14, "bold"),
                bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=15, pady=12)
        
        carrinho_body = tk.Frame(card_carrinho, bg="#ffffff")
        carrinho_body.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns_carrinho = ('Produto', 'Qtd', 'Preço Unit.', 'Subtotal')
        self.tree_carrinho = ttk.Treeview(carrinho_body, columns=columns_carrinho, show='headings', height=15)
        
        for col in columns_carrinho:
            self.tree_carrinho.heading(col, text=col)
            if col == 'Produto':
                self.tree_carrinho.column(col, width=200)
            else:
                self.tree_carrinho.column(col, width=120)
        
        scrollbar_carrinho = ttk.Scrollbar(carrinho_body, orient=tk.VERTICAL, command=self.tree_carrinho.yview)
        self.tree_carrinho.configure(yscrollcommand=scrollbar_carrinho.set)
        
        self.tree_carrinho.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_carrinho.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Card Validade e Total
        card_totais = tk.Frame(right_frame, bg="#ffffff", relief=tk.FLAT, bd=1,
                               highlightbackground="#e0e0e0", highlightthickness=1)
        card_totais.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        totais_header = tk.Frame(card_totais, bg="#f5f5f5", height=40)
        totais_header.pack(fill=tk.X)
        totais_header.pack_propagate(False)
        
        tk.Label(totais_header, text="💰 Totais", font=("Segoe UI", 12, "bold"),
                bg="#f5f5f5", fg="#333").pack(side=tk.LEFT, padx=15, pady=10)
        
        totais_body = tk.Frame(card_totais, bg="#ffffff")
        totais_body.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(totais_body, text="Dias de validade:", font=("Segoe UI", 11),
                bg="#ffffff", fg="#333").pack(anchor=tk.W, pady=(0, 5))
        self.validade_entry = tk.Entry(totais_body, font=("Segoe UI", 11), width=15)
        self.validade_entry.insert(0, "30")
        self.validade_entry.pack(anchor=tk.W, pady=(0, 15))
        
        # Total destacado
        total_frame = tk.Frame(totais_body, bg="#4CAF50", relief=tk.FLAT)
        total_frame.pack(fill=tk.X, pady=(0, 0))
        
        tk.Label(total_frame, text="TOTAL", font=("Segoe UI", 11, "bold"),
                bg="#4CAF50", fg="white").pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        self.total_label = tk.Label(total_frame, text="R$ 0,00",
                                   font=("Segoe UI", 24, "bold"),
                                   bg="#4CAF50", fg="white")
        self.total_label.pack(padx=15, pady=(0, 15))
        
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

