"""
Painel de Usuários - Versão para exibir dentro da janela principal
"""
import tkinter as tk
from tkinter import ttk, messagebox
from auth import Auth

class UsuariosPanel:
    def __init__(self, parent, auth):
        self.parent = parent
        self.auth = auth
        
        self.create_widgets()
        self.load_usuarios()
    
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
        
        title_label = tk.Label(title_inner, text="👥 Usuários",
                              font=("Segoe UI", 20, "bold"),
                              bg="#ffffff", fg="#333")
        title_label.pack(side=tk.LEFT)
        
        # Frame de busca e botão
        frame_busca = tk.Frame(main_frame, bg="#ffffff")
        frame_busca.pack(fill=tk.X, pady=(0, 15))
        
        btn_novo = tk.Button(frame_busca, text="➕ Novo Usuário",
                            bg="#4CAF50", fg="white",
                            font=("Segoe UI", 10, "bold"),
                            relief=tk.FLAT, cursor="hand2",
                            activebackground="#45a049",
                            activeforeground="white",
                            padx=20, pady=10,
                            command=self.novo_usuario)
        btn_novo.pack(side=tk.RIGHT, padx=15, pady=15)
        
        # Treeview
        frame_tree = tk.Frame(main_frame, bg="#ffffff")
        frame_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        columns = ('ID', 'Nome', 'Usuário', 'Nível de Acesso', 'Ativo')
        self.tree = ttk.Treeview(frame_tree, columns=columns, show='headings', height=20)
        
        # Configurar colunas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Usuário', text='Usuário')
        self.tree.heading('Nível de Acesso', text='Nível de Acesso')
        self.tree.heading('Ativo', text='Ativo')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nome', width=200)
        self.tree.column('Usuário', width=150)
        self.tree.column('Nível de Acesso', width=150)
        self.tree.column('Ativo', width=80, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=15)
        
        self.tree.bind('<Double-1>', lambda e: self.editar_usuario())
    
    def load_usuarios(self):
        """Carrega usuários"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        usuarios = self.auth.list_users()
        for usuario in usuarios:
            # Converter ativo (1/0) para Sim/Não
            ativo_text = "Sim" if usuario[4] == 1 else "Não"
            self.tree.insert('', tk.END, values=(
                usuario[0], usuario[1], usuario[2], usuario[3], ativo_text
            ))
    
    def novo_usuario(self):
        """Abre formulário de novo usuário"""
        self.abrir_form_usuario()
    
    def editar_usuario(self):
        """Edita usuário selecionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar!")
            return
        
        item = self.tree.item(selection[0])
        usuario_id = item['values'][0]
        messagebox.showinfo("Info", "Edição de usuário será implementada em breve!")
        # TODO: Implementar edição de usuário
    
    def abrir_form_usuario(self):
        """Abre formulário de novo/editar usuário"""
        root_window = self.parent.winfo_toplevel()
        dialog = tk.Toplevel(root_window)
        dialog.title("Novo Usuário")
        dialog.geometry("550x500")
        dialog.transient(root_window)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Cores modernas
        bg_color = "#ffffff"
        entry_bg = "#fafafa"
        border_color = "#e0e0e0"
        primary_color = "#2196F3"
        text_color = "#333333"
        
        dialog.configure(bg="#f5f5f5")
        
        # Container principal
        main_frame = tk.Frame(dialog, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame branco interno
        content_frame = tk.Frame(main_frame, bg=bg_color, padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(content_frame, text="✏️ Novo Usuário",
                              font=("Segoe UI", 18, "bold"),
                              bg=bg_color, fg=text_color)
        title_label.pack(anchor='w', pady=(0, 25))
        
        frame = tk.Frame(content_frame, bg=bg_color)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Nome
        tk.Label(frame, text="Nome *", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=0, column=0, sticky='w', pady=(0, 5))
        nome_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                             relief=tk.FLAT, bd=1, highlightthickness=1,
                             highlightbackground=border_color,
                             highlightcolor=primary_color,
                             bg=entry_bg, fg=text_color,
                             insertbackground=primary_color)
        nome_entry.grid(row=0, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        nome_entry.focus()
        
        # Usuário
        tk.Label(frame, text="Usuário *", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=1, column=0, sticky='w', pady=(0, 5))
        usuario_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45,
                               relief=tk.FLAT, bd=1, highlightthickness=1,
                               highlightbackground=border_color,
                               highlightcolor=primary_color,
                               bg=entry_bg, fg=text_color,
                               insertbackground=primary_color)
        usuario_entry.grid(row=1, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Senha
        tk.Label(frame, text="Senha *", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=2, column=0, sticky='w', pady=(0, 5))
        senha_entry = tk.Entry(frame, font=("Segoe UI", 10), width=45, show="*",
                             relief=tk.FLAT, bd=1, highlightthickness=1,
                             highlightbackground=border_color,
                             highlightcolor=primary_color,
                             bg=entry_bg, fg=text_color,
                             insertbackground=primary_color)
        senha_entry.grid(row=2, column=1, pady=(0, 15), padx=(10, 0), ipady=8)
        
        # Nível de Acesso
        tk.Label(frame, text="Nível de Acesso *", font=("Segoe UI", 10, "bold"),
                bg=bg_color, fg=text_color).grid(row=3, column=0, sticky='w', pady=(0, 5))
        nivel_var = tk.StringVar(value="Vendedor")
        nivel_combo = ttk.Combobox(frame, textvariable=nivel_var,
                                   values=["Vendedor", "Conferente", "Gerente", "Admin"],
                                   state="readonly", width=42, font=("Segoe UI", 10))
        nivel_combo.grid(row=3, column=1, pady=(0, 15), padx=(10, 0), ipady=8, sticky='w')
        
        # Botões
        frame_buttons = tk.Frame(dialog, bg="#f5f5f5", height=80)
        frame_buttons.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)
        frame_buttons.pack_propagate(False)
        
        btn_container = tk.Frame(frame_buttons, bg="#f5f5f5")
        btn_container.pack(expand=True)
        
        def salvar():
            if not nome_entry.get().strip() or not usuario_entry.get().strip() or not senha_entry.get().strip():
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            if self.auth.create_user(nome_entry.get().strip(), usuario_entry.get().strip(),
                                    senha_entry.get().strip(), nivel_var.get()):
                messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
                self.load_usuarios()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao criar usuário! Verifique se o usuário já existe.")
        
        btn_salvar = tk.Button(btn_container, text="✓ SALVAR", 
                              bg="#4CAF50", fg="white",
                              font=("Segoe UI", 12, "bold"), 
                              width=15,
                              padx=30, pady=12,
                              relief=tk.FLAT, cursor="hand2",
                              activebackground="#45a049",
                              activeforeground="white",
                              command=salvar)
        btn_salvar.pack(side=tk.LEFT, padx=(0, 15))
        
        btn_cancelar = tk.Button(btn_container, text="✕ CANCELAR", 
                                bg="#f44336", fg="white",
                                font=("Segoe UI", 12, "bold"), 
                                width=15,
                                padx=30, pady=12,
                                relief=tk.FLAT, cursor="hand2",
                                activebackground="#da190b",
                                activeforeground="white",
                                command=dialog.destroy)
        btn_cancelar.pack(side=tk.LEFT)
        
        # Enter para salvar
        senha_entry.bind('<Return>', lambda e: salvar())
    
    def voltar_dashboard(self):
        """Volta para o dashboard"""
        if hasattr(self.parent, 'main_window'):
            self.parent.main_window.show_dashboard()

