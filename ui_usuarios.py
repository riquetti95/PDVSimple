"""
Tela de Gerenciamento de Usuários
"""
import tkinter as tk
from tkinter import ttk, messagebox
from auth import Auth

class UsuariosWindow:
    def __init__(self, root, auth):
        self.root = root
        self.auth = auth
        
        self.window = tk.Toplevel(root)
        self.window.title("Usuários")
        self.window.geometry("800x500")
        
        self.create_widgets()
        self.load_usuarios()
    
    def create_widgets(self):
        """Cria os widgets"""
        # Botão novo usuário
        frame_buttons = tk.Frame(self.window)
        frame_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        btn_novo = tk.Button(frame_buttons, text="Novo Usuário", bg="#4CAF50", fg="white",
                            command=self.novo_usuario, cursor="hand2")
        btn_novo.pack(side=tk.LEFT)
        
        # Treeview
        frame_tree = tk.Frame(self.window)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nome', 'Usuário', 'Nível de Acesso', 'Ativo')
        self.tree = ttk.Treeview(frame_tree, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_usuarios(self):
        """Carrega usuários"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        usuarios = self.auth.list_users()
        for usuario in usuarios:
            self.tree.insert('', tk.END, values=usuario)
    
    def novo_usuario(self):
        """Abre formulário de novo usuário"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Novo Usuário")
        dialog.geometry("400x300")
        dialog.transient(self.window)
        dialog.grab_set()
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Nome *:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', pady=5)
        nome_entry = tk.Entry(frame, font=("Arial", 10), width=30)
        nome_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(frame, text="Usuário *:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', pady=5)
        usuario_entry = tk.Entry(frame, font=("Arial", 10), width=30)
        usuario_entry.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(frame, text="Senha *:", font=("Arial", 10)).grid(row=2, column=0, sticky='w', pady=5)
        senha_entry = tk.Entry(frame, font=("Arial", 10), width=30, show="*")
        senha_entry.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Label(frame, text="Nível de Acesso *:", font=("Arial", 10)).grid(row=3, column=0, sticky='w', pady=5)
        nivel_var = tk.StringVar(value="Vendedor")
        nivel_combo = ttk.Combobox(frame, textvariable=nivel_var,
                                   values=["Vendedor", "Conferente", "Gerente", "Admin"],
                                   state="readonly", width=27)
        nivel_combo.grid(row=3, column=1, pady=5, padx=5)
        
        def salvar():
            if not nome_entry.get() or not usuario_entry.get() or not senha_entry.get():
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            if self.auth.create_user(nome_entry.get(), usuario_entry.get(),
                                    senha_entry.get(), nivel_var.get()):
                messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
                self.load_usuarios()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao criar usuário!")
        
        btn_salvar = tk.Button(frame, text="Salvar", bg="#4CAF50", fg="white",
                              command=salvar, cursor="hand2")
        btn_salvar.grid(row=4, column=0, columnspan=2, pady=20)

