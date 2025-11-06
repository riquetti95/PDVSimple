"""
Tela de Configuração da Empresa
"""
import tkinter as tk
from tkinter import messagebox, filedialog
from empresa_config import EmpresaConfig

class ConfigEmpresaWindow:
    def __init__(self, root, auth):
        self.root = root
        self.auth = auth
        self.empresa = EmpresaConfig()
        
        self.window = tk.Toplevel(root)
        self.window.title("Configuração da Empresa")
        self.window.geometry("600x700")
        self.window.transient(root)
        
        self.logo_path = None
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Cria os widgets"""
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Razão Social
        tk.Label(frame, text="Razão Social *:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.razao_social_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.razao_social_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Nome Fantasia
        tk.Label(frame, text="Nome Fantasia:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.nome_fantasia_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.nome_fantasia_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # CNPJ
        tk.Label(frame, text="CNPJ:", font=("Arial", 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.cnpj_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.cnpj_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Inscrição Estadual
        tk.Label(frame, text="Inscrição Estadual:", font=("Arial", 10)).grid(row=3, column=0, sticky='w', pady=5)
        self.ie_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.ie_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Telefone
        tk.Label(frame, text="Telefone:", font=("Arial", 10)).grid(row=4, column=0, sticky='w', pady=5)
        self.telefone_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.telefone_entry.grid(row=4, column=1, pady=5, padx=5)
        
        # Email
        tk.Label(frame, text="Email:", font=("Arial", 10)).grid(row=5, column=0, sticky='w', pady=5)
        self.email_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.email_entry.grid(row=5, column=1, pady=5, padx=5)
        
        # Endereço
        tk.Label(frame, text="Endereço:", font=("Arial", 10)).grid(row=6, column=0, sticky='w', pady=5)
        self.endereco_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.endereco_entry.grid(row=6, column=1, pady=5, padx=5)
        
        # Número
        tk.Label(frame, text="Número:", font=("Arial", 10)).grid(row=7, column=0, sticky='w', pady=5)
        self.numero_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.numero_entry.grid(row=7, column=1, pady=5, padx=5)
        
        # Complemento
        tk.Label(frame, text="Complemento:", font=("Arial", 10)).grid(row=8, column=0, sticky='w', pady=5)
        self.complemento_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.complemento_entry.grid(row=8, column=1, pady=5, padx=5)
        
        # Bairro
        tk.Label(frame, text="Bairro:", font=("Arial", 10)).grid(row=9, column=0, sticky='w', pady=5)
        self.bairro_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.bairro_entry.grid(row=9, column=1, pady=5, padx=5)
        
        # Cidade
        tk.Label(frame, text="Cidade:", font=("Arial", 10)).grid(row=10, column=0, sticky='w', pady=5)
        self.cidade_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.cidade_entry.grid(row=10, column=1, pady=5, padx=5)
        
        # Estado
        tk.Label(frame, text="Estado:", font=("Arial", 10)).grid(row=11, column=0, sticky='w', pady=5)
        self.estado_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.estado_entry.grid(row=11, column=1, pady=5, padx=5)
        
        # CEP
        tk.Label(frame, text="CEP:", font=("Arial", 10)).grid(row=12, column=0, sticky='w', pady=5)
        self.cep_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        self.cep_entry.grid(row=12, column=1, pady=5, padx=5)
        
        # Logo
        tk.Label(frame, text="Logo:", font=("Arial", 10)).grid(row=13, column=0, sticky='w', pady=5)
        frame_logo = tk.Frame(frame)
        frame_logo.grid(row=13, column=1, pady=5, padx=5, sticky='w')
        
        btn_selecionar_logo = tk.Button(frame_logo, text="Selecionar Logo",
                                       command=self.selecionar_logo, cursor="hand2")
        btn_selecionar_logo.pack(side=tk.LEFT)
        
        self.logo_label = tk.Label(frame_logo, text="Nenhum logo selecionado", font=("Arial", 9), fg="gray")
        self.logo_label.pack(side=tk.LEFT, padx=10)
        
        # Botões
        frame_buttons = tk.Frame(frame)
        frame_buttons.grid(row=14, column=0, columnspan=2, pady=20)
        
        btn_salvar = tk.Button(frame_buttons, text="Salvar", bg="#4CAF50", fg="white",
                             font=("Arial", 10, "bold"), padx=20, pady=5,
                             command=self.salvar, cursor="hand2")
        btn_salvar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = tk.Button(frame_buttons, text="Cancelar", bg="#f44336", fg="white",
                                font=("Arial", 10), padx=20, pady=5,
                                command=self.window.destroy, cursor="hand2")
        btn_cancelar.pack(side=tk.LEFT, padx=5)
    
    def selecionar_logo(self):
        """Seleciona arquivo de logo"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Logo",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos", "*.*")]
        )
        if file_path:
            self.logo_path = file_path
            self.logo_label.config(text=file_path.split('/')[-1])
    
    def load_data(self):
        """Carrega dados da empresa"""
        config = self.empresa.get_config()
        if config:
            self.razao_social_entry.insert(0, config.get('razao_social', ''))
            self.nome_fantasia_entry.insert(0, config.get('nome_fantasia', ''))
            self.cnpj_entry.insert(0, config.get('cnpj', ''))
            self.ie_entry.insert(0, config.get('inscricao_estadual', ''))
            self.telefone_entry.insert(0, config.get('telefone', ''))
            self.email_entry.insert(0, config.get('email', ''))
            self.endereco_entry.insert(0, config.get('endereco', ''))
            self.numero_entry.insert(0, config.get('numero', ''))
            self.complemento_entry.insert(0, config.get('complemento', ''))
            self.bairro_entry.insert(0, config.get('bairro', ''))
            self.cidade_entry.insert(0, config.get('cidade', ''))
            self.estado_entry.insert(0, config.get('estado', ''))
            self.cep_entry.insert(0, config.get('cep', ''))
            if config.get('logo_path'):
                self.logo_label.config(text=config['logo_path'].split('/')[-1])
    
    def salvar(self):
        """Salva configuração"""
        if not self.razao_social_entry.get().strip():
            messagebox.showerror("Erro", "A razão social é obrigatória!")
            return
        
        dados = {
            'razao_social': self.razao_social_entry.get().strip(),
            'nome_fantasia': self.nome_fantasia_entry.get().strip(),
            'cnpj': self.cnpj_entry.get().strip(),
            'inscricao_estadual': self.ie_entry.get().strip(),
            'telefone': self.telefone_entry.get().strip(),
            'email': self.email_entry.get().strip(),
            'endereco': self.endereco_entry.get().strip(),
            'numero': self.numero_entry.get().strip(),
            'complemento': self.complemento_entry.get().strip(),
            'bairro': self.bairro_entry.get().strip(),
            'cidade': self.cidade_entry.get().strip(),
            'estado': self.estado_entry.get().strip(),
            'cep': self.cep_entry.get().strip()
        }
        
        try:
            self.empresa.save_config(dados, self.logo_path)
            messagebox.showinfo("Sucesso", "Configuração salva com sucesso!")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

