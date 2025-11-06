"""
Formulário de Produto
"""
import tkinter as tk
from tkinter import messagebox
from produtos import Produtos

class FormProdutoWindow:
    def __init__(self, parent, produtos, produto_id=None, callback=None):
        self.produtos = produtos
        self.produto_id = produto_id
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Produto" if produto_id else "Novo Produto")
        self.window.geometry("600x750")
        self.window.transient(parent)
        self.window.grab_set()
        self.window.resizable(False, False)
        
        self.create_widgets()
        if produto_id:
            self.load_data()
    
    def create_widgets(self):
        """Cria os widgets do formulário"""
        # Cores modernas
        bg_color = "#ffffff"
        entry_bg = "#fafafa"
        border_color = "#e0e0e0"
        primary_color = "#2196F3"
        text_color = "#333333"
        
        self.window.configure(bg="#f5f5f5")
        
        # Container principal com scroll
        canvas_frame = tk.Frame(self.window, bg="#f5f5f5")
        canvas_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        canvas = tk.Canvas(canvas_frame, bg="#f5f5f5", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame branco interno
        content_frame = tk.Frame(scrollable_frame, bg=bg_color, padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(content_frame, text="✏️ " + ("Produto" if self.produto_id else "Novo Produto"),
                              font=("Segoe UI", 18, "bold"),
                              bg=bg_color, fg=text_color)
        title_label.pack(anchor='w', pady=(0, 25))
        
        frame = tk.Frame(content_frame, bg=bg_color)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Código
        tk.Label(frame, text="Código:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.codigo_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                     relief=tk.FLAT, bd=1, highlightthickness=1,
                                     highlightbackground=border_color,
                                     highlightcolor=primary_color,
                                     bg=entry_bg, fg=text_color,
                                     insertbackground=primary_color)
        self.codigo_entry.grid(row=0, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Descrição
        tk.Label(frame, text="Descrição *", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=1, column=0, sticky='w', pady=(0, 5))
        self.descricao_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                        relief=tk.FLAT, bd=1, highlightthickness=1,
                                        highlightbackground=border_color,
                                        highlightcolor=primary_color,
                                        bg=entry_bg, fg=text_color,
                                        insertbackground=primary_color)
        self.descricao_entry.grid(row=1, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        self.descricao_entry.focus()
        
        # Categoria
        tk.Label(frame, text="Categoria:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=2, column=0, sticky='w', pady=(0, 5))
        self.categoria_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                        relief=tk.FLAT, bd=1, highlightthickness=1,
                                        highlightbackground=border_color,
                                        highlightcolor=primary_color,
                                        bg=entry_bg, fg=text_color,
                                        insertbackground=primary_color)
        self.categoria_entry.grid(row=2, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Unidade
        tk.Label(frame, text="Unidade:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=3, column=0, sticky='w', pady=(0, 5))
        self.unidade_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                     relief=tk.FLAT, bd=1, highlightthickness=1,
                                     highlightbackground=border_color,
                                     highlightcolor=primary_color,
                                     bg=entry_bg, fg=text_color,
                                     insertbackground=primary_color)
        self.unidade_entry.insert(0, "UN")
        self.unidade_entry.grid(row=3, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Preço de Venda
        tk.Label(frame, text="Preço de Venda *", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=4, column=0, sticky='w', pady=(0, 5))
        self.preco_venda_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                          relief=tk.FLAT, bd=1, highlightthickness=1,
                                          highlightbackground=border_color,
                                          highlightcolor=primary_color,
                                          bg=entry_bg, fg=text_color,
                                          insertbackground=primary_color)
        self.preco_venda_entry.grid(row=4, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Preço de Custo
        tk.Label(frame, text="Preço de Custo:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=5, column=0, sticky='w', pady=(0, 5))
        self.preco_custo_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                          relief=tk.FLAT, bd=1, highlightthickness=1,
                                          highlightbackground=border_color,
                                          highlightcolor=primary_color,
                                          bg=entry_bg, fg=text_color,
                                          insertbackground=primary_color)
        self.preco_custo_entry.grid(row=5, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Estoque Atual (apenas visualização se editando)
        if self.produto_id:
            tk.Label(frame, text="Estoque Atual:", font=("Segoe UI", 10, "bold"),
                    bg=bg_color, fg=text_color).grid(row=6, column=0, sticky='w', pady=(0, 5))
            self.estoque_label = tk.Label(frame, text="0", font=("Segoe UI", 10, "bold"),
                                         bg=bg_color, fg=text_color)
            self.estoque_label.grid(row=6, column=1, sticky='w', pady=(0, 15), padx=(10, 0))
        else:
            tk.Label(frame, text="Estoque Inicial:", font=("Segoe UI", 10, "bold"),
                    bg=bg_color, fg=text_color).grid(row=6, column=0, sticky='w', pady=(0, 5))
            self.estoque_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                         relief=tk.FLAT, bd=1, highlightthickness=1,
                                         highlightbackground=border_color,
                                         highlightcolor=primary_color,
                                         bg=entry_bg, fg=text_color,
                                         insertbackground=primary_color)
            self.estoque_entry.insert(0, "0")
            self.estoque_entry.grid(row=6, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Estoque Mínimo
        tk.Label(frame, text="Estoque Mínimo:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=7, column=0, sticky='w', pady=(0, 5))
        self.estoque_minimo_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                            relief=tk.FLAT, bd=1, highlightthickness=1,
                                            highlightbackground=border_color,
                                            highlightcolor=primary_color,
                                            bg=entry_bg, fg=text_color,
                                            insertbackground=primary_color)
        self.estoque_minimo_entry.insert(0, "0")
        self.estoque_minimo_entry.grid(row=7, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Ativo
        self.ativo_var = tk.BooleanVar(value=True)
        tk.Checkbutton(frame, text="Produto Ativo", variable=self.ativo_var,
                      font=("Segoe UI", 10), bg=bg_color, fg=text_color,
                      activebackground=bg_color, activeforeground=text_color,
                      selectcolor=bg_color).grid(row=8, column=0, columnspan=2, sticky='w', pady=(10, 0))
        
        # Botões - Frame fixo na parte inferior
        frame_buttons = tk.Frame(self.window, bg="#f5f5f5", height=80)
        frame_buttons.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)
        frame_buttons.pack_propagate(False)
        
        btn_container = tk.Frame(frame_buttons, bg="#f5f5f5")
        btn_container.pack(expand=True)
        
        btn_salvar = tk.Button(btn_container, text="✓ SALVAR", 
                              bg="#4CAF50", fg="white",
                              font=("Segoe UI", 12, "bold"), 
                              width=15,
                              padx=30, pady=12,
                              relief=tk.FLAT, cursor="hand2",
                              activebackground="#45a049",
                              activeforeground="white",
                              command=self.salvar)
        btn_salvar.pack(side=tk.LEFT, padx=(0, 15))
        
        btn_cancelar = tk.Button(btn_container, text="✕ CANCELAR", 
                                bg="#f44336", fg="white",
                                font=("Segoe UI", 12, "bold"), 
                                width=15,
                                padx=30, pady=12,
                                relief=tk.FLAT, cursor="hand2",
                                activebackground="#da190b",
                                activeforeground="white",
                                command=self.window.destroy)
        btn_cancelar.pack(side=tk.LEFT)
    
    def load_data(self):
        """Carrega dados do produto"""
        produto = self.produtos.get_by_id(self.produto_id)
        if produto:
            self.codigo_entry.insert(0, produto.get('codigo', ''))
            self.descricao_entry.insert(0, produto.get('descricao', ''))
            self.categoria_entry.insert(0, produto.get('categoria', ''))
            self.unidade_entry.delete(0, tk.END)
            self.unidade_entry.insert(0, produto.get('unidade', 'UN'))
            self.preco_venda_entry.insert(0, str(produto.get('preco_venda', 0)))
            self.preco_custo_entry.insert(0, str(produto.get('preco_custo', 0)))
            self.estoque_label.config(text=str(produto.get('estoque_atual', 0)))
            self.estoque_minimo_entry.delete(0, tk.END)
            self.estoque_minimo_entry.insert(0, str(produto.get('estoque_minimo', 0)))
            self.ativo_var.set(produto.get('ativo', 1) == 1)
    
    def salvar(self):
        """Salva o produto"""
        if not self.descricao_entry.get().strip():
            messagebox.showerror("Erro", "A descrição é obrigatória!")
            return
        
        try:
            preco_venda = float(self.preco_venda_entry.get().replace(',', '.'))
            preco_custo = float(self.preco_custo_entry.get().replace(',', '.')) if self.preco_custo_entry.get() else 0
            estoque_minimo = float(self.estoque_minimo_entry.get().replace(',', '.')) if self.estoque_minimo_entry.get() else 0
        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos!")
            return
        
        dados = {
            'codigo': self.codigo_entry.get().strip(),
            'descricao': self.descricao_entry.get().strip(),
            'categoria': self.categoria_entry.get().strip(),
            'unidade': self.unidade_entry.get().strip() or 'UN',
            'preco_venda': preco_venda,
            'preco_custo': preco_custo,
            'estoque_minimo': estoque_minimo,
            'ativo': 1 if self.ativo_var.get() else 0
        }
        
        if not self.produto_id:
            dados['estoque_atual'] = float(self.estoque_entry.get().replace(',', '.')) if self.estoque_entry.get() else 0
        
        try:
            if self.produto_id:
                self.produtos.update(self.produto_id, dados)
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            else:
                self.produtos.create(dados)
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            
            if self.callback:
                self.callback()
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar produto: {str(e)}")

