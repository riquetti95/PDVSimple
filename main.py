"""
SimpleVendas - Sistema de Vendas
Aplicação principal
"""
import tkinter as tk
from ui_login import LoginWindow
from ui_main import MainWindow
from database import Database

def on_closing(root):
    """Handler para fechamento da aplicação"""
    from tkinter import messagebox
    from backup import fazer_backup_banco
    
    if messagebox.askokcancel("Sair", "Deseja realmente fechar o sistema?"):
        # Fazer backup antes de fechar
        try:
            if fazer_backup_banco():
                print("✓ Backup criado com sucesso!")
            else:
                print("⚠ Aviso: Não foi possível criar o backup")
        except Exception as e:
            print(f"⚠ Erro ao criar backup: {str(e)}")
        
        root.destroy()

def start_app():
    """Inicia a aplicação"""
    # Inicializar banco de dados
    db = Database()
    
    # Criar janela principal
    root = tk.Tk()
    
    # Configurar handler de fechamento
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    
    def on_login_success(auth, login_root):
        """Callback quando login é bem-sucedido"""
        # Usar a mesma janela root para a tela principal
        main_window = MainWindow(login_root, auth)
    
    # Mostrar tela de login
    login_window = LoginWindow(root, on_login_success)
    
    root.mainloop()

if __name__ == "__main__":
    start_app()

