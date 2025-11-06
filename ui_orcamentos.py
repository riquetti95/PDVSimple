"""
Tela de Orçamentos
"""
import tkinter as tk
from tkinter import ttk, messagebox
from orcamentos import Orcamentos
from produtos import Produtos
from clientes import Clientes

class OrcamentosWindow:
    def __init__(self, root, auth):
        self.root = root
        self.auth = auth
        self.orcamentos = Orcamentos()
        self.produtos = Produtos()
        self.clientes = Clientes()
        
        self.carrinho = []
        self.cliente_id = None
        
        self.window = tk.Toplevel(root)
        self.window.title("Novo Orçamento")
        self.window.geometry("1200x700")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
        # Similar à tela de vendas, mas para orçamentos
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame esquerdo
        left_frame = tk.Frame(main_frame, width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Cliente
        frame_cliente = tk.LabelFrame(left_frame, text="Cliente", font=("Arial", 10, "bold"))
        frame_cliente.pack(fill=tk.X, pady=(0, 10))
        
        self.cliente_label = tk.Label(frame_cliente, text="Nenhum cliente selecionado", font=("Arial", 9))
        self.cliente_label.pack(padx=10, pady=10)
        
        btn_selecionar_cliente = tk.Button(frame_cliente, text="Selecionar Cliente",
                                          command=self.selecionar_cliente, cursor="hand2")
        btn_selecionar_cliente.pack(pady=5)
        
        # Busca de produtos
        frame_busca = tk.LabelFrame(left_frame, text="Buscar Produto", font=("Arial", 10, "bold"))
        frame_busca.pack(fill=tk.X, pady=(0, 10))
        
        self.search_entry = tk.Entry(frame_busca, font=("Arial", 12))
        self.search_entry.pack(fill=tk.X, padx=10, pady=10)
        self.search_entry.bind('<KeyRelease>', lambda e: self.buscar_produto_auto())
        
        # Lista de produtos
        frame_produtos = tk.LabelFrame(left_frame, text="Produtos", font=("Arial", 10, "bold"))
        frame_produtos.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Código', 'Descrição', 'Preço', 'Estoque')
        self.tree_produtos = ttk.Treeview(frame_produtos, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree_produtos.heading(col, text=col)
            self.tree_produtos.column(col, width=90)
        
        scrollbar = ttk.Scrollbar(frame_produtos, orient=tk.VERTICAL, command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        self.tree_produtos.bind('<Double-1>', lambda e: self.adicionar_produto())
        
        # Frame direito - Carrinho
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Carrinho
        frame_carrinho = tk.LabelFrame(right_frame, text="Itens do Orçamento", font=("Arial", 10, "bold"))
        frame_carrinho.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
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
        frame_validade = tk.LabelFrame(right_frame, text="Validade", font=("Arial", 10, "bold"))
        frame_validade.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(frame_validade, text="Dias de validade:", font=("Arial", 10)).pack()
        self.validade_entry = tk.Entry(frame_validade, font=("Arial", 10), width=15)
        self.validade_entry.insert(0, "30")
        self.validade_entry.pack(pady=5)
        
        # Total
        self.total_label = tk.Label(frame_validade, text="Total: R$ 0,00", font=("Arial", 14, "bold"))
        self.total_label.pack(pady=5)
        
        # Botões
        frame_buttons = tk.Frame(right_frame)
        frame_buttons.pack(fill=tk.X)
        
        btn_salvar = tk.Button(frame_buttons, text="Salvar Orçamento", bg="#4CAF50", fg="white",
                              font=("Arial", 12, "bold"), padx=20, pady=10,
                              command=self.salvar_orcamento, cursor="hand2")
        btn_salvar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = tk.Button(frame_buttons, text="Cancelar", bg="#f44336", fg="white",
                               font=("Arial", 12), padx=20, pady=10,
                               command=self.window.destroy, cursor="hand2")
        btn_cancelar.pack(side=tk.LEFT, padx=5)
        
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
        SelecionarClienteWindow(self.window, self.clientes, callback=self.set_cliente)
    
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
        
        # Verificar se já está no carrinho
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
        dialog = tk.Toplevel(self.window)
        dialog.title("Quantidade")
        dialog.geometry("300x150")
        dialog.transient(self.window)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Produto: {produto['descricao']}", font=("Arial", 10)).pack(pady=10)
        
        quantidade_var = tk.StringVar(value="1")
        entry = tk.Entry(dialog, textvariable=quantidade_var, font=("Arial", 12), width=10)
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
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar orçamento: {str(e)}")

class ListaOrcamentosWindow:
    def __init__(self, root, auth):
        self.root = root
        self.auth = auth
        self.orcamentos = Orcamentos()
        
        self.window = tk.Toplevel(root)
        self.window.title("Orçamentos")
        self.window.geometry("1000x600")
        
        # Frame de filtros
        frame_filtros = tk.Frame(self.window)
        frame_filtros.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_filtros, text="Status:").pack(side=tk.LEFT, padx=5)
        self.status_var = tk.StringVar(value="Todos")
        status_combo = ttk.Combobox(frame_filtros, textvariable=self.status_var,
                                   values=["Todos", "Aberto", "Aprovado", "Cancelado", "Vendido"],
                                   state="readonly", width=15)
        status_combo.pack(side=tk.LEFT, padx=5)
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.load_orcamentos())
        
        btn_buscar = tk.Button(frame_filtros, text="Buscar", command=self.load_orcamentos, cursor="hand2")
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        # Treeview
        frame_tree = tk.Frame(self.window)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Número', 'Data', 'Cliente', 'Valor', 'Status', 'Validade')
        self.tree = ttk.Treeview(frame_tree, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<Double-1>', lambda e: self.ver_detalhes())
        
        # Botões de ação
        frame_buttons = tk.Frame(self.window)
        frame_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        btn_aprovar = tk.Button(frame_buttons, text="Aprovar", bg="#4CAF50", fg="white",
                               command=self.aprovar_orcamento, cursor="hand2")
        btn_aprovar.pack(side=tk.LEFT, padx=5)
        
        btn_converter = tk.Button(frame_buttons, text="Converter em Venda", bg="#2196F3", fg="white",
                                 command=self.converter_venda, cursor="hand2")
        btn_converter.pack(side=tk.LEFT, padx=5)
        
        self.load_orcamentos()
    
    def load_orcamentos(self):
        """Carrega orçamentos"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        status = None if self.status_var.get() == "Todos" else self.status_var.get()
        orcamentos = self.orcamentos.list_all(status)
        
        for orc in orcamentos:
            self.tree.insert('', tk.END, values=orc, tags=(orc[0],))
    
    def ver_detalhes(self):
        """Ver detalhes"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        orcamento_id = item['tags'][0]
        
        orcamento = self.orcamentos.get_by_id(orcamento_id)
        if orcamento:
            messagebox.showinfo("Orçamento", f"Número: {orcamento['numero']}\n"
                                           f"Cliente: {orcamento.get('cliente_nome', 'N/A')}\n"
                                           f"Valor: R$ {orcamento['valor_total']:.2f}\n"
                                           f"Status: {orcamento['status']}")
    
    def aprovar_orcamento(self):
        """Aprova orçamento"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um orçamento!")
            return
        
        item = self.tree.item(selection[0])
        orcamento_id = item['tags'][0]
        
        if messagebox.askyesno("Confirmar", "Deseja aprovar este orçamento?"):
            self.orcamentos.atualizar_status(orcamento_id, 'Aprovado')
            self.load_orcamentos()
    
    def converter_venda(self):
        """Converte orçamento em venda"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um orçamento!")
            return
        
        item = self.tree.item(selection[0])
        orcamento_id = item['tags'][0]
        
        orcamento = self.orcamentos.get_by_id(orcamento_id)
        if orcamento['status'] != 'Aprovado':
            messagebox.showwarning("Aviso", "Apenas orçamentos aprovados podem ser convertidos em venda!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja converter este orçamento em venda?"):
            usuario_id = self.auth.get_current_user()['id']
            venda_id = self.orcamentos.converter_para_venda(orcamento_id, usuario_id)
            if venda_id:
                messagebox.showinfo("Sucesso", f"Orçamento convertido em venda!\nVenda ID: {venda_id}")
                self.load_orcamentos()

