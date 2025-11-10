"""
Painel de Clientes - Versão para exibir dentro da janela principal
"""
import tkinter as tk
from tkinter import ttk, messagebox
from clientes import Clientes

class ClientesPanel:
    def __init__(self, parent, auth):
        self.parent = parent
        self.auth = auth
        self.clientes = Clientes()
        
        self.create_widgets()
        self.load_clientes()
    
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
        
        icon_label = tk.Label(title_container, text="👥", font=("Segoe UI", 28),
                             bg="#2196F3", fg="white")
        icon_label.pack(side=tk.LEFT, padx=(0, 12))
        
        title_label = tk.Label(title_container, text="Clientes",
                              font=("Segoe UI", 24, "bold"),
                              bg="#2196F3", fg="white")
        title_label.pack(side=tk.LEFT)
        
        # Container do conteúdo
        content_frame = tk.Frame(main_frame, bg="#f0f4f8")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Card de busca
        card_busca = tk.Frame(content_frame, bg="#ffffff", relief=tk.FLAT, bd=1,
                             highlightbackground="#e0e0e0", highlightthickness=1)
        card_busca.pack(fill=tk.X, pady=(0, 15))
        
        busca_inner = tk.Frame(card_busca, bg="#ffffff")
        busca_inner.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(busca_inner, text="🔍 Buscar:", font=("Segoe UI", 11, "bold"),
                bg="#ffffff", fg="#333").pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_cliente = tk.Entry(busca_inner, font=("Segoe UI", 11),
                                      relief=tk.FLAT, bd=1, highlightthickness=1,
                                      highlightbackground="#e0e0e0",
                                      highlightcolor="#2196F3",
                                      bg="#fafafa")
        self.search_cliente.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)
        self.search_cliente.bind('<KeyRelease>', lambda e: self.load_clientes())
        
        btn_novo_cliente = tk.Button(busca_inner, text="➕ Novo Cliente",
                                    bg="#4CAF50", fg="white",
                                    font=("Segoe UI", 11, "bold"),
                                    relief=tk.FLAT, cursor="hand2",
                                    padx=20, pady=10,
                                    activebackground="#45a049",
                                    activeforeground="white",
                                    command=self.novo_cliente)
        btn_novo_cliente.pack(side=tk.RIGHT)
        
        # Card da tabela
        card_tabela = tk.Frame(content_frame, bg="#ffffff", relief=tk.FLAT, bd=1,
                              highlightbackground="#e0e0e0", highlightthickness=1)
        card_tabela.pack(fill=tk.BOTH, expand=True)
        
        frame_tree_inner = tk.Frame(card_tabela, bg="#ffffff")
        frame_tree_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        columns = ('ID', 'Nome', 'CPF/CNPJ', 'Telefone', 'Email', 'Cidade')
        self.tree_clientes = ttk.Treeview(frame_tree_inner, columns=columns, show='headings', height=20)
        
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        
        for col in columns:
            self.tree_clientes.heading(col, text=col)
            if col == 'Nome':
                self.tree_clientes.column(col, width=250)
            else:
                self.tree_clientes.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame_tree_inner, orient=tk.VERTICAL, command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)
        
        self.tree_clientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_clientes.bind('<Double-1>', lambda e: self.editar_cliente())
    
    def load_clientes(self):
        """Carrega lista de clientes"""
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        search = self.search_cliente.get()
        clientes = self.clientes.list_all(search)
        
        for cliente in clientes:
            self.tree_clientes.insert('', tk.END, values=cliente)
    
    def novo_cliente(self):
        """Abre formulário de novo cliente"""
        from ui_form_cliente import FormClienteWindow
        root_window = self.parent.winfo_toplevel()
        FormClienteWindow(root_window, self.clientes, callback=self.load_clientes)
    
    def editar_cliente(self):
        """Edita cliente selecionado"""
        selection = self.tree_clientes.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar!")
            return
        
        item = self.tree_clientes.item(selection[0])
        cliente_id = item['values'][0]
        
        from ui_form_cliente import FormClienteWindow
        root_window = self.parent.winfo_toplevel()
        FormClienteWindow(root_window, self.clientes, cliente_id=cliente_id, callback=self.load_clientes)
    
    def voltar_dashboard(self):
        """Volta para o dashboard"""
        if hasattr(self.parent, 'main_window'):
            self.parent.main_window.show_dashboard()

