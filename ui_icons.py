"""
Gerenciamento de ícones do sistema
"""
import tkinter as tk
import os

class IconManager:
    """Gerencia ícones do sistema"""
    
    def __init__(self):
        self.assets_dir = "assets"
        self.icons = {}
        self.load_icons()
    
    def load_icons(self):
        """Carrega ícones disponíveis"""
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir, exist_ok=True)
            return
        
        # Tentar carregar ícone do carrinho
        carrinho_paths = [
            os.path.join(self.assets_dir, "carrinho.png"),
            os.path.join(self.assets_dir, "carrinho.ico"),
            os.path.join(self.assets_dir, "cart.png"),
        ]
        
        for path in carrinho_paths:
            if os.path.exists(path):
                try:
                    self.icons['carrinho'] = tk.PhotoImage(file=path)
                    break
                except:
                    pass
    
    def get_icon(self, icon_name):
        """Retorna um ícone se disponível, senão retorna None"""
        return self.icons.get(icon_name)
    
    def get_carrinho_icon(self):
        """Retorna o ícone do carrinho"""
        return self.get_icon('carrinho')
    
    def create_carrinho_label(self, parent, size=24):
        """Cria um label com ícone de carrinho (ou emoji se não houver ícone)"""
        icon = self.get_carrinho_icon()
        
        if icon:
            # Redimensionar se necessário
            try:
                # Tkinter PhotoImage não suporta redimensionamento direto
                # Usar o ícone original ou criar uma versão menor
                label = tk.Label(parent, image=icon, bg=parent.cget('bg') if hasattr(parent, 'cget') else 'white')
            except:
                label = tk.Label(parent, text="🛒", font=("Segoe UI", size), 
                               bg=parent.cget('bg') if hasattr(parent, 'cget') else 'white')
        else:
            # Usar emoji como fallback
            label = tk.Label(parent, text="🛒", font=("Segoe UI", size),
                           bg=parent.cget('bg') if hasattr(parent, 'cget') else 'white')
        
        return label

# Instância global
icon_manager = IconManager()

