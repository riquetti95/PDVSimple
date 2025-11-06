"""
Painel de Vendas - Versão para exibir dentro da janela principal
"""
import tkinter as tk
from tkinter import ttk, messagebox
from vendas import Vendas
from produtos import Produtos
from clientes import Clientes
from cupom import Cupom

class VendasPanel:
    def __init__(self, parent, auth):
        self.parent = parent
        self.auth = auth
        self.vendas = Vendas()
        self.produtos = Produtos()
        self.clientes = Clientes()
        self.cupom = Cupom()
        
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
        
        # Ícone de carrinho + título
        title_container = tk.Frame(title_inner, bg="#ffffff")
        title_container.pack(side=tk.LEFT)
        
        # Ícone de carrinho
        from ui_icons import icon_manager
        carrinho_icon = icon_manager.get_carrinho_icon()
        if carrinho_icon:
            icon_label = tk.Label(title_container, image=carrinho_icon, bg="#ffffff")
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
        else:
            # Fallback para emoji
            icon_label = tk.Label(title_container, text="🛒", font=("Segoe UI", 24),
                                 bg="#ffffff", fg="#4CAF50")
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_container, text="Nova Venda",
                              font=("Segoe UI", 20, "bold"),
                              bg="#ffffff", fg="#333")
        title_label.pack(side=tk.LEFT)
        
        # Container do conteúdo
        content_frame = tk.Frame(main_frame, bg="#f5f5f5")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame esquerdo - Busca de produtos
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
        
        # Carrinho com ícone
        frame_carrinho = tk.LabelFrame(right_frame, text="",
                                      font=("Segoe UI", 11, "bold"),
                                      bg="#ffffff", fg="#333",
                                      relief=tk.FLAT, bd=1)
        frame_carrinho.pack(fill=tk.BOTH, expand=True, padx=15, pady=(15, 10))
        
        # Título do carrinho com ícone
        carrinho_title = tk.Frame(frame_carrinho, bg="#ffffff")
        carrinho_title.pack(fill=tk.X, padx=10, pady=10)
        
        from ui_icons import icon_manager
        carrinho_icon = icon_manager.get_carrinho_icon()
        if carrinho_icon:
            carrinho_icon_label = tk.Label(carrinho_title, image=carrinho_icon, bg="#ffffff")
            carrinho_icon_label.pack(side=tk.LEFT, padx=(0, 8))
        else:
            carrinho_icon_label = tk.Label(carrinho_title, text="🛒", font=("Segoe UI", 16),
                                          bg="#ffffff", fg="#4CAF50")
            carrinho_icon_label.pack(side=tk.LEFT, padx=(0, 8))
        
        carrinho_label = tk.Label(carrinho_title, text="Carrinho",
                                  font=("Segoe UI", 11, "bold"),
                                  bg="#ffffff", fg="#333")
        carrinho_label.pack(side=tk.LEFT)
        
        # Frame para a treeview do carrinho
        carrinho_tree_frame = tk.Frame(frame_carrinho, bg="#ffffff")
        carrinho_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        columns_carrinho = ('Produto', 'Qtd', 'Preço Unit.', 'Subtotal')
        self.tree_carrinho = ttk.Treeview(frame_carrinho, columns=columns_carrinho, show='headings', height=15)
        
        for col in columns_carrinho:
            self.tree_carrinho.heading(col, text=col)
            self.tree_carrinho.column(col, width=120)
        
        scrollbar_carrinho = ttk.Scrollbar(carrinho_tree_frame, orient=tk.VERTICAL, command=self.tree_carrinho.yview)
        self.tree_carrinho.configure(yscrollcommand=scrollbar_carrinho.set)
        
        self.tree_carrinho.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_carrinho.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_carrinho.bind('<Double-1>', lambda e: self.remover_item())
        
        # Totais
        frame_totais = tk.LabelFrame(right_frame, text="Totais",
                                    font=("Segoe UI", 11, "bold"),
                                    bg="#ffffff", fg="#333",
                                    relief=tk.FLAT, bd=1)
        frame_totais.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.subtotal_label = tk.Label(frame_totais, text="Subtotal: R$ 0,00",
                                       font=("Segoe UI", 11),
                                       bg="#ffffff", fg="#333")
        self.subtotal_label.pack(pady=10)
        
        tk.Label(frame_totais, text="Desconto:", font=("Segoe UI", 10),
                bg="#ffffff", fg="#333").pack()
        self.desconto_entry = tk.Entry(frame_totais, font=("Segoe UI", 10), width=15)
        self.desconto_entry.pack(pady=5)
        self.desconto_entry.insert(0, "0")
        self.desconto_entry.bind('<KeyRelease>', lambda e: self.calcular_total())
        
        self.total_label = tk.Label(frame_totais, text="Total: R$ 0,00",
                                    font=("Segoe UI", 16, "bold"),
                                    bg="#ffffff", fg="#4CAF50")
        self.total_label.pack(pady=10)
        
        # Botões
        frame_buttons = tk.Frame(right_frame, bg="#ffffff")
        frame_buttons.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        btn_finalizar = tk.Button(frame_buttons, text="Finalizar Venda",
                                 bg="#4CAF50", fg="white",
                                 font=("Segoe UI", 11, "bold"),
                                 relief=tk.FLAT, cursor="hand2",
                                 padx=20, pady=12,
                                 command=self.finalizar_venda)
        btn_finalizar.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        btn_limpar = tk.Button(frame_buttons, text="Limpar",
                              bg="#FF9800", fg="white",
                              font=("Segoe UI", 11),
                              relief=tk.FLAT, cursor="hand2",
                              padx=20, pady=12,
                              command=self.limpar_carrinho)
        btn_limpar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Carregar produtos
        self.load_produtos()
    
    def load_produtos(self):
        """Carrega lista de produtos"""
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        produtos = self.produtos.list_all()
        for produto in produtos:
            if produto[5] > 0:  # Apenas produtos com estoque
                self.tree_produtos.insert('', tk.END, values=(
                    produto[1], produto[2], f"R$ {produto[4]:.2f}", produto[5]
                ), tags=(produto[0],))
    
    def buscar_produto_auto(self):
        """Busca automática de produtos"""
        search = self.search_entry.get()
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        produtos = self.produtos.list_all(search)
        for produto in produtos:
            if produto[5] > 0:
                self.tree_produtos.insert('', tk.END, values=(
                    produto[1], produto[2], f"R$ {produto[4]:.2f}", produto[5]
                ), tags=(produto[0],))
    
    def selecionar_cliente(self):
        """Abre diálogo para selecionar cliente"""
        from ui_selecionar_cliente import SelecionarClienteWindow
        root_window = self.parent.winfo_toplevel()
        SelecionarClienteWindow(root_window, self.clientes, callback=self.set_cliente)
    
    def set_cliente(self, cliente):
        """Define o cliente selecionado"""
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
        
        if produto['estoque_atual'] <= 0:
            messagebox.showwarning("Aviso", "Produto sem estoque!")
            return
        
        quantidade = self.pedir_quantidade(produto)
        if quantidade <= 0:
            return
        
        for i, item_carrinho in enumerate(self.carrinho):
            if item_carrinho['produto_id'] == produto_id:
                nova_qtd = item_carrinho['quantidade'] + quantidade
                if nova_qtd > produto['estoque_atual']:
                    messagebox.showwarning("Aviso", "Quantidade excede o estoque disponível!")
                    return
                item_carrinho['quantidade'] = nova_qtd
                item_carrinho['subtotal'] = nova_qtd * item_carrinho['preco_unitario']
                self.atualizar_carrinho()
                return
        
        if quantidade > produto['estoque_atual']:
            messagebox.showwarning("Aviso", "Quantidade excede o estoque disponível!")
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
        """Solicita quantidade do produto"""
        dialog = tk.Toplevel(self.parent.winfo_toplevel())
        dialog.title("Quantidade")
        dialog.geometry("300x150")
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Produto: {produto['descricao']}", font=("Segoe UI", 10)).pack(pady=10)
        tk.Label(dialog, text=f"Estoque: {produto['estoque_atual']}", font=("Segoe UI", 9)).pack()
        
        quantidade_var = tk.StringVar(value="1")
        entry = tk.Entry(dialog, textvariable=quantidade_var, font=("Segoe UI", 12), width=10)
        entry.pack(pady=10)
        entry.focus()
        entry.select_range(0, tk.END)
        
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
    
    def remover_item(self):
        """Remove item do carrinho"""
        selection = self.tree_carrinho.selection()
        if not selection:
            return
        
        if messagebox.askyesno("Confirmar", "Deseja remover este item?"):
            index = self.tree_carrinho.index(selection[0])
            self.carrinho.pop(index)
            self.atualizar_carrinho()
    
    def limpar_carrinho(self):
        """Limpa o carrinho"""
        if messagebox.askyesno("Confirmar", "Deseja limpar o carrinho?"):
            self.carrinho = []
            self.atualizar_carrinho()
    
    def atualizar_carrinho(self):
        """Atualiza exibição do carrinho"""
        for item in self.tree_carrinho.get_children():
            self.tree_carrinho.delete(item)
        
        for item in self.carrinho:
            self.tree_carrinho.insert('', tk.END, values=(
                item['descricao'][:30],
                item['quantidade'],
                f"R$ {item['preco_unitario']:.2f}",
                f"R$ {item['subtotal']:.2f}"
            ))
        
        self.calcular_total()
    
    def calcular_total(self):
        """Calcula totais"""
        subtotal = sum(item['subtotal'] for item in self.carrinho)
        
        try:
            desconto = float(self.desconto_entry.get().replace(',', '.'))
        except:
            desconto = 0
        
        total = subtotal - desconto
        
        self.subtotal_label.config(text=f"Subtotal: R$ {subtotal:.2f}")
        self.total_label.config(text=f"Total: R$ {total:.2f}")
    
    def finalizar_venda(self):
        """Finaliza a venda"""
        if not self.carrinho:
            messagebox.showwarning("Aviso", "Adicione produtos ao carrinho!")
            return
        
        try:
            desconto = float(self.desconto_entry.get().replace(',', '.'))
        except:
            desconto = 0
        
        usuario_id = self.auth.get_current_user()['id']
        
        try:
            venda_id = self.vendas.create(
                self.cliente_id,
                usuario_id,
                self.carrinho,
                desconto=desconto
            )
            
            messagebox.showinfo("Sucesso", f"Venda finalizada com sucesso!\nNúmero: {venda_id}")
            
            # Limpar carrinho
            self.carrinho = []
            self.cliente_id = None
            self.cliente_label.config(text="Nenhum cliente selecionado")
            self.desconto_entry.delete(0, tk.END)
            self.desconto_entry.insert(0, "0")
            self.atualizar_carrinho()
            
            # Gerar cupom
            if messagebox.askyesno("Cupom", "Deseja visualizar o cupom não fiscal?"):
                self.visualizar_cupom(venda_id)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao finalizar venda: {str(e)}")
    
    def visualizar_cupom(self, venda_id):
        """Visualiza o cupom"""
        cupom_texto = self.cupom.gerar_cupom(venda_id)
        if cupom_texto:
            from ui_cupom_view import CupomViewWindow
            root_window = self.parent.winfo_toplevel()
            CupomViewWindow(root_window, cupom_texto, venda_id)
    
    def voltar_dashboard(self):
        """Volta para o dashboard"""
        # Acessar MainWindow através da referência armazenada
        if hasattr(self.parent, 'main_window'):
            self.parent.main_window.show_dashboard()

