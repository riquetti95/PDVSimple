"""
Tela Principal do Sistema
"""
import tkinter as tk
from tkinter import ttk, messagebox
from ui_cadastros import CadastrosWindow
from ui_vendas import VendasWindow
from ui_orcamentos import OrcamentosWindow
from ui_estoque import EstoqueWindow
from ui_config_empresa import ConfigEmpresaWindow

class MainWindow:
    def __init__(self, root, auth):
        self.root = root
        self.auth = auth
        self.current_user = auth.get_current_user()
        
        # Resetar configurações da janela
        try:
            self.root.state('normal')
        except:
            pass
        
        # Configurar cores modernas
        self.bg_color = "#f5f5f5"
        
        self.root.title("SimpleVendas - Sistema de Vendas")
        self.root.configure(bg=self.bg_color)
        self.root.resizable(True, True)
        self.root.state('zoomed')  # Maximizar
        
        # Configurar handler de fechamento para backup
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Container principal para as telas
        self.content_frame = None
        self.current_screen = None
        
        self.create_menu()
        self.create_toolbar()
        self.create_content_area()
        self.create_statusbar()
        
        # Mostrar tela inicial (dashboard ou vazio)
        self.show_dashboard()
    
    def create_menu(self):
        """Cria o menu principal"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Vendas
        menu_vendas = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Vendas", menu=menu_vendas)
        menu_vendas.add_command(label="Nova Venda", command=self.abrir_vendas)
        menu_vendas.add_command(label="Histórico de Vendas", command=self.historico_vendas)
        
        # Menu Orçamentos
        menu_orcamentos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Orçamentos", menu=menu_orcamentos)
        menu_orcamentos.add_command(label="Novo Orçamento", command=self.abrir_orcamentos)
        menu_orcamentos.add_command(label="Listar Orçamentos", command=self.listar_orcamentos)
        
        # Menu Cadastros
        menu_cadastros = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)
        menu_cadastros.add_command(label="Clientes", command=self.abrir_cadastros)
        menu_cadastros.add_command(label="Produtos", command=self.abrir_cadastros)
        
        # Menu Estoque
        menu_estoque = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Estoque", menu=menu_estoque)
        menu_estoque.add_command(label="Consultar Estoque", command=self.abrir_estoque)
        menu_estoque.add_command(label="Movimentações", command=self.movimentacoes_estoque)
        
        # Menu Configurações
        menu_config = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Configurações", menu=menu_config)
        if self.auth.has_permission('Gerente'):
            menu_config.add_command(label="Dados da Empresa", command=self.abrir_config_empresa)
        if self.auth.has_permission('Admin'):
            menu_config.add_command(label="Usuários", command=self.abrir_usuarios)
        menu_config.add_separator()
        menu_config.add_command(label="Sair", command=self.logout)
    
    def create_toolbar(self):
        """Cria a barra de ferramentas"""
        toolbar = tk.Frame(self.root, bg="#ffffff", height=70, relief=tk.FLAT, bd=0)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Container interno com padding
        toolbar_inner = tk.Frame(toolbar, bg="#ffffff")
        toolbar_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Botões principais com estilo moderno
        btn_style = {
            'font': ("Segoe UI", 10, "bold"),
            'relief': tk.FLAT,
            'bd': 0,
            'cursor': "hand2",
            'padx': 20,
            'pady': 12
        }
        
        # Botão Nova Venda com ícone
        from ui_icons import icon_manager
        carrinho_icon = icon_manager.get_carrinho_icon()
        
        if carrinho_icon:
            btn_venda = tk.Button(toolbar_inner, image=carrinho_icon,
                                 text=" Nova Venda", compound=tk.LEFT,
                                 bg="#4CAF50", fg="white",
                                 activebackground="#45a049",
                                 activeforeground="white",
                                 command=self.abrir_vendas, **btn_style)
        else:
            btn_venda = tk.Button(toolbar_inner, text="🛒 Nova Venda", 
                                 bg="#4CAF50", fg="white",
                                 activebackground="#45a049",
                                 activeforeground="white",
                                 command=self.abrir_vendas, **btn_style)
        btn_venda.pack(side=tk.LEFT, padx=(0, 8))
        
        btn_orcamento = tk.Button(toolbar_inner, text="📋 Orçamento",
                                 bg="#2196F3", fg="white",
                                 activebackground="#1976D2",
                                 activeforeground="white",
                                 command=self.abrir_orcamentos, **btn_style)
        btn_orcamento.pack(side=tk.LEFT, padx=(0, 8))
        
        btn_produtos = tk.Button(toolbar_inner, text="📦 Produtos",
                                bg="#FF9800", fg="white",
                                activebackground="#F57C00",
                                activeforeground="white",
                                command=self.abrir_cadastros, **btn_style)
        btn_produtos.pack(side=tk.LEFT, padx=(0, 8))
        
        btn_estoque = tk.Button(toolbar_inner, text="📊 Estoque",
                               bg="#9C27B0", fg="white",
                               activebackground="#7B1FA2",
                               activeforeground="white",
                               command=self.abrir_estoque, **btn_style)
        btn_estoque.pack(side=tk.LEFT, padx=(0, 8))
        
        # Botão Dashboard
        btn_dashboard = tk.Button(toolbar_inner, text="🏠 Dashboard",
                                 bg="#607D8B", fg="white",
                                 activebackground="#455A64",
                                 activeforeground="white",
                                 command=self.show_dashboard, **btn_style)
        btn_dashboard.pack(side=tk.LEFT, padx=(0, 8))
        
        # Espaço
        tk.Label(toolbar_inner, bg="#ffffff").pack(side=tk.LEFT, expand=True)
        
        # Usuário logado com estilo moderno e botão desconectar
        user_frame = tk.Frame(toolbar_inner, bg="#f5f5f5", relief=tk.FLAT, bd=0)
        user_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        user_icon = tk.Label(user_frame, text="👤", font=("Segoe UI", 12),
                            bg="#f5f5f5", fg="#666")
        user_icon.pack(side=tk.LEFT, padx=(10, 5))
        
        user_info = tk.Frame(user_frame, bg="#f5f5f5")
        user_info.pack(side=tk.LEFT, padx=(0, 10))
        
        user_name = tk.Label(user_info, text=self.current_user['nome'],
                            bg="#f5f5f5", font=("Segoe UI", 10, "bold"),
                            fg="#333")
        user_name.pack(anchor='w')
        
        user_level = tk.Label(user_info, text=self.current_user['nivel_acesso'],
                             bg="#f5f5f5", font=("Segoe UI", 8),
                             fg="#757575")
        user_level.pack(anchor='w')
        
        # Botão desconectar
        btn_logout = tk.Button(user_frame, text="🚪 Sair",
                              font=("Segoe UI", 9, "bold"),
                              bg="#f44336", fg="white",
                              activebackground="#d32f2f",
                              activeforeground="white",
                              relief=tk.FLAT, cursor="hand2",
                              padx=12, pady=6,
                              command=self.logout)
        btn_logout.pack(side=tk.LEFT, padx=(10, 10))
    
    def create_content_area(self):
        """Cria a área de conteúdo onde as telas serão exibidas"""
        self.content_frame = tk.Frame(self.root, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        # Armazenar referência da MainWindow no frame para acesso pelos painéis
        self.content_frame.main_window = self
    
    def clear_content(self):
        """Limpa o conteúdo atual"""
        if self.content_frame:
            for widget in self.content_frame.winfo_children():
                widget.destroy()
    
    def show_dashboard(self):
        """Mostra a tela inicial/dashboard"""
        self.clear_content()
        
        # Frame do dashboard
        dashboard_frame = tk.Frame(self.content_frame, bg=self.bg_color, padx=30, pady=30)
        dashboard_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título de boas-vindas
        welcome_frame = tk.Frame(dashboard_frame, bg="#ffffff", relief=tk.FLAT, bd=0)
        welcome_frame.pack(fill=tk.X, pady=(0, 20))
        
        welcome_label = tk.Label(welcome_frame, 
                                text=f"Bem-vindo, {self.current_user['nome']}!",
                                font=("Segoe UI", 24, "bold"),
                                bg="#ffffff", fg="#333")
        welcome_label.pack(anchor='w', padx=30, pady=30)
        
        # Cards de ações rápidas
        actions_frame = tk.Frame(dashboard_frame, bg=self.bg_color)
        actions_frame.pack(fill=tk.BOTH, expand=True)
        
        # Card Vendas
        self.create_dashboard_card(actions_frame, "🛒", "Nova Venda", 
                                   "Iniciar uma nova venda", "#4CAF50",
                                   self.abrir_vendas, 0, 0)
        
        # Card Orçamentos
        self.create_dashboard_card(actions_frame, "📋", "Orçamento", 
                                   "Criar novo orçamento", "#2196F3",
                                   self.abrir_orcamentos, 0, 1)
        
        # Card Produtos
        self.create_dashboard_card(actions_frame, "📦", "Produtos", 
                                   "Gerenciar produtos", "#FF9800",
                                   self.abrir_cadastros, 1, 0)
        
        # Card Estoque
        self.create_dashboard_card(actions_frame, "📊", "Estoque", 
                                   "Consultar estoque", "#9C27B0",
                                   self.abrir_estoque, 1, 1)
        
        # Botão voltar (se não estiver no dashboard)
        btn_voltar_frame = tk.Frame(dashboard_frame, bg=self.bg_color)
        btn_voltar_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Não precisa de botão voltar no dashboard
    
    def create_dashboard_card(self, parent, icon, title, subtitle, color, command, row, col):
        """Cria um card no dashboard"""
        card = tk.Frame(parent, bg="#ffffff", relief=tk.FLAT, bd=0)
        card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        card.bind("<Button-1>", lambda e: command())
        card.configure(cursor="hand2")
        
        # Ícone
        icon_label = tk.Label(card, text=icon, font=("Segoe UI", 48),
                             bg="#ffffff", fg=color)
        icon_label.pack(pady=(30, 10))
        
        # Título
        title_label = tk.Label(card, text=title, font=("Segoe UI", 16, "bold"),
                              bg="#ffffff", fg="#333")
        title_label.pack()
        
        # Subtítulo
        subtitle_label = tk.Label(card, text=subtitle, font=("Segoe UI", 10),
                                 bg="#ffffff", fg="#757575")
        subtitle_label.pack(pady=(5, 30))
        
        # Efeito hover
        def on_enter(e):
            card.config(bg="#f5f5f5")
        def on_leave(e):
            card.config(bg="#ffffff")
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        for widget in [icon_label, title_label, subtitle_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)
    
    def create_statusbar(self):
        """Cria a barra de status"""
        self.statusbar = tk.Label(self.root, text="✓ SimpleVendas - Pronto",
                                 bd=0, relief=tk.FLAT, anchor=tk.W,
                                 bg="#f5f5f5", fg="#666",
                                 font=("Segoe UI", 9),
                                 padx=15, pady=8)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def abrir_vendas(self):
        """Abre a tela de vendas dentro da janela principal"""
        from ui_vendas_panel import VendasPanel
        self.clear_content()
        self.current_screen = VendasPanel(self.content_frame, self.auth)
        self.update_status("Tela de Vendas")
    
    def abrir_orcamentos(self):
        """Abre a tela de orçamentos dentro da janela principal"""
        from ui_orcamentos_panel import OrcamentosPanel
        self.clear_content()
        self.current_screen = OrcamentosPanel(self.content_frame, self.auth)
        self.update_status("Tela de Orçamentos")
    
    def abrir_cadastros(self):
        """Abre a tela de cadastros dentro da janela principal"""
        from ui_cadastros_panel import CadastrosPanel
        self.clear_content()
        self.current_screen = CadastrosPanel(self.content_frame, self.auth)
        self.update_status("Tela de Cadastros")
    
    def abrir_estoque(self):
        """Abre a tela de estoque dentro da janela principal"""
        from ui_estoque_panel import EstoquePanel
        self.clear_content()
        self.current_screen = EstoquePanel(self.content_frame, self.auth)
        self.update_status("Tela de Estoque")
    
    def update_status(self, message):
        """Atualiza a barra de status"""
        if self.statusbar:
            self.statusbar.config(text=f"✓ {message}")
    
    def abrir_config_empresa(self):
        """Abre a tela de configuração da empresa"""
        if self.auth.has_permission('Gerente'):
            ConfigEmpresaWindow(self.root, self.auth)
        else:
            messagebox.showwarning("Acesso Negado", "Você não tem permissão para acessar esta funcionalidade!")
    
    def abrir_usuarios(self):
        """Abre a tela de usuários"""
        if self.auth.has_permission('Admin'):
            from ui_usuarios_panel import UsuariosPanel
            self.clear_content()
            self.current_screen = UsuariosPanel(self.content_frame, self.auth)
            self.update_status("Gerenciamento de Usuários")
        else:
            messagebox.showwarning("Acesso Negado", "Você não tem permissão para acessar esta funcionalidade!")
    
    def historico_vendas(self):
        """Abre histórico de vendas"""
        from ui_vendas import HistoricoVendasPanel
        self.clear_content()
        self.current_screen = HistoricoVendasPanel(self.content_frame, self.auth)
        self.update_status("Histórico de Vendas")
    
    def listar_orcamentos(self):
        """Lista orçamentos"""
        # Por enquanto usa a janela separada, pode ser convertido depois
        from ui_orcamentos import ListaOrcamentosWindow
        ListaOrcamentosWindow(self.root, self.auth)
    
    def movimentacoes_estoque(self):
        """Abre movimentações de estoque"""
        # Por enquanto usa a janela separada, pode ser convertido depois
        from ui_estoque import MovimentacoesWindow
        MovimentacoesWindow(self.root, self.auth)
    
    def on_closing(self):
        """Handler para fechamento da janela principal"""
        if messagebox.askokcancel("Sair", "Deseja realmente fechar o sistema?"):
            # Fazer backup antes de fechar
            try:
                from backup import fazer_backup_banco
                if fazer_backup_banco():
                    self.update_status("Backup criado com sucesso!")
                else:
                    self.update_status("Aviso: Não foi possível criar o backup")
            except Exception as e:
                print(f"Erro ao criar backup: {str(e)}")
            
            self.root.destroy()
    
    def logout(self):
        """Faz logout"""
        if messagebox.askyesno("Confirmar", "Deseja realmente sair do sistema?"):
            # Fazer backup antes de fazer logout
            try:
                from backup import fazer_backup_banco
                fazer_backup_banco()
            except:
                pass
            
            self.auth.logout()
            # Limpar todos os widgets
            for widget in self.root.winfo_children():
                widget.destroy()
            # Voltar para tela de login
            from ui_login import LoginWindow
            def on_login_success(auth, root):
                for widget in root.winfo_children():
                    widget.destroy()
                MainWindow(root, auth)
            LoginWindow(self.root, on_login_success)
    
    def voltar_dashboard(self):
        """Volta para o dashboard"""
        self.show_dashboard()
        self.update_status("SimpleVendas - Pronto")

