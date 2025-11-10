"""
Painel de Vendas - Versão moderna e rápida para PDV
"""
import tkinter as tk
from tkinter import ttk, messagebox
from vendas import Vendas
from produtos import Produtos
from clientes import Clientes
from cupom import Cupom
import os
from PIL import Image, ImageTk

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
        self.produto_selecionado = None
        self.quantidade_var = tk.StringVar(value="1")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
        # Frame principal com gradiente visual
        main_frame = tk.Frame(self.parent, bg="#f0f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header moderno
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
        
        from ui_icons import icon_manager
        carrinho_icon = icon_manager.get_carrinho_icon()
        if carrinho_icon:
            icon_label = tk.Label(title_container, image=carrinho_icon, bg="#2196F3")
            icon_label.pack(side=tk.LEFT, padx=(0, 12))
        else:
            icon_label = tk.Label(title_container, text="🛒", font=("Segoe UI", 28),
                                 bg="#2196F3", fg="white")
            icon_label.pack(side=tk.LEFT, padx=(0, 12))
        
        title_label = tk.Label(title_container, text="Nova Venda",
                              font=("Segoe UI", 24, "bold"),
                              bg="#2196F3", fg="white")
        title_label.pack(side=tk.LEFT)
        
        # Container do conteúdo
        content_frame = tk.Frame(main_frame, bg="#f0f4f8")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Frame esquerdo - Área de produtos
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
        
        tk.Label(busca_header, text="🔍 Buscar Produto", font=("Segoe UI", 11, "bold"),
                bg="#f5f5f5", fg="#333").pack(side=tk.LEFT, padx=15, pady=10)
        
        busca_body = tk.Frame(card_busca, bg="#ffffff")
        busca_body.pack(fill=tk.X, padx=15, pady=10)
        
        self.search_entry = tk.Entry(busca_body, font=("Segoe UI", 11),
                                     relief=tk.FLAT, bd=1, highlightthickness=1,
                                     highlightbackground="#4CAF50",
                                     highlightcolor="#4CAF50",
                                     bg="#fafafa", insertbackground="#333")
        self.search_entry.pack(fill=tk.X, ipady=8)
        self.search_entry.bind('<KeyRelease>', lambda e: self.buscar_produto_auto())
        self.search_entry.bind('<Return>', lambda e: self.adicionar_produto_rapido())
        self.search_entry.focus()
        
        # Frame para produtos e controles
        produtos_container = tk.Frame(left_frame, bg="#ffffff")
        produtos_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Lista de produtos - Card
        card_produtos = tk.Frame(produtos_container, bg="#ffffff", relief=tk.FLAT, bd=1,
                                highlightbackground="#e0e0e0", highlightthickness=1)
        card_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        produtos_header = tk.Frame(card_produtos, bg="#f5f5f5", height=40)
        produtos_header.pack(fill=tk.X)
        produtos_header.pack_propagate(False)
        
        tk.Label(produtos_header, text="📦 Produtos Disponíveis", font=("Segoe UI", 12, "bold"),
                bg="#f5f5f5", fg="#333").pack(side=tk.LEFT, padx=15, pady=10)
        
        produtos_body = tk.Frame(card_produtos, bg="#ffffff")
        produtos_body.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('Código', 'Descrição', 'Preço', 'Estoque')
        self.tree_produtos = ttk.Treeview(produtos_body, columns=columns, show='headings', height=18)
        
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        
        for col in columns:
            self.tree_produtos.heading(col, text=col)
            if col == 'Descrição':
                self.tree_produtos.column(col, width=250)
            else:
                self.tree_produtos.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(produtos_body, orient=tk.VERTICAL, command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_produtos.bind('<ButtonRelease-1>', lambda e: self.selecionar_produto())
        self.tree_produtos.bind('<Button-1>', lambda e: self.parent.after(10, self.selecionar_produto))
        self.tree_produtos.bind('<Return>', lambda e: self.adicionar_produto_rapido())
        self.tree_produtos.bind('<Double-1>', lambda e: self.adicionar_produto_rapido())
        
        # Card Controles de Quantidade e Adicionar
        card_controles = tk.Frame(produtos_container, bg="#ffffff", relief=tk.FLAT, bd=1,
                                 highlightbackground="#e0e0e0", highlightthickness=1)
        card_controles.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 0))
        
        controles_header = tk.Frame(card_controles, bg="#f5f5f5", height=40)
        controles_header.pack(fill=tk.X)
        controles_header.pack_propagate(False)
        
        tk.Label(controles_header, text="⚙️ Controles", font=("Segoe UI", 12, "bold"),
                bg="#f5f5f5", fg="#333").pack(side=tk.LEFT, padx=15, pady=10)
        
        controles_body = tk.Frame(card_controles, bg="#ffffff")
        controles_body.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Foto do produto
        frame_foto = tk.LabelFrame(controles_body, text="Foto da Peça",
                                  font=("Segoe UI", 11, "bold"),
                                  bg="#ffffff", fg="#333",
                                  relief=tk.FLAT, bd=1)
        frame_foto.pack(fill=tk.X, pady=(0, 15))
        
        # Frame para centralizar a foto com tamanho fixo
        foto_container = tk.Frame(frame_foto, bg="#f0f0f0", width=250, height=250)
        foto_container.pack(padx=10, pady=10)
        foto_container.pack_propagate(False)  # Manter tamanho fixo
        
        self.foto_produto_label = tk.Label(foto_container, text="📷\nSelecione um produto",
                                          font=("Segoe UI", 10),
                                          bg="#f0f0f0", fg="#999",
                                          width=250, height=250,
                                          relief=tk.SOLID, bd=1,
                                          justify=tk.CENTER)
        self.foto_produto_label.pack(fill=tk.BOTH, expand=True)
        self.foto_produto_image = None
        
        # Quantidade - Card destacado
        frame_qtd = tk.LabelFrame(controles_body, text="Quantidade",
                                 font=("Segoe UI", 11, "bold"),
                                 bg="#ffffff", fg="#333",
                                 relief=tk.FLAT, bd=1)
        frame_qtd.pack(fill=tk.X, pady=(0, 15))
        
        qtd_controls = tk.Frame(frame_qtd, bg="#ffffff")
        qtd_controls.pack(padx=10, pady=15)
        
        btn_menos = tk.Button(qtd_controls, text="−", font=("Segoe UI", 18, "bold"),
                             bg="#f44336", fg="white",
                             relief=tk.FLAT, cursor="hand2",
                             width=3, height=1,
                             activebackground="#d32f2f",
                             command=self.diminuir_quantidade)
        btn_menos.pack(side=tk.LEFT, padx=(0, 10))
        
        self.qtd_entry = tk.Entry(qtd_controls, textvariable=self.quantidade_var,
                                  font=("Segoe UI", 16, "bold"),
                                  width=8, justify=tk.CENTER,
                                  relief=tk.SOLID, bd=2,
                                  highlightthickness=2,
                                  highlightbackground="#4CAF50",
                                  highlightcolor="#4CAF50")
        self.qtd_entry.pack(side=tk.LEFT, padx=5)
        self.qtd_entry.bind('<KeyRelease>', lambda e: self.validar_quantidade())
        self.qtd_entry.bind('<Return>', lambda e: self.adicionar_produto_rapido())
        
        btn_mais = tk.Button(qtd_controls, text="+", font=("Segoe UI", 18, "bold"),
                            bg="#4CAF50", fg="white",
                            relief=tk.FLAT, cursor="hand2",
                            width=3, height=1,
                            activebackground="#45a049",
                            command=self.aumentar_quantidade)
        btn_mais.pack(side=tk.LEFT, padx=(10, 0))
        
        # Botão grande de adicionar
        btn_adicionar = tk.Button(controles_body, text="➕ ADICIONAR AO CARRINHO",
                                 font=("Segoe UI", 14, "bold"),
                                 bg="#4CAF50", fg="white",
                                 relief=tk.FLAT, cursor="hand2",
                                 padx=20, pady=20,
                                 activebackground="#45a049",
                                 activeforeground="white",
                                 command=self.adicionar_produto_rapido)
        btn_adicionar.pack(fill=tk.X, pady=(0, 0))
        
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
        
        carrinho_title = tk.Frame(carrinho_header, bg="#FF9800")
        carrinho_title.pack(side=tk.LEFT, padx=15, pady=12)
        
        from ui_icons import icon_manager
        carrinho_icon = icon_manager.get_carrinho_icon()
        if carrinho_icon:
            carrinho_icon_label = tk.Label(carrinho_title, image=carrinho_icon, bg="#FF9800")
            carrinho_icon_label.pack(side=tk.LEFT, padx=(0, 8))
        else:
            carrinho_icon_label = tk.Label(carrinho_title, text="🛒", font=("Segoe UI", 20),
                                          bg="#FF9800", fg="white")
            carrinho_icon_label.pack(side=tk.LEFT, padx=(0, 8))
        
        tk.Label(carrinho_title, text="Carrinho", font=("Segoe UI", 16, "bold"),
                bg="#FF9800", fg="white").pack(side=tk.LEFT)
        
        carrinho_body = tk.Frame(card_carrinho, bg="#ffffff")
        carrinho_body.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns_carrinho = ('Produto', 'Qtd', 'Preço Unit.', 'Subtotal')
        self.tree_carrinho = ttk.Treeview(carrinho_body, columns=columns_carrinho, show='headings', height=8)
        
        for col in columns_carrinho:
            self.tree_carrinho.heading(col, text=col)
            if col == 'Produto':
                self.tree_carrinho.column(col, width=200)
            else:
                self.tree_carrinho.column(col, width=100)
        
        scrollbar_carrinho = ttk.Scrollbar(carrinho_body, orient=tk.VERTICAL, command=self.tree_carrinho.yview)
        self.tree_carrinho.configure(yscrollcommand=scrollbar_carrinho.set)
        
        self.tree_carrinho.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_carrinho.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_carrinho.bind('<Double-1>', lambda e: self.remover_item())
        self.tree_carrinho.bind('<Delete>', lambda e: self.remover_item())
        
        # Variáveis para o modal (serão criadas quando necessário)
        self.desconto_entry = None
        self.forma_pagamento_var = None
        self.valor_recebido_entry = None
        
        # Botões de ação
        frame_buttons = tk.Frame(right_frame, bg="#ffffff")
        frame_buttons.pack(fill=tk.X, padx=15, pady=(15, 15))
        
        btn_finalizar = tk.Button(frame_buttons, text="✓ FINALIZAR VENDA",
                                 bg="#4CAF50", fg="white",
                                 font=("Segoe UI", 16, "bold"),
                                 relief=tk.FLAT, cursor="hand2",
                                 padx=30, pady=20,
                                 activebackground="#45a049",
                                 activeforeground="white",
                                 command=self.abrir_modal_finalizar)
        btn_finalizar.pack(fill=tk.X, pady=(0, 10))
        
        btn_limpar = tk.Button(frame_buttons, text="🗑️ Limpar Carrinho",
                              bg="#f44336", fg="white",
                              font=("Segoe UI", 12, "bold"),
                              relief=tk.FLAT, cursor="hand2",
                              padx=20, pady=12,
                              activebackground="#d32f2f",
                              activeforeground="white",
                              command=self.limpar_carrinho)
        btn_limpar.pack(fill=tk.X)
        
        # Carregar produtos de forma assíncrona para não travar a interface
        self.parent.after(100, self.load_produtos)
    
    def load_produtos(self):
        """Carrega lista de produtos (otimizado)"""
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        # Mostrar mensagem de carregamento
        self.tree_produtos.insert('', tk.END, values=('', 'Carregando...', '', ''))
        self.parent.update()  # Atualizar interface
        
        try:
            produtos = self.produtos.list_all()
            # Limpar mensagem de carregamento
            for item in self.tree_produtos.get_children():
                self.tree_produtos.delete(item)
            
            # Limitar a 100 produtos iniciais para performance
            produtos_com_estoque = [p for p in produtos if p[5] > 0]
            produtos_limite = produtos_com_estoque[:100]
            
            for produto in produtos_limite:
                self.tree_produtos.insert('', tk.END, values=(
                    produto[1], produto[2], f"R$ {produto[4]:.2f}", produto[5]
                ), tags=(produto[0],))
            
            # Se houver mais produtos, mostrar mensagem
            if len(produtos_com_estoque) > 100:
                self.tree_produtos.insert('', tk.END, values=(
                    '', f'... e mais {len(produtos_com_estoque) - 100} produtos. Use a busca.', '', ''
                ))
        except Exception as e:
            # Limpar mensagem de erro se houver
            for item in self.tree_produtos.get_children():
                self.tree_produtos.delete(item)
            self.tree_produtos.insert('', tk.END, values=('', 'Erro ao carregar produtos', '', ''))
    
    def buscar_produto_auto(self):
        """Busca automática de produtos (otimizado)"""
        search = self.search_entry.get()
        
        # Se busca vazia, recarregar lista limitada
        if not search.strip():
            self.load_produtos()
            return
        
        # Limpar lista
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        # Buscar produtos
        produtos = self.produtos.list_all(search)
        produtos_com_estoque = [p for p in produtos if p[5] > 0]
        
        for produto in produtos_com_estoque:
            self.tree_produtos.insert('', tk.END, values=(
                produto[1], produto[2], f"R$ {produto[4]:.2f}", produto[5]
            ), tags=(produto[0],))
        
        # Selecionar primeiro item se houver
        items = self.tree_produtos.get_children()
        if items:
            # Verificar se não é mensagem
            first_item = self.tree_produtos.item(items[0])
            if first_item['values'][1] != 'Carregando...' and first_item['values'][1] != 'Erro ao carregar produtos':
                self.tree_produtos.selection_set(items[0])
                self.tree_produtos.focus(items[0])
                self.selecionar_produto()
    
    def selecionar_produto(self):
        """Seleciona produto e mostra foto"""
        selection = self.tree_produtos.selection()
        if not selection:
            self.produto_selecionado = None
            self.mostrar_foto_produto()  # Limpar foto se não houver seleção
            return
        
        item = self.tree_produtos.item(selection[0])
        produto_id = int(item['tags'][0])
        
        # Recarregar produto do banco para garantir que tem foto_path atualizado
        produto = self.produtos.get_by_id(produto_id)
        
        if produto:
            self.produto_selecionado = produto
            self.mostrar_foto_produto()
            # Atualizar quantidade máxima disponível
            estoque = produto.get('estoque_atual', 0)
            if estoque > 0:
                try:
                    qtd_atual = float(self.quantidade_var.get().replace(',', '.'))
                    if qtd_atual > estoque:
                        self.quantidade_var.set("1")
                except:
                    self.quantidade_var.set("1")
    
    def mostrar_foto_produto(self):
        """Mostra a foto do produto selecionado"""
        if not self.produto_selecionado:
            self.foto_produto_label.config(image='', text="📷\nSelecione um produto",
                                          bg="#f0f0f0", fg="#999")
            return
        
        produto = self.produto_selecionado
        foto_path = produto.get('foto_path', '')
        
        if foto_path and foto_path.strip():
            # Normalizar caminho - aceitar tanto \ quanto /
            foto_path_original = foto_path.strip()
            
            # Tentar múltiplos caminhos
            caminhos_tentar = []
            
            # 1. Caminho original
            caminhos_tentar.append(foto_path_original)
            
            # 2. Normalizar separadores
            foto_path_norm = os.path.normpath(foto_path_original)
            caminhos_tentar.append(foto_path_norm)
            
            # 3. Caminho absoluto
            if not os.path.isabs(foto_path_norm):
                caminhos_tentar.append(os.path.abspath(foto_path_norm))
                caminhos_tentar.append(os.path.join(os.getcwd(), foto_path_norm))
            
            # 4. Apenas nome do arquivo em data/fotos_produtos
            nome_arquivo = os.path.basename(foto_path_original)
            if nome_arquivo:
                caminhos_tentar.append(os.path.join('data', 'fotos_produtos', nome_arquivo))
                caminhos_tentar.append(os.path.abspath(os.path.join('data', 'fotos_produtos', nome_arquivo)))
                caminhos_tentar.append(os.path.normpath(os.path.join('data', 'fotos_produtos', nome_arquivo)))
            
            # Tentar cada caminho
            foto_encontrada = None
            for caminho in caminhos_tentar:
                try:
                    # Normalizar o caminho
                    caminho_test = os.path.normpath(str(caminho))
                    if os.path.exists(caminho_test) and os.path.isfile(caminho_test):
                        foto_encontrada = caminho_test
                        break
                except Exception as e:
                    continue
            
            if foto_encontrada:
                try:
                    img = Image.open(foto_encontrada)
                    
                    # Tamanho fixo do picturebox
                    target_size = (250, 250)
                    
                    # Calcular dimensões para fazer zoom (preencher o espaço)
                    img_width, img_height = img.size
                    target_width, target_height = target_size
                    
                    # Calcular escala para preencher todo o espaço (zoom)
                    scale = max(target_width / img_width, target_height / img_height)
                    
                    # Novo tamanho após escala
                    new_width = int(img_width * scale)
                    new_height = int(img_height * scale)
                    
                    # Redimensionar a imagem
                    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Fazer crop centralizado para o tamanho exato
                    left = (new_width - target_width) // 2
                    top = (new_height - target_height) // 2
                    right = left + target_width
                    bottom = top + target_height
                    
                    img_cropped = img_resized.crop((left, top, right, bottom))
                    
                    # Converter para PhotoImage
                    self.foto_produto_image = ImageTk.PhotoImage(img_cropped)
                    self.foto_produto_label.config(image=self.foto_produto_image, text="", bg="#ffffff")
                    return
                except Exception as e:
                    pass  # Erro ao abrir imagem, manter "Sem foto"
        
        self.foto_produto_label.config(image='', text="📷\nSem foto", bg="#f0f0f0", fg="#999")
    
    def aumentar_quantidade(self):
        """Aumenta quantidade em 1"""
        try:
            qtd = float(self.quantidade_var.get().replace(',', '.'))
            if self.produto_selecionado:
                estoque = self.produto_selecionado.get('estoque_atual', 0)
                if qtd < estoque:
                    qtd += 1
            else:
                qtd += 1
            self.quantidade_var.set(str(int(qtd)))
        except:
            self.quantidade_var.set("1")
    
    def diminuir_quantidade(self):
        """Diminui quantidade em 1"""
        try:
            qtd = float(self.quantidade_var.get().replace(',', '.'))
            if qtd > 1:
                qtd -= 1
                self.quantidade_var.set(str(int(qtd)))
        except:
            self.quantidade_var.set("1")
    
    def validar_quantidade(self):
        """Valida quantidade digitada"""
        try:
            qtd = float(self.quantidade_var.get().replace(',', '.'))
            if self.produto_selecionado:
                estoque = self.produto_selecionado.get('estoque_atual', 0)
                if qtd > estoque:
                    self.quantidade_var.set(str(int(estoque)))
                elif qtd < 1:
                    self.quantidade_var.set("1")
        except:
            self.quantidade_var.set("1")
    
    def adicionar_produto_rapido(self):
        """Adiciona produto ao carrinho sem modal"""
        if not self.produto_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto primeiro!")
            return
        
        produto = self.produto_selecionado
        produto_id = produto['id']
        
        if produto['estoque_atual'] <= 0:
            messagebox.showwarning("Aviso", "Produto sem estoque!")
            return
        
        try:
            quantidade = float(self.quantidade_var.get().replace(',', '.'))
        except:
            quantidade = 1
        
        if quantidade <= 0:
            messagebox.showwarning("Aviso", "Quantidade inválida!")
            return
        
        # Verificar se já está no carrinho
        for item_carrinho in self.carrinho:
            if item_carrinho['produto_id'] == produto_id:
                nova_qtd = item_carrinho['quantidade'] + quantidade
                if nova_qtd > produto['estoque_atual']:
                    messagebox.showwarning("Aviso", f"Quantidade excede o estoque disponível!\nEstoque: {produto['estoque_atual']}")
                    return
                item_carrinho['quantidade'] = nova_qtd
                item_carrinho['subtotal'] = nova_qtd * item_carrinho['preco_unitario']
                self.atualizar_carrinho()
                self.quantidade_var.set("1")
                self.search_entry.focus()
                return
        
        if quantidade > produto['estoque_atual']:
            messagebox.showwarning("Aviso", f"Quantidade excede o estoque disponível!\nEstoque: {produto['estoque_atual']}")
            return
        
        self.carrinho.append({
            'produto_id': produto_id,
            'descricao': produto['descricao'],
            'quantidade': quantidade,
            'preco_unitario': produto['preco_venda'],
            'subtotal': quantidade * produto['preco_venda']
        })
        
        self.atualizar_carrinho()
        self.quantidade_var.set("1")
        self.search_entry.focus()
    
    def selecionar_cliente(self):
        """Abre diálogo para selecionar cliente"""
        from ui_selecionar_cliente import SelecionarClienteWindow
        root_window = self.parent.winfo_toplevel()
        SelecionarClienteWindow(root_window, self.clientes, callback=self.set_cliente)
    
    def set_cliente(self, cliente):
        """Define o cliente selecionado"""
        self.cliente_id = cliente['id']
        self.cliente_label.config(text=f"{cliente['nome']} - {cliente.get('cpf_cnpj', '')}")
    
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
                item['descricao'][:40],
                f"{item['quantidade']:.2f}",
                f"R$ {item['preco_unitario']:.2f}",
                f"R$ {item['subtotal']:.2f}"
            ))
        
    
    def abrir_modal_finalizar(self):
        """Abre modal para finalizar venda"""
        if not self.carrinho:
            messagebox.showwarning("Aviso", "Adicione produtos ao carrinho!")
            return
        
        # Calcular subtotal
        subtotal = sum(item['subtotal'] for item in self.carrinho)
        
        # Criar modal - tamanho mais compacto
        modal = tk.Toplevel(self.parent)
        modal.title("Finalizar Venda")
        modal.geometry("420x520")
        modal.transient(self.parent)
        modal.grab_set()
        modal.resizable(False, False)
        
        # Centralizar
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (modal.winfo_width() // 2)
        y = (modal.winfo_screenheight() // 2) - (modal.winfo_height() // 2)
        modal.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_container = tk.Frame(modal, bg="#ffffff")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Frame de conteúdo - com espaço para botões na parte inferior (90px)
        content_frame = tk.Frame(main_container, bg="#ffffff")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(12, 90))
        
        # Usar content_frame diretamente
        content_wrapper = content_frame
        
        # Título - menor
        title_label = tk.Label(content_wrapper, text="💰 Finalizar Venda",
                              font=("Segoe UI", 14, "bold"),
                              bg="#ffffff", fg="#333")
        title_label.pack(pady=(0, 12))
        
        # Subtotal - mais compacto
        subtotal_frame = tk.Frame(content_wrapper, bg="#ffffff")
        subtotal_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(subtotal_frame, text="Subtotal:", font=("Segoe UI", 10),
                bg="#ffffff", fg="#666").pack(side=tk.LEFT)
        
        subtotal_label = tk.Label(subtotal_frame, text=f"R$ {subtotal:.2f}",
                                 font=("Segoe UI", 10, "bold"),
                                 bg="#ffffff", fg="#333")
        subtotal_label.pack(side=tk.RIGHT)
        
        # Desconto - mais compacto
        desconto_frame = tk.Frame(content_wrapper, bg="#ffffff")
        desconto_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(desconto_frame, text="Desconto:", font=("Segoe UI", 10),
                bg="#ffffff", fg="#666").pack(anchor=tk.W, pady=(0, 3))
        
        desconto_input_frame = tk.Frame(desconto_frame, bg="#ffffff")
        desconto_input_frame.pack(fill=tk.X)
        
        tk.Label(desconto_input_frame, text="R$", font=("Segoe UI", 10, "bold"),
                bg="#ffffff", fg="#333").pack(side=tk.LEFT, padx=(0, 5))
        
        desconto_entry = tk.Entry(desconto_input_frame, font=("Segoe UI", 11, "bold"),
                                 width=15, relief=tk.SOLID, bd=1,
                                 highlightthickness=1,
                                 highlightbackground="#FF9800",
                                 highlightcolor="#FF9800",
                                 justify=tk.RIGHT)
        desconto_entry.pack(side=tk.LEFT, ipady=4, fill=tk.X, expand=True)
        desconto_entry.insert(0, "0,00")
        desconto_entry.focus()
        
        # Total - mais compacto
        total_frame = tk.Frame(content_wrapper, bg="#4CAF50", relief=tk.FLAT)
        total_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(total_frame, text="TOTAL A PAGAR", font=("Segoe UI", 10, "bold"),
                bg="#4CAF50", fg="white").pack(anchor=tk.W, padx=12, pady=(8, 3))
        
        total_label = tk.Label(total_frame, text=f"R$ {subtotal:.2f}",
                              font=("Segoe UI", 18, "bold"),
                              bg="#4CAF50", fg="white")
        total_label.pack(padx=12, pady=(0, 10))
        
        # Forma de Pagamento - mais compacto
        pagamento_frame = tk.LabelFrame(content_wrapper, text="💳 Forma de Pagamento",
                                       font=("Segoe UI", 10, "bold"),
                                       bg="#ffffff", fg="#333",
                                       relief=tk.FLAT, bd=1)
        pagamento_frame.pack(fill=tk.X, pady=(0, 10))
        
        pagamento_body = tk.Frame(pagamento_frame, bg="#ffffff")
        pagamento_body.pack(fill=tk.X, padx=12, pady=10)
        
        forma_pagamento_var = tk.StringVar(value="Dinheiro")
        formas = ["Dinheiro", "Cartão Débito", "Cartão Crédito", "PIX", "Vale"]
        
        forma_frame = tk.Frame(pagamento_body, bg="#ffffff")
        forma_frame.pack(fill=tk.X, pady=(0, 8))
        
        for forma in formas:
            rb = tk.Radiobutton(forma_frame, text=forma, variable=forma_pagamento_var,
                              value=forma, font=("Segoe UI", 9),
                              bg="#ffffff", fg="#333", selectcolor="#ffffff",
                              activebackground="#ffffff", activeforeground="#2196F3")
            rb.pack(side=tk.LEFT, padx=(0, 10))
        
        # Valor recebido (para dinheiro) - mais compacto
        valor_recebido_frame = tk.Frame(pagamento_body, bg="#ffffff")
        valor_recebido_frame.pack(fill=tk.X, pady=(0, 6))
        
        tk.Label(valor_recebido_frame, text="Valor Recebido:", font=("Segoe UI", 9),
                bg="#ffffff", fg="#666").pack(anchor=tk.W, pady=(0, 3))
        
        valor_input_frame = tk.Frame(valor_recebido_frame, bg="#ffffff")
        valor_input_frame.pack(fill=tk.X)
        
        tk.Label(valor_input_frame, text="R$", font=("Segoe UI", 10, "bold"),
                bg="#ffffff", fg="#333").pack(side=tk.LEFT, padx=(0, 5))
        
        valor_recebido_entry = tk.Entry(valor_input_frame, font=("Segoe UI", 11, "bold"),
                                       width=15, relief=tk.SOLID, bd=1,
                                       highlightthickness=1,
                                       highlightbackground="#2196F3",
                                       highlightcolor="#2196F3",
                                       justify=tk.RIGHT)
        valor_recebido_entry.pack(side=tk.LEFT, ipady=4, fill=tk.X, expand=True)
        valor_recebido_entry.insert(0, "0,00")
        
        # Troco - mais compacto
        troco_frame = tk.Frame(pagamento_body, bg="#4CAF50", relief=tk.FLAT)
        troco_frame.pack(fill=tk.X, pady=(0, 0))
        
        tk.Label(troco_frame, text="TROCO", font=("Segoe UI", 9, "bold"),
                bg="#4CAF50", fg="white").pack(anchor=tk.W, padx=8, pady=(6, 2))
        
        troco_label = tk.Label(troco_frame, text="R$ 0,00",
                              font=("Segoe UI", 14, "bold"),
                              bg="#4CAF50", fg="white")
        troco_label.pack(padx=8, pady=(0, 6))
        
        # Função para atualizar total e troco
        def atualizar_totais():
            try:
                desconto_str = desconto_entry.get().replace(',', '.').replace('R$', '').strip()
                desconto = float(desconto_str) if desconto_str else 0
                if desconto < 0:
                    desconto = 0
                if desconto > subtotal:
                    desconto = subtotal
                    desconto_entry.delete(0, tk.END)
                    desconto_entry.insert(0, f"{desconto:.2f}".replace('.', ','))
                
                total = subtotal - desconto
                if total < 0:
                    total = 0
                
                total_label.config(text=f"R$ {total:.2f}")
                
                # Calcular troco se for dinheiro
                forma = forma_pagamento_var.get()
                if forma == "Dinheiro":
                    # Mostrar campos de dinheiro
                    try:
                        valor_recebido_frame.pack(fill=tk.X, pady=(0, 10), in_=pagamento_body)
                    except:
                        pass
                    try:
                        troco_frame.pack(fill=tk.X, pady=(0, 0), in_=pagamento_body)
                    except:
                        pass
                    try:
                        valor_recebido_str = valor_recebido_entry.get().replace(',', '.').replace('R$', '').strip()
                        valor_recebido = float(valor_recebido_str) if valor_recebido_str else 0
                        if valor_recebido < 0:
                            valor_recebido = 0
                        troco = valor_recebido - total
                        if troco < 0:
                            troco = 0
                        troco_label.config(text=f"R$ {troco:.2f}")
                    except:
                        troco_label.config(text="R$ 0,00")
                else:
                    # Ocultar campos de dinheiro
                    try:
                        valor_recebido_frame.pack_forget()
                    except:
                        pass
                    try:
                        troco_frame.pack_forget()
                    except:
                        pass
            except:
                pass
        
        # Bind eventos
        desconto_entry.bind('<KeyRelease>', lambda e: atualizar_totais())
        desconto_entry.bind('<FocusOut>', lambda e: atualizar_totais())
        valor_recebido_entry.bind('<KeyRelease>', lambda e: atualizar_totais())
        valor_recebido_entry.bind('<FocusOut>', lambda e: atualizar_totais())
        for rb in forma_frame.winfo_children():
            if isinstance(rb, tk.Radiobutton):
                rb.config(command=atualizar_totais)
        
        # Botões - SEMPRE VISÍVEIS usando place na parte inferior
        buttons_frame = tk.Frame(modal, bg="#ffffff", relief=tk.FLAT, bd=1,
                                 highlightbackground="#e0e0e0", highlightthickness=1)
        buttons_frame.place(relx=0, rely=1, relwidth=1, anchor="sw")
        
        buttons_inner = tk.Frame(buttons_frame, bg="#ffffff")
        buttons_inner.pack(fill=tk.X, padx=15, pady=8)
        
        def confirmar_venda():
            try:
                desconto_str = desconto_entry.get().replace(',', '.').replace('R$', '').strip()
                desconto = float(desconto_str) if desconto_str else 0
                if desconto < 0:
                    desconto = 0
                if desconto > subtotal:
                    desconto = subtotal
                
                total = subtotal - desconto
                if total < 0:
                    total = 0
                
                forma_pagamento = forma_pagamento_var.get()
                
                if forma_pagamento == "Dinheiro":
                    valor_recebido_str = valor_recebido_entry.get().replace(',', '.').replace('R$', '').strip()
                    valor_recebido = float(valor_recebido_str) if valor_recebido_str else 0
                    
                    if valor_recebido < total:
                        messagebox.showerror("Erro", f"Valor recebido (R$ {valor_recebido:.2f}) é menor que o total (R$ {total:.2f})!")
                        return
                    
                    troco = valor_recebido - total
                    if troco > 0:
                        if not messagebox.askyesno("Confirmar", f"Total: R$ {total:.2f}\nRecebido: R$ {valor_recebido:.2f}\nTroco: R$ {troco:.2f}\n\nConfirmar venda?"):
                            return
                else:
                    if not messagebox.askyesno("Confirmar", f"Total: R$ {total:.2f}\nForma de Pagamento: {forma_pagamento}\n\nConfirmar venda?"):
                        return
                
                # Fechar modal e finalizar
                modal.destroy()
                self.confirmar_finalizar_venda(desconto, forma_pagamento, valor_recebido if forma_pagamento == "Dinheiro" else None)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar: {str(e)}")
        
        btn_confirmar = tk.Button(buttons_inner, text="✓ CONFIRMAR VENDA",
                                 bg="#4CAF50", fg="white",
                                 font=("Segoe UI", 11, "bold"),
                                 relief=tk.FLAT, cursor="hand2",
                                 padx=15, pady=8,
                                 activebackground="#45a049",
                                 activeforeground="white",
                                 command=confirmar_venda)
        btn_confirmar.pack(fill=tk.X, pady=(0, 6))
        
        btn_cancelar = tk.Button(buttons_inner, text="Cancelar",
                                bg="#9E9E9E", fg="white",
                                font=("Segoe UI", 10),
                                relief=tk.FLAT, cursor="hand2",
                                padx=15, pady=6,
                                activebackground="#757575",
                                activeforeground="white",
                                command=modal.destroy)
        btn_cancelar.pack(fill=tk.X)
        
        # Atualizar inicial
        atualizar_totais()
    
    def confirmar_finalizar_venda(self, desconto, forma_pagamento, valor_recebido=None):
        """Confirma e finaliza a venda"""
        if not self.carrinho:
            messagebox.showwarning("Aviso", "Adicione produtos ao carrinho!")
            return
        
            subtotal = sum(item['subtotal'] for item in self.carrinho)
        total = subtotal - desconto
        if total < 0:
            total = 0
        
        usuario_id = self.auth.get_current_user()['id']
        
        try:
            # Adicionar forma de pagamento nas observações
            observacoes = f"Forma de Pagamento: {forma_pagamento}"
            if forma_pagamento == "Dinheiro" and valor_recebido:
                troco = valor_recebido - total
                observacoes += f" | Recebido: R$ {valor_recebido:.2f} | Troco: R$ {troco:.2f}"
            
            venda_id = self.vendas.create(
                self.cliente_id,
                usuario_id,
                self.carrinho,
                desconto=desconto,
                observacoes=observacoes
            )
            
            messagebox.showinfo("Sucesso", f"Venda finalizada com sucesso!\nNúmero: {venda_id}\nForma: {forma_pagamento}")
            
            # Limpar carrinho
            self.carrinho = []
            self.cliente_id = None
            self.cliente_label.config(text="Nenhum cliente selecionado")
            self.produto_selecionado = None
            self.foto_produto_label.config(image='', text="📷\nSelecione um produto",
                                          bg="#f0f0f0", fg="#999")
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
        if hasattr(self.parent, 'main_window'):
            self.parent.main_window.show_dashboard()
