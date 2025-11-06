"""
Formulário de Cliente
"""
import tkinter as tk
from tkinter import messagebox
from clientes import Clientes

class FormClienteWindow:
    def __init__(self, parent, clientes, cliente_id=None, callback=None):
        self.clientes = clientes
        self.cliente_id = cliente_id
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Cliente" if cliente_id else "Novo Cliente")
        self.window.geometry("600x750")
        self.window.transient(parent)
        self.window.grab_set()
        self.window.resizable(False, False)
        
        self.create_widgets()
        if cliente_id:
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
        
        # Container principal com scroll (deixando espaço para os botões)
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
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Frame branco interno
        content_frame = tk.Frame(scrollable_frame, bg=bg_color, padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(content_frame, text="✏️ " + ("Cliente" if self.cliente_id else "Novo Cliente"),
                              font=("Segoe UI", 18, "bold"),
                              bg=bg_color, fg=text_color)
        title_label.pack(anchor='w', pady=(0, 25))
        
        frame = tk.Frame(content_frame, bg=bg_color)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Nome
        tk.Label(frame, text="Nome *", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.nome_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                   relief=tk.FLAT, bd=1, highlightthickness=1,
                                   highlightbackground=border_color,
                                   highlightcolor=primary_color,
                                   bg=entry_bg, fg=text_color,
                                   insertbackground=primary_color)
        self.nome_entry.grid(row=0, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # CPF/CNPJ
        tk.Label(frame, text="CPF/CNPJ:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=1, column=0, sticky='w', pady=(0, 5))
        self.cpf_cnpj_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                      relief=tk.FLAT, bd=1, highlightthickness=1,
                                      highlightbackground=border_color,
                                      highlightcolor=primary_color,
                                      bg=entry_bg, fg=text_color,
                                      insertbackground=primary_color)
        self.cpf_cnpj_entry.grid(row=1, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Telefone
        tk.Label(frame, text="Telefone:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=2, column=0, sticky='w', pady=(0, 5))
        self.telefone_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                      relief=tk.FLAT, bd=1, highlightthickness=1,
                                      highlightbackground=border_color,
                                      highlightcolor=primary_color,
                                      bg=entry_bg, fg=text_color,
                                      insertbackground=primary_color)
        self.telefone_entry.grid(row=2, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Email
        tk.Label(frame, text="Email:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=3, column=0, sticky='w', pady=(0, 5))
        self.email_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                   relief=tk.FLAT, bd=1, highlightthickness=1,
                                   highlightbackground=border_color,
                                   highlightcolor=primary_color,
                                   bg=entry_bg, fg=text_color,
                                   insertbackground=primary_color)
        self.email_entry.grid(row=3, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Endereço
        tk.Label(frame, text="Endereço:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=4, column=0, sticky='w', pady=(0, 5))
        self.endereco_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                       relief=tk.FLAT, bd=1, highlightthickness=1,
                                       highlightbackground=border_color,
                                       highlightcolor=primary_color,
                                       bg=entry_bg, fg=text_color,
                                       insertbackground=primary_color)
        self.endereco_entry.grid(row=4, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Número
        tk.Label(frame, text="Número:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=5, column=0, sticky='w', pady=(0, 5))
        self.numero_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                    relief=tk.FLAT, bd=1, highlightthickness=1,
                                    highlightbackground=border_color,
                                    highlightcolor=primary_color,
                                    bg=entry_bg, fg=text_color,
                                    insertbackground=primary_color)
        self.numero_entry.grid(row=5, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Complemento
        tk.Label(frame, text="Complemento:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=6, column=0, sticky='w', pady=(0, 5))
        self.complemento_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                          relief=tk.FLAT, bd=1, highlightthickness=1,
                                          highlightbackground=border_color,
                                          highlightcolor=primary_color,
                                          bg=entry_bg, fg=text_color,
                                          insertbackground=primary_color)
        self.complemento_entry.grid(row=6, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Bairro
        tk.Label(frame, text="Bairro:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=7, column=0, sticky='w', pady=(0, 5))
        self.bairro_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                     relief=tk.FLAT, bd=1, highlightthickness=1,
                                     highlightbackground=border_color,
                                     highlightcolor=primary_color,
                                     bg=entry_bg, fg=text_color,
                                     insertbackground=primary_color)
        self.bairro_entry.grid(row=7, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Cidade
        tk.Label(frame, text="Cidade:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=8, column=0, sticky='w', pady=(0, 5))
        self.cidade_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                    relief=tk.FLAT, bd=1, highlightthickness=1,
                                    highlightbackground=border_color,
                                    highlightcolor=primary_color,
                                    bg=entry_bg, fg=text_color,
                                    insertbackground=primary_color)
        self.cidade_entry.grid(row=8, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Estado
        tk.Label(frame, text="Estado:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=9, column=0, sticky='w', pady=(0, 5))
        self.estado_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                     relief=tk.FLAT, bd=1, highlightthickness=1,
                                     highlightbackground=border_color,
                                     highlightcolor=primary_color,
                                     bg=entry_bg, fg=text_color,
                                     insertbackground=primary_color)
        self.estado_entry.grid(row=9, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # CEP
        tk.Label(frame, text="CEP:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=10, column=0, sticky='w', pady=(0, 5))
        self.cep_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                                  relief=tk.FLAT, bd=1, highlightthickness=1,
                                  highlightbackground=border_color,
                                  highlightcolor=primary_color,
                                  bg=entry_bg, fg=text_color,
                                  insertbackground=primary_color)
        self.cep_entry.grid(row=10, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Observações
        tk.Label(frame, text="Observações:", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=11, column=0, sticky='nw', pady=(10, 5))
        self.observacoes_text = tk.Text(frame, font=("Segoe UI", 10), width=40, height=4,
                                        relief=tk.FLAT, bd=1, highlightthickness=1,
                                        highlightbackground=border_color,
                                        highlightcolor=primary_color,
                                        bg=entry_bg, fg=text_color,
                                        wrap=tk.WORD)
        self.observacoes_text.grid(row=11, column=1, pady=(10, 5), padx=(10, 0), sticky='w')
        
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
        """Carrega dados do cliente"""
        cliente = self.clientes.get_by_id(self.cliente_id)
        if cliente:
            self.nome_entry.insert(0, cliente.get('nome', ''))
            self.cpf_cnpj_entry.insert(0, cliente.get('cpf_cnpj', ''))
            self.telefone_entry.insert(0, cliente.get('telefone', ''))
            self.email_entry.insert(0, cliente.get('email', ''))
            self.endereco_entry.insert(0, cliente.get('endereco', ''))
            self.numero_entry.insert(0, cliente.get('numero', ''))
            self.complemento_entry.insert(0, cliente.get('complemento', ''))
            self.bairro_entry.insert(0, cliente.get('bairro', ''))
            self.cidade_entry.insert(0, cliente.get('cidade', ''))
            self.estado_entry.insert(0, cliente.get('estado', ''))
            self.cep_entry.insert(0, cliente.get('cep', ''))
            self.observacoes_text.insert('1.0', cliente.get('observacoes', ''))
    
    def salvar(self):
        """Salva o cliente"""
        if not self.nome_entry.get().strip():
            messagebox.showerror("Erro", "O nome é obrigatório!")
            return
        
        dados = {
            'nome': self.nome_entry.get().strip(),
            'cpf_cnpj': self.cpf_cnpj_entry.get().strip(),
            'telefone': self.telefone_entry.get().strip(),
            'email': self.email_entry.get().strip(),
            'endereco': self.endereco_entry.get().strip(),
            'numero': self.numero_entry.get().strip(),
            'complemento': self.complemento_entry.get().strip(),
            'bairro': self.bairro_entry.get().strip(),
            'cidade': self.cidade_entry.get().strip(),
            'estado': self.estado_entry.get().strip(),
            'cep': self.cep_entry.get().strip(),
            'observacoes': self.observacoes_text.get('1.0', tk.END).strip()
        }
        
        try:
            if self.cliente_id:
                self.clientes.update(self.cliente_id, dados)
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            else:
                self.clientes.create(dados)
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            
            if self.callback:
                self.callback()
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar cliente: {str(e)}")

