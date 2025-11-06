"""
Visualizador de Cupom
"""
import tkinter as tk
from tkinter import messagebox
from cupom import Cupom

class CupomViewWindow:
    def __init__(self, parent, cupom_texto, venda_id):
        self.parent = parent
        self.cupom = Cupom()
        self.venda_id = venda_id
        
        self.window = tk.Toplevel(parent)
        self.window.title("Cupom Não Fiscal")
        self.window.geometry("600x700")
        self.window.transient(parent)
        
        # Text widget
        frame_text = tk.Frame(self.window)
        frame_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.text_widget = tk.Text(frame_text, font=("Courier", 10), wrap=tk.WORD)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.text_widget.insert('1.0', cupom_texto)
        self.text_widget.config(state=tk.DISABLED)
        
        # Botões
        frame_buttons = tk.Frame(self.window)
        frame_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        btn_imprimir = tk.Button(frame_buttons, text="Imprimir", bg="#4CAF50", fg="white",
                                command=self.imprimir, cursor="hand2")
        btn_imprimir.pack(side=tk.LEFT, padx=5)
        
        btn_salvar = tk.Button(frame_buttons, text="Salvar Arquivo", bg="#2196F3", fg="white",
                              command=self.salvar_arquivo, cursor="hand2")
        btn_salvar.pack(side=tk.LEFT, padx=5)
        
        btn_fechar = tk.Button(frame_buttons, text="Fechar", bg="#f44336", fg="white",
                              command=self.window.destroy, cursor="hand2")
        btn_fechar.pack(side=tk.LEFT, padx=5)
    
    def imprimir(self):
        """Imprime o cupom"""
        cupom_texto = self.cupom.imprimir_cupom(self.venda_id)
        messagebox.showinfo("Impressão", "Cupom enviado para impressão!")
    
    def salvar_arquivo(self):
        """Salva cupom em arquivo"""
        if self.cupom.salvar_cupom(self.venda_id):
            messagebox.showinfo("Sucesso", "Cupom salvo com sucesso!")
        else:
            messagebox.showerror("Erro", "Erro ao salvar cupom!")

