"""
Tela de Vendas
"""
import tkinter as tk
from tkinter import ttk, messagebox
from vendas import Vendas
from produtos import Produtos
from clientes import Clientes
from cupom import Cupom

class VendasWindow:
    def __init__(self, root, auth):
        self.root = root
        self.auth = auth
        self.vendas = Vendas()
        self.produtos = Produtos()
        self.clientes = Clientes()
        self.cupom = Cupom()
        
        self.carrinho = []
        self.cliente_id = None
        
        self.window = tk.Toplevel(root)
        self.window.title("Nova Venda")
        self.window.geometry("1200x700")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
        # Frame principal
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame esquerdo - Busca de produtos
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
        self.search_entry.bind('<Return>', lambda e: self.buscar_produto())
        self.search_entry.bind('<KeyRelease>', lambda e: self.buscar_produto_auto())
        
        btn_buscar = tk.Button(frame_busca, text="Buscar", command=self.buscar_produto, cursor="hand2")
        btn_buscar.pack(pady=5)
        
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
        frame_carrinho = tk.LabelFrame(right_frame, text="Carrinho", font=("Arial", 10, "bold"))
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
        
        self.tree_carrinho.bind('<Double-1>', lambda e: self.remover_item())
        
        # Totais
        frame_totais = tk.LabelFrame(right_frame, text="Totais", font=("Arial", 10, "bold"))
        frame_totais.pack(fill=tk.X, pady=(0, 10))
        
        self.subtotal_label = tk.Label(frame_totais, text="Subtotal: R$ 0,00", font=("Arial", 12))
        self.subtotal_label.pack(pady=5)
        
        tk.Label(frame_totais, text="Desconto:", font=("Arial", 10)).pack()
        self.desconto_entry = tk.Entry(frame_totais, font=("Arial", 10), width=15)
        self.desconto_entry.pack(pady=5)
        self.desconto_entry.insert(0, "0")
        self.desconto_entry.bind('<KeyRelease>', lambda e: self.calcular_total())
        
        self.total_label = tk.Label(frame_totais, text="Total: R$ 0,00", font=("Arial", 14, "bold"))
        self.total_label.pack(pady=5)
        
        # Botões
        frame_buttons = tk.Frame(right_frame)
        frame_buttons.pack(fill=tk.X)
        
        btn_finalizar = tk.Button(frame_buttons, text="Finalizar Venda", bg="#4CAF50", fg="white",
                                 font=("Arial", 12, "bold"), padx=20, pady=10,
                                 command=self.finalizar_venda, cursor="hand2")
        btn_finalizar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = tk.Button(frame_buttons, text="Cancelar", bg="#f44336", fg="white",
                                font=("Arial", 12), padx=20, pady=10,
                                command=self.window.destroy, cursor="hand2")
        btn_cancelar.pack(side=tk.LEFT, padx=5)
        
        btn_limpar = tk.Button(frame_buttons, text="Limpar", bg="#FF9800", fg="white",
                              font=("Arial", 12), padx=20, pady=10,
                              command=self.limpar_carrinho, cursor="hand2")
        btn_limpar.pack(side=tk.LEFT, padx=5)
        
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
    
    def buscar_produto(self):
        """Busca produto e adiciona ao carrinho"""
        self.buscar_produto_auto()
        if self.tree_produtos.selection():
            self.adicionar_produto()
    
    def selecionar_cliente(self):
        """Abre diálogo para selecionar cliente"""
        from ui_selecionar_cliente import SelecionarClienteWindow
        SelecionarClienteWindow(self.window, self.clientes, callback=self.set_cliente)
    
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
        
        # Verificar estoque
        if produto['estoque_atual'] <= 0:
            messagebox.showwarning("Aviso", "Produto sem estoque!")
            return
        
        # Pedir quantidade
        quantidade = self.pedir_quantidade(produto)
        if quantidade <= 0:
            return
        
        # Verificar se já está no carrinho
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
        
        # Adicionar novo item
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
        dialog = tk.Toplevel(self.window)
        dialog.title("Quantidade")
        dialog.geometry("300x150")
        dialog.transient(self.window)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Produto: {produto['descricao']}", font=("Arial", 10)).pack(pady=10)
        tk.Label(dialog, text=f"Estoque: {produto['estoque_atual']}", font=("Arial", 9)).pack()
        
        quantidade_var = tk.StringVar(value="1")
        entry = tk.Entry(dialog, textvariable=quantidade_var, font=("Arial", 12), width=10)
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
            
            # Gerar cupom
            if messagebox.askyesno("Cupom", "Deseja visualizar o cupom não fiscal?"):
                self.visualizar_cupom(venda_id)
            
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao finalizar venda: {str(e)}")
    
    def visualizar_cupom(self, venda_id):
        """Visualiza o cupom"""
        cupom_texto = self.cupom.gerar_cupom(venda_id)
        if cupom_texto:
            from ui_cupom_view import CupomViewWindow
            CupomViewWindow(self.window, cupom_texto, venda_id)

class HistoricoVendasWindow:
    def __init__(self, root, auth):
        self.root = root
        self.auth = auth
        self.vendas = Vendas()
        
        self.window = tk.Toplevel(root)
        self.window.title("Histórico de Vendas")
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
        
        btn_buscar = tk.Button(frame_filtros, text="Buscar", command=self.load_vendas, cursor="hand2")
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        # Treeview
        frame_tree = tk.Frame(self.window)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Número', 'Data', 'Cliente', 'Total', 'Status')
        self.tree = ttk.Treeview(frame_tree, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<Double-1>', lambda e: self.ver_detalhes())
        
        self.load_vendas()
    
    def load_vendas(self):
        """Carrega vendas"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        data_inicio = self.data_inicio.get() or None
        data_fim = self.data_fim.get() or None
        
        vendas = self.vendas.list_all(data_inicio, data_fim)
        for venda in vendas:
            self.tree.insert('', tk.END, values=venda, tags=(venda[0],))
    
    def ver_detalhes(self):
        """Ver detalhes da venda"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        venda_id = item['tags'][0]
        
        venda = self.vendas.get_by_id(venda_id)
        if venda:
            from ui_detalhes_venda import DetalhesVendaWindow
            DetalhesVendaWindow(self.window, venda, self.vendas, self.auth)

