"""
Tela de Login
"""
import tkinter as tk
from tkinter import messagebox
from auth import Auth

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.auth = Auth()
        
        # Resetar estado da janela se estava maximizada
        try:
            self.root.state('normal')
        except:
            pass
        
        # Configurar cores modernas
        self.bg_color = "#f5f5f5"
        self.primary_color = "#2196F3"
        self.primary_dark = "#1976D2"
        self.success_color = "#4CAF50"
        self.text_color = "#333333"
        self.border_color = "#e0e0e0"
        
        self.root.title("SimpleVendas - Login")
        self.root.geometry("450x500")
        self.root.resizable(False, False)
        self.root.configure(bg=self.bg_color)
        
        # Centralizar janela
        self.center_window()
        
        # Container principal com sombra visual
        main_container = tk.Frame(root, bg="#ffffff", relief=tk.FLAT, bd=0)
        main_container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)
        
        # Frame interno
        frame = tk.Frame(main_container, bg="#ffffff", padx=40, pady=40)
        frame.pack(expand=True, fill='both')
        
        # Título com estilo moderno
        title_frame = tk.Frame(frame, bg="#ffffff")
        title_frame.pack(pady=(0, 40))
        
        title_label = tk.Label(title_frame, text="SimpleVendas", 
                              font=("Segoe UI", 28, "bold"),
                              bg="#ffffff", fg=self.primary_color)
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Sistema de Vendas", 
                                 font=("Segoe UI", 11),
                                 bg="#ffffff", fg="#757575")
        subtitle_label.pack(pady=(5, 0))
        
        # Frame de formulário
        form_frame = tk.Frame(frame, bg="#ffffff")
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Usuário
        user_label = tk.Label(form_frame, text="Usuário", 
                             font=("Segoe UI", 10, "bold"),
                             bg="#ffffff", fg=self.text_color, anchor='w')
        user_label.pack(fill=tk.X, pady=(0, 8))
        
        self.usuario_entry = tk.Entry(form_frame, font=("Segoe UI", 11),
                                     relief=tk.FLAT, bd=1, highlightthickness=1,
                                     highlightbackground=self.border_color,
                                     highlightcolor=self.primary_color,
                                     bg="#fafafa", fg=self.text_color,
                                     insertbackground=self.primary_color)
        self.usuario_entry.pack(fill=tk.X, ipady=10, pady=(0, 20))
        self.usuario_entry.focus()
        self.usuario_entry.bind('<Return>', lambda e: self.senha_entry.focus())
        self.usuario_entry.bind('<FocusIn>', lambda e: self.usuario_entry.config(highlightbackground=self.primary_color))
        self.usuario_entry.bind('<FocusOut>', lambda e: self.usuario_entry.config(highlightbackground=self.border_color))
        
        # Senha
        pass_label = tk.Label(form_frame, text="Senha",
                             font=("Segoe UI", 10, "bold"),
                             bg="#ffffff", fg=self.text_color, anchor='w')
        pass_label.pack(fill=tk.X, pady=(0, 8))
        
        self.senha_entry = tk.Entry(form_frame, font=("Segoe UI", 11),
                                    show="*", relief=tk.FLAT, bd=1, highlightthickness=1,
                                    highlightbackground=self.border_color,
                                    highlightcolor=self.primary_color,
                                    bg="#fafafa", fg=self.text_color,
                                    insertbackground=self.primary_color)
        self.senha_entry.pack(fill=tk.X, ipady=10, pady=(0, 30))
        self.senha_entry.bind('<Return>', lambda e: self.login())
        self.senha_entry.bind('<FocusIn>', lambda e: self.senha_entry.config(highlightbackground=self.primary_color))
        self.senha_entry.bind('<FocusOut>', lambda e: self.senha_entry.config(highlightbackground=self.border_color))
        
        # Botão Login moderno
        btn_login = tk.Button(form_frame, text="ENTRAR", 
                             font=("Segoe UI", 11, "bold"),
                             bg=self.primary_color, fg="white",
                             activebackground=self.primary_dark,
                             activeforeground="white",
                             relief=tk.FLAT, bd=0,
                             padx=0, pady=0, cursor="hand2",
                             command=self.login)
        btn_login.pack(fill=tk.X, ipady=12)
        
        # Efeito hover no botão
        def on_enter(e):
            btn_login.config(bg=self.primary_dark)
        def on_leave(e):
            btn_login.config(bg=self.primary_color)
        btn_login.bind("<Enter>", on_enter)
        btn_login.bind("<Leave>", on_leave)
        
        # Info padrão
        info_frame = tk.Frame(frame, bg="#ffffff")
        info_frame.pack(pady=(20, 0))
        
        info_label = tk.Label(info_frame, 
                             text="Usuário padrão: admin | Senha: admin123",
                             font=("Segoe UI", 9),
                             bg="#ffffff", fg="#9E9E9E")
        info_label.pack()
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def login(self):
        """Realiza o login"""
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get()
        
        if not usuario or not senha:
            messagebox.showerror("Erro", "Por favor, preencha usuário e senha!")
            return
        
        if self.auth.login(usuario, senha):
            # Limpar widgets da tela de login
            for widget in self.root.winfo_children():
                widget.destroy()
            self.on_success(self.auth, self.root)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")
            self.senha_entry.delete(0, tk.END)

