"""
Detalhes da Venda
"""
import tkinter as tk
from tkinter import ttk, messagebox
from vendas import Vendas
from cupom import Cupom

class DetalhesVendaWindow:
    def __init__(self, parent, venda, vendas_module, auth):
        self.parent = parent
        self.venda = venda
        self.vendas = vendas_module
        self.auth = auth
        self.cupom = Cupom()
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Venda #{venda['numero']}")
        self.window.geometry("800x600")
        self.window.transient(parent)
        
        self.create_widgets()
        self.load_itens()
    
    def create_widgets(self):
        """Cria os widgets"""
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Informações da venda
        info_frame = tk.LabelFrame(frame, text="Informações da Venda", font=("Arial", 10, "bold"))
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(info_frame, text=f"Número: {self.venda['numero']}", font=("Arial", 10)).pack(anchor='w', padx=10, pady=5)
        tk.Label(info_frame, text=f"Data: {self.venda['data_venda']}", font=("Arial", 10)).pack(anchor='w', padx=10, pady=5)
        tk.Label(info_frame, text=f"Cliente: {self.venda.get('cliente_nome', 'N/A')}", font=("Arial", 10)).pack(anchor='w', padx=10, pady=5)
        tk.Label(info_frame, text=f"Status: {self.venda['status']}", font=("Arial", 10)).pack(anchor='w', padx=10, pady=5)
        tk.Label(info_frame, text=f"Total: R$ {self.venda['valor_final']:.2f}", font=("Arial", 12, "bold")).pack(anchor='w', padx=10, pady=5)
        
        # Itens
        itens_frame = tk.LabelFrame(frame, text="Itens", font=("Arial", 10, "bold"))
        itens_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        columns = ('Produto', 'Quantidade', 'Preço Unit.', 'Subtotal')
        self.tree = ttk.Treeview(itens_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(itens_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Botões
        buttons_frame = tk.Frame(frame)
        buttons_frame.pack(fill=tk.X)
        
        if self.venda['status'] != 'Cancelada':
            btn_cancelar = tk.Button(buttons_frame, text="Cancelar Venda", bg="#f44336", fg="white",
                                    command=self.cancelar_venda, cursor="hand2")
            btn_cancelar.pack(side=tk.LEFT, padx=5)
        
        btn_cupom = tk.Button(buttons_frame, text="Ver Cupom", bg="#4CAF50", fg="white",
                             command=self.ver_cupom, cursor="hand2")
        btn_cupom.pack(side=tk.LEFT, padx=5)
        
        btn_fechar = tk.Button(buttons_frame, text="Fechar", bg="#9E9E9E", fg="white",
                               command=self.window.destroy, cursor="hand2")
        btn_fechar.pack(side=tk.LEFT, padx=5)
    
    def load_itens(self):
        """Carrega itens da venda"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        itens = self.vendas.get_itens(self.venda['id'])
        for item in itens:
            self.tree.insert('', tk.END, values=(
                item[5] if len(item) > 5 else item[2],  # descricao
                item[3],  # quantidade
                f"R$ {item[4]:.2f}",  # preco_unitario
                f"R$ {item[5]:.2f}"  # subtotal
            ))
    
    def cancelar_venda(self):
        """Cancela a venda"""
        if messagebox.askyesno("Confirmar", "Deseja realmente cancelar esta venda?\nO estoque será revertido."):
            usuario_id = self.auth.get_current_user()['id']
            if self.vendas.cancelar(self.venda['id'], usuario_id):
                messagebox.showinfo("Sucesso", "Venda cancelada com sucesso!")
                self.window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao cancelar venda!")
    
    def ver_cupom(self):
        """Visualiza cupom"""
        cupom_texto = self.cupom.gerar_cupom(self.venda['id'])
        if cupom_texto:
            from ui_cupom_view import CupomViewWindow
            CupomViewWindow(self.window, cupom_texto, self.venda['id'])

