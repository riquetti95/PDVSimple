"""
Formulário de Produto
"""
import tkinter as tk
from tkinter import messagebox, filedialog
from produtos import Produtos
import os
import shutil
from PIL import Image, ImageTk

class FormProdutoWindow:
    def __init__(self, parent, produtos, produto_id=None, callback=None):
        self.produtos = produtos
        self.produto_id = produto_id
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Produto" if produto_id else "Novo Produto")
        self.window.geometry("700x700")
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
        
        # Botões - Frame fixo na parte inferior (criar primeiro para garantir visibilidade)
        frame_buttons = tk.Frame(self.window, bg="#f5f5f5", height=70)
        frame_buttons.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        frame_buttons.pack_propagate(False)
        
        btn_container = tk.Frame(frame_buttons, bg="#f5f5f5")
        btn_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=12)
        
        btn_salvar = tk.Button(btn_container, text="✓ SALVAR", 
                              bg="#4CAF50", fg="white",
                              font=("Segoe UI", 12, "bold"), 
                              width=15,
                              padx=30, pady=10,
                              relief=tk.FLAT, cursor="hand2",
                              activebackground="#45a049",
                              activeforeground="white",
                              command=self.salvar)
        btn_salvar.pack(side=tk.LEFT, padx=(0, 15))
        
        btn_cancelar = tk.Button(btn_container, text="✕ CANCELAR", 
                                bg="#f44336", fg="white",
                                font=("Segoe UI", 12, "bold"), 
                                width=15,
                                padx=30, pady=10,
                                relief=tk.FLAT, cursor="hand2",
                                activebackground="#da190b",
                                activeforeground="white",
                                command=self.window.destroy)
        btn_cancelar.pack(side=tk.LEFT)
        
        # Container principal (sem scroll) - criar depois dos botões
        main_container = tk.Frame(self.window, bg="#f5f5f5")
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Frame branco interno
        content_frame = tk.Frame(main_container, bg=bg_color, padx=25, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Título
        title_label = tk.Label(content_frame, text="✏️ " + ("Produto" if self.produto_id else "Novo Produto"),
                              font=("Segoe UI", 16, "bold"),
                              bg=bg_color, fg=text_color)
        title_label.pack(anchor='w', pady=(0, 15))
        
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
        self.codigo_entry.grid(row=0, column=1, pady=(0, 10), padx=(10, 0), ipady=6)
        
        # Descrição
        tk.Label(frame, text="Descrição *", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=1, column=0, sticky='w', pady=(0, 5))
        self.descricao_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                        relief=tk.FLAT, bd=1, highlightthickness=1,
                                        highlightbackground=border_color,
                                        highlightcolor=primary_color,
                                        bg=entry_bg, fg=text_color,
                                        insertbackground=primary_color)
        self.descricao_entry.grid(row=1, column=1, pady=(0, 10), padx=(10, 0), ipady=6)
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
        self.categoria_entry.grid(row=2, column=1, pady=(0, 10), padx=(10, 0), ipady=6)
        
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
        self.unidade_entry.grid(row=3, column=1, pady=(0, 10), padx=(10, 0), ipady=6)
        
        # Preço de Venda
        tk.Label(frame, text="Preço de Venda *", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=4, column=0, sticky='w', pady=(0, 5))
        self.preco_venda_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                          relief=tk.FLAT, bd=1, highlightthickness=1,
                                          highlightbackground=border_color,
                                          highlightcolor=primary_color,
                                          bg=entry_bg, fg=text_color,
                                          insertbackground=primary_color)
        self.preco_venda_entry.grid(row=4, column=1, pady=(0, 10), padx=(10, 0), ipady=6)
        
        # Preço de Custo
        tk.Label(frame, text="Preço de Custo:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=5, column=0, sticky='w', pady=(0, 5))
        self.preco_custo_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                          relief=tk.FLAT, bd=1, highlightthickness=1,
                                          highlightbackground=border_color,
                                          highlightcolor=primary_color,
                                          bg=entry_bg, fg=text_color,
                                          insertbackground=primary_color)
        self.preco_custo_entry.grid(row=5, column=1, pady=(0, 10), padx=(10, 0), ipady=6)
        
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
            self.estoque_entry.grid(row=6, column=1, pady=(0, 10), padx=(10, 0), ipady=6)
        
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
        self.estoque_minimo_entry.grid(row=7, column=1, pady=(0, 8), padx=(10, 0), ipady=6)
        
        # Foto do Produto - Seção compacta (movida para row 9)
        foto_section = tk.LabelFrame(frame, text="📷 Foto da Peça",
                                    font=("Segoe UI", 10, "bold"),
                                    bg=bg_color, fg=text_color,
                                    relief=tk.FLAT, bd=1,
                                    highlightbackground="#e0e0e0",
                                    highlightthickness=1)
        foto_section.grid(row=9, column=0, columnspan=2, sticky='ew', pady=(0, 8), padx=(0, 10))
        
        foto_inner = tk.Frame(foto_section, bg=bg_color)
        foto_inner.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Área de exibição da foto (menor)
        foto_display_frame = tk.Frame(foto_inner, bg=bg_color)
        foto_display_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        # Frame com borda para a foto
        foto_border = tk.Frame(foto_display_frame, bg="#e0e0e0", relief=tk.SOLID, bd=1)
        foto_border.pack()
        
        self.foto_label = tk.Label(foto_border, text="📷\nSem foto",
                                  font=("Segoe UI", 9),
                                  bg="#f5f5f5", fg="#999",
                                  width=18, height=8,
                                  relief=tk.FLAT,
                                  justify=tk.CENTER)
        self.foto_label.pack(padx=2, pady=2)
        self.foto_path = None
        self.foto_image = None
        
        # Botões de foto (compactos)
        foto_buttons = tk.Frame(foto_inner, bg=bg_color)
        foto_buttons.pack(side=tk.LEFT, fill=tk.Y)
        
        btn_selecionar_foto = tk.Button(foto_buttons, text="📁 Selecionar",
                                       font=("Segoe UI", 9, "bold"),
                                       bg="#2196F3", fg="white",
                                       relief=tk.FLAT, cursor="hand2",
                                       padx=15, pady=8,
                                       activebackground="#1976D2",
                                       activeforeground="white",
                                       command=self.selecionar_foto)
        btn_selecionar_foto.pack(pady=(0, 8))
        
        btn_remover_foto = tk.Button(foto_buttons, text="🗑️ Remover",
                                    font=("Segoe UI", 9, "bold"),
                                    bg="#f44336", fg="white",
                                    relief=tk.FLAT, cursor="hand2",
                                    padx=15, pady=8,
                                    activebackground="#d32f2f",
                                    activeforeground="white",
                                    command=self.remover_foto)
        btn_remover_foto.pack()
        
        # Ativo - mover para antes da foto para não ficar escondido
        self.ativo_var = tk.BooleanVar(value=True)
        tk.Checkbutton(frame, text="✓ Produto Ativo", variable=self.ativo_var,
                      font=("Segoe UI", 10, "bold"), bg=bg_color, fg="#4CAF50",
                      activebackground=bg_color, activeforeground="#4CAF50",
                      selectcolor=bg_color).grid(row=8, column=0, columnspan=2, sticky='w', pady=(0, 8))
    
    def selecionar_foto(self):
        """Seleciona foto do produto"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Foto da Peça",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.gif"), ("Todos", "*.*")]
        )
        if file_path:
            self.foto_path = file_path
            self.exibir_foto(file_path)
    
    def remover_foto(self):
        """Remove a foto selecionada"""
        self.foto_path = None
        self.foto_image = None
        self.foto_label.config(image='', text="📷\nSem foto", bg="#f5f5f5", fg="#999")
    
    def exibir_foto(self, caminho):
        """Exibe a foto no label"""
        try:
            img = Image.open(caminho)
            # Redimensionar mantendo proporção
            img.thumbnail((150, 150), Image.Resampling.LANCZOS)
            self.foto_image = ImageTk.PhotoImage(img)
            self.foto_label.config(image=self.foto_image, text="", bg="#ffffff")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem: {str(e)}")
    
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
            # Carregar status ativo corretamente (1 = ativo, 0 = inativo)
            ativo_valor = produto.get('ativo', 1)
            # Garantir que seja boolean
            if isinstance(ativo_valor, int):
                self.ativo_var.set(ativo_valor == 1)
            elif isinstance(ativo_valor, bool):
                self.ativo_var.set(ativo_valor)
            else:
                self.ativo_var.set(True)  # Default para True se valor inválido
            
            # Carregar foto se existir
            foto_path = produto.get('foto_path', '')
            if foto_path and foto_path.strip():
                # Normalizar caminho (converter barras invertidas em barras normais)
                foto_path = foto_path.strip().replace('\\', os.sep).replace('/', os.sep)
                
                # Tentar diferentes caminhos possíveis
                caminhos_tentar = []
                
                # 1. Caminho como está (pode ser relativo ou absoluto)
                caminhos_tentar.append(foto_path)
                
                # 2. Normalizar e tentar caminho absoluto
                if not os.path.isabs(foto_path):
                    caminhos_tentar.append(os.path.abspath(foto_path))
                    caminhos_tentar.append(os.path.normpath(os.path.join(os.getcwd(), foto_path)))
                
                # 3. Tentar apenas o nome do arquivo em data/fotos_produtos
                nome_arquivo = os.path.basename(foto_path)
                if nome_arquivo:
                    caminhos_tentar.append(os.path.normpath(os.path.join('data', 'fotos_produtos', nome_arquivo)))
                    caminhos_tentar.append(os.path.normpath(os.path.abspath(os.path.join('data', 'fotos_produtos', nome_arquivo))))
                
                # Tentar cada caminho até encontrar um que existe
                foto_encontrada = None
                for caminho in caminhos_tentar:
                    try:
                        caminho_normalizado = os.path.normpath(caminho)
                        if os.path.exists(caminho_normalizado) and os.path.isfile(caminho_normalizado):
                            foto_encontrada = caminho_normalizado
                            break
                    except:
                        continue
                
                if foto_encontrada:
                    self.foto_path = foto_encontrada
                    self.exibir_foto(foto_encontrada)
    
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
        
        # Copiar foto para pasta de fotos se foi selecionada
        foto_salva = ''
        if self.foto_path:
            try:
                fotos_dir = os.path.join('data', 'fotos_produtos')
                if not os.path.exists(fotos_dir):
                    os.makedirs(fotos_dir)
                
                # Normalizar caminho absoluto
                foto_path_abs = os.path.normpath(os.path.abspath(self.foto_path))
                fotos_dir_abs = os.path.normpath(os.path.abspath(fotos_dir))
                
                # Se a foto já está na pasta de fotos, usar caminho relativo
                if foto_path_abs.startswith(fotos_dir_abs):
                    # Usar caminho relativo para salvar no banco (normalizado)
                    foto_salva = os.path.normpath(os.path.relpath(foto_path_abs, os.getcwd()))
                else:
                    # Gerar nome único para a foto
                    if self.produto_id:
                        nome_arquivo = f"produto_{self.produto_id}_{os.path.basename(self.foto_path)}"
                    else:
                        # Para novo produto, usar timestamp
                        import time
                        nome_arquivo = f"produto_{int(time.time())}_{os.path.basename(self.foto_path)}"
                    
                    destino = os.path.normpath(os.path.join(fotos_dir, nome_arquivo))
                    shutil.copy2(foto_path_abs, destino)
                    # Salvar caminho relativo no banco (normalizado)
                    foto_salva = os.path.normpath(os.path.relpath(os.path.abspath(destino), os.getcwd()))
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar foto: {str(e)}")
                return
        elif self.produto_id:
            # Se está editando e não selecionou nova foto, manter a existente
            produto = self.produtos.get_by_id(self.produto_id)
            if produto:
                foto_salva = produto.get('foto_path', '')
        
        dados = {
            'codigo': self.codigo_entry.get().strip(),
            'descricao': self.descricao_entry.get().strip(),
            'categoria': self.categoria_entry.get().strip(),
            'unidade': self.unidade_entry.get().strip() or 'UN',
            'preco_venda': preco_venda,
            'preco_custo': preco_custo,
            'estoque_minimo': estoque_minimo,
            'foto_path': foto_salva,
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
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar produto: {str(e)}")

