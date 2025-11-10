"""
Painel de Produtos - Versão para exibir dentro da janela principal
"""
import tkinter as tk
from tkinter import ttk, messagebox
from produtos import Produtos

class ProdutosPanel:
    def __init__(self, parent, auth):
        self.parent = parent
        self.auth = auth
        self.produtos = Produtos()
        
        self.create_widgets()
        self.load_produtos()
    
    def create_widgets(self):
        """Cria os widgets da tela"""
        # Frame principal com mesmo estilo da venda
        main_frame = tk.Frame(self.parent, bg="#f0f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header moderno azul
        header_frame = tk.Frame(main_frame, bg="#FF9800", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg="#FF9800")
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Botão voltar no header
        btn_voltar = tk.Button(header_content, text="← Voltar",
                              font=("Segoe UI", 11, "bold"),
                              bg="#F57C00", fg="white",
                              activebackground="#E65100",
                              activeforeground="white",
                              relief=tk.FLAT, cursor="hand2",
                              padx=20, pady=10,
                              command=self.voltar_dashboard)
        btn_voltar.pack(side=tk.LEFT, padx=(0, 20))
        
        # Título com ícone
        title_container = tk.Frame(header_content, bg="#FF9800")
        title_container.pack(side=tk.LEFT)
        
        icon_label = tk.Label(title_container, text="📦", font=("Segoe UI", 28),
                             bg="#FF9800", fg="white")
        icon_label.pack(side=tk.LEFT, padx=(0, 12))
        
        title_label = tk.Label(title_container, text="Produtos",
                              font=("Segoe UI", 24, "bold"),
                              bg="#FF9800", fg="white")
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
        
        self.search_produto = tk.Entry(busca_inner, font=("Segoe UI", 11),
                                       relief=tk.FLAT, bd=1, highlightthickness=1,
                                       highlightbackground="#e0e0e0",
                                       highlightcolor="#FF9800",
                                       bg="#fafafa")
        self.search_produto.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)
        self.search_produto.bind('<KeyRelease>', lambda e: self.load_produtos())
        
        btn_novo_produto = tk.Button(busca_inner, text="➕ Novo Produto",
                                    bg="#4CAF50", fg="white",
                                    font=("Segoe UI", 11, "bold"),
                                    relief=tk.FLAT, cursor="hand2",
                                    padx=20, pady=10,
                                    activebackground="#45a049",
                                    activeforeground="white",
                                    command=self.novo_produto)
        btn_novo_produto.pack(side=tk.RIGHT)
        
        # Card da tabela
        card_tabela = tk.Frame(content_frame, bg="#ffffff", relief=tk.FLAT, bd=1,
                              highlightbackground="#e0e0e0", highlightthickness=1)
        card_tabela.pack(fill=tk.BOTH, expand=True)
        
        frame_tree_inner = tk.Frame(card_tabela, bg="#ffffff")
        frame_tree_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        columns = ('ID', 'Código', 'Descrição', 'Categoria', 'Preço', 'Estoque', 'Unidade')
        self.tree_produtos = ttk.Treeview(frame_tree_inner, columns=columns, show='headings', height=20)
        
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        
        for col in columns:
            self.tree_produtos.heading(col, text=col)
            if col == 'Descrição':
                self.tree_produtos.column(col, width=250)
            else:
                self.tree_produtos.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(frame_tree_inner, orient=tk.VERTICAL, command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_produtos.bind('<Double-1>', lambda e: self.editar_produto())
    
    def load_produtos(self):
        """Carrega lista de produtos"""
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        search = self.search_produto.get()
        # Mostrar todos os produtos (ativos e inativos) como no estoque
        produtos = self.produtos.list_all(search, apenas_ativos=False)
        
        for produto in produtos:
            self.tree_produtos.insert('', tk.END, values=(
                produto[0], produto[1], produto[2], produto[3],
                f"R$ {produto[4]:.2f}", produto[5], produto[6]
            ))
    
    def novo_produto(self):
        """Abre formulário de novo produto"""
        try:
            # Garantir que estamos usando o módulo correto
            import ui_form_produto
            FormProdutoWindow = ui_form_produto.FormProdutoWindow
            
            root_window = self.parent.winfo_toplevel()
            
            # Verificar se produtos está inicializado
            if not hasattr(self, 'produtos') or self.produtos is None:
                self.produtos = Produtos()
            
            # Criar instância do formulário de PRODUTO (não cliente!)
            form = FormProdutoWindow(root_window, self.produtos, callback=self.load_produtos)
            
            # Verificar se foi criado corretamente
            if not form or not hasattr(form, 'window'):
                raise Exception("Falha ao criar formulário de produto")
                
            # Verificar se o título da janela está correto
            if hasattr(form, 'window') and form.window:
                title = form.window.title()
                if "Cliente" in title or "cliente" in title.lower():
                    raise Exception(f"ERRO: Formulário de cliente foi aberto ao invés de produto! Título: {title}")
                    
        except ImportError as e:
            messagebox.showerror("Erro de Importação", f"Erro ao importar FormProdutoWindow: {str(e)}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir formulário de produto: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def editar_produto(self):
        """Edita produto selecionado"""
        selection = self.tree_produtos.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para editar!")
            return
        
        try:
            item = self.tree_produtos.item(selection[0])
            produto_id = item['values'][0]
            
            from ui_form_produto import FormProdutoWindow
            root_window = self.parent.winfo_toplevel()
            # Verificar se produtos está inicializado
            if not hasattr(self, 'produtos') or self.produtos is None:
                self.produtos = Produtos()
            # Criar instância do formulário de PRODUTO
            form = FormProdutoWindow(root_window, self.produtos, produto_id=produto_id, callback=self.load_produtos)
            if not form or not hasattr(form, 'window'):
                raise Exception("Falha ao criar formulário de produto")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir formulário de produto: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def voltar_dashboard(self):
        """Volta para o dashboard"""
        if hasattr(self.parent, 'main_window'):
            self.parent.main_window.show_dashboard()

