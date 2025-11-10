"""
Painel de Fechamento de Caixa - Versão para exibir dentro da janela principal
"""
import tkinter as tk
from tkinter import ttk, messagebox
from caixa import Caixa
from datetime import datetime

class CaixaPanel:
    def __init__(self, parent, auth):
        self.parent = parent
        self.auth = auth
        self.caixa = Caixa()
        
        self.create_widgets()
        self.verificar_caixa()
    
    def create_widgets(self):
        """Cria os widgets"""
        # Frame principal
        main_frame = tk.Frame(self.parent, bg="#f0f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header moderno verde
        header_frame = tk.Frame(main_frame, bg="#4CAF50", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg="#4CAF50")
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Botão voltar
        btn_voltar = tk.Button(header_content, text="← Voltar",
                              font=("Segoe UI", 11, "bold"),
                              bg="#45a049", fg="white",
                              activebackground="#3d8b40",
                              activeforeground="white",
                              relief=tk.FLAT, cursor="hand2",
                              padx=20, pady=10,
                              command=self.voltar_dashboard)
        btn_voltar.pack(side=tk.LEFT, padx=(0, 20))
        
        # Título
        title_label = tk.Label(header_content, text="💰 Fechamento de Caixa",
                              font=("Segoe UI", 24, "bold"),
                              bg="#4CAF50", fg="white")
        title_label.pack(side=tk.LEFT)
        
        # Container do conteúdo
        content_frame = tk.Frame(main_frame, bg="#f0f4f8")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame de status do caixa
        status_frame = tk.Frame(content_frame, bg="#ffffff", relief=tk.FLAT, bd=1,
                                highlightbackground="#e0e0e0", highlightthickness=1)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        status_header = tk.Frame(status_frame, bg="#f5f5f5", height=50)
        status_header.pack(fill=tk.X)
        status_header.pack_propagate(False)
        
        tk.Label(status_header, text="Status do Caixa", font=("Segoe UI", 14, "bold"),
                bg="#f5f5f5", fg="#333").pack(side=tk.LEFT, padx=20, pady=15)
        
        status_body = tk.Frame(status_frame, bg="#ffffff")
        status_body.pack(fill=tk.X, padx=20, pady=20)
        
        self.status_label = tk.Label(status_body, text="Verificando...",
                                    font=("Segoe UI", 12),
                                    bg="#ffffff", fg="#666")
        self.status_label.pack(side=tk.LEFT)
        
        self.btn_acao_caixa = tk.Button(status_body, text="Abrir Caixa",
                                        font=("Segoe UI", 11, "bold"),
                                        bg="#4CAF50", fg="white",
                                        activebackground="#45a049",
                                        activeforeground="white",
                                        relief=tk.FLAT, cursor="hand2",
                                        padx=20, pady=10,
                                        command=self.abrir_caixa)
        self.btn_acao_caixa.pack(side=tk.RIGHT)
        
        # Frame de informações do caixa
        self.info_frame = tk.Frame(content_frame, bg="#ffffff", relief=tk.FLAT, bd=1,
                                  highlightbackground="#e0e0e0", highlightthickness=1)
        self.info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_header = tk.Frame(self.info_frame, bg="#f5f5f5", height=50)
        info_header.pack(fill=tk.X)
        info_header.pack_propagate(False)
        
        tk.Label(info_header, text="Informações do Caixa", font=("Segoe UI", 14, "bold"),
                bg="#f5f5f5", fg="#333").pack(side=tk.LEFT, padx=20, pady=15)
        
        self.info_body = tk.Frame(self.info_frame, bg="#ffffff")
        self.info_body.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Criar labels de informações
        self.info_labels = {}
        self.criar_info_labels()
    
    def criar_info_labels(self):
        """Cria os labels de informações"""
        # Limpar labels existentes
        for widget in self.info_body.winfo_children():
            widget.destroy()
        
        info_items = [
            ("Data/Hora Abertura:", "data_abertura"),
            ("Usuário:", "usuario_nome"),
            ("Valor Inicial:", "valor_inicial"),
            ("Total de Vendas:", "total_vendas"),
            ("Total Cancelamentos:", "total_cancelamentos"),
            ("Total Descontos:", "total_descontos"),
            ("Valor Esperado:", "valor_esperado"),
            ("Valor Final:", "valor_final")
        ]
        
        for i, (label_text, key) in enumerate(info_items):
            row = i // 2
            col = (i % 2) * 2
            
            # Label do campo
            label = tk.Label(self.info_body, text=label_text,
                           font=("Segoe UI", 11),
                           bg="#ffffff", fg="#666")
            label.grid(row=row, column=col, sticky='w', padx=(0, 10), pady=10)
            
            # Label do valor
            value_label = tk.Label(self.info_body, text="-",
                                  font=("Segoe UI", 11, "bold"),
                                  bg="#ffffff", fg="#333")
            value_label.grid(row=row, column=col+1, sticky='w', padx=(0, 30), pady=10)
            
            self.info_labels[key] = value_label
        
        # Frame de fechamento
        self.fechamento_frame = tk.Frame(self.info_body, bg="#ffffff")
        self.fechamento_frame.grid(row=4, column=0, columnspan=4, sticky='ew', pady=20)
        
        tk.Label(self.fechamento_frame, text="Valor Final (Dinheiro no Caixa):",
                font=("Segoe UI", 11, "bold"),
                bg="#ffffff", fg="#333").pack(side=tk.LEFT, padx=(0, 10))
        
        self.valor_final_entry = tk.Entry(self.fechamento_frame,
                                          font=("Segoe UI", 12),
                                          width=15)
        self.valor_final_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_fechar = tk.Button(self.fechamento_frame, text="Fechar Caixa",
                                   font=("Segoe UI", 11, "bold"),
                                   bg="#f44336", fg="white",
                                   activebackground="#d32f2f",
                                   activeforeground="white",
                                   relief=tk.FLAT, cursor="hand2",
                                   padx=20, pady=10,
                                   command=self.fechar_caixa)
        self.btn_fechar.pack(side=tk.LEFT)
        
        self.fechamento_frame.grid_remove()  # Ocultar inicialmente
    
    def verificar_caixa(self):
        """Verifica se há caixa aberto"""
        caixa_aberto = self.caixa.get_caixa_aberto()
        
        if caixa_aberto:
            self.status_label.config(text=f"Caixa ABERTO - {caixa_aberto['data_abertura']}")
            self.btn_acao_caixa.config(text="Caixa Já Aberto", state=tk.DISABLED)
            self.carregar_info_caixa(caixa_aberto)
        else:
            self.status_label.config(text="Caixa FECHADO - Nenhum caixa aberto hoje")
            self.btn_acao_caixa.config(text="Abrir Caixa", state=tk.NORMAL)
            self.limpar_info_caixa()
    
    def abrir_caixa(self):
        """Abre o caixa"""
        # Janela para abrir caixa
        dialog = tk.Toplevel(self.parent)
        dialog.title("Abrir Caixa")
        dialog.geometry("400x250")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(dialog, bg="#ffffff", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Valor Inicial do Caixa:",
                font=("Segoe UI", 11),
                bg="#ffffff", fg="#333").pack(anchor='w', pady=(0, 5))
        
        valor_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=20)
        valor_entry.pack(fill=tk.X, pady=(0, 15))
        valor_entry.insert(0, "0,00")
        valor_entry.focus()
        
        tk.Label(main_frame, text="Observações:",
                font=("Segoe UI", 11),
                bg="#ffffff", fg="#333").pack(anchor='w', pady=(0, 5))
        
        obs_text = tk.Text(main_frame, font=("Segoe UI", 10), height=4, width=40)
        obs_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        def confirmar():
            try:
                valor_str = valor_entry.get().replace(',', '.').replace('R$', '').strip()
                valor_inicial = float(valor_str) if valor_str else 0
                observacoes = obs_text.get('1.0', tk.END).strip()
                
                usuario_id = self.auth.get_current_user()['id']
                caixa_id = self.caixa.abrir_caixa(usuario_id, valor_inicial, observacoes)
                
                if caixa_id:
                    messagebox.showinfo("Sucesso", "Caixa aberto com sucesso!")
                    dialog.destroy()
                    self.verificar_caixa()
                else:
                    messagebox.showerror("Erro", "Erro ao abrir caixa. Verifique se já existe um caixa aberto.")
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir caixa: {str(e)}")
        
        btn_frame = tk.Frame(main_frame, bg="#ffffff")
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="Cancelar", bg="#9E9E9E", fg="white",
                 font=("Segoe UI", 10), relief=tk.FLAT, cursor="hand2",
                 padx=20, pady=8, command=dialog.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(btn_frame, text="Abrir", bg="#4CAF50", fg="white",
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor="hand2",
                 padx=20, pady=8, command=confirmar).pack(side=tk.RIGHT)
    
    def carregar_info_caixa(self, caixa_data):
        """Carrega informações do caixa"""
        # Calcular resumo do dia
        resumo = self.caixa.get_resumo_dia(caixa_data['data_abertura'])
        
        # Calcular valor esperado
        valor_esperado = caixa_data['valor_inicial'] + resumo['total_vendas'] - resumo['total_cancelamentos']
        
        # Atualizar labels
        self.info_labels['data_abertura'].config(text=caixa_data['data_abertura'])
        self.info_labels['usuario_nome'].config(text=caixa_data.get('usuario_nome', '-'))
        self.info_labels['valor_inicial'].config(text=f"R$ {caixa_data['valor_inicial']:.2f}")
        self.info_labels['total_vendas'].config(text=f"R$ {resumo['total_vendas']:.2f} ({resumo['num_vendas']} vendas)")
        self.info_labels['total_cancelamentos'].config(text=f"R$ {resumo['total_cancelamentos']:.2f} ({resumo['num_cancelamentos']} cancelamentos)")
        self.info_labels['total_descontos'].config(text=f"R$ {resumo['total_descontos']:.2f}")
        self.info_labels['valor_esperado'].config(text=f"R$ {valor_esperado:.2f}")
        
        if caixa_data.get('valor_final'):
            self.info_labels['valor_final'].config(text=f"R$ {caixa_data['valor_final']:.2f}")
            self.valor_final_entry.delete(0, tk.END)
            self.valor_final_entry.insert(0, f"{caixa_data['valor_final']:.2f}")
        else:
            self.info_labels['valor_final'].config(text="-")
            self.valor_final_entry.delete(0, tk.END)
            self.valor_final_entry.insert(0, f"{valor_esperado:.2f}")
        
        # Mostrar frame de fechamento
        self.fechamento_frame.grid()
        self.btn_fechar.config(state=tk.NORMAL)
    
    def limpar_info_caixa(self):
        """Limpa informações do caixa"""
        for label in self.info_labels.values():
            label.config(text="-")
        self.valor_final_entry.delete(0, tk.END)
        self.fechamento_frame.grid_remove()
    
    def fechar_caixa(self):
        """Fecha o caixa"""
        if not messagebox.askyesno("Confirmar", "Deseja realmente fechar o caixa?"):
            return
        
        try:
            valor_str = self.valor_final_entry.get().replace(',', '.').replace('R$', '').strip()
            valor_final = float(valor_str) if valor_str else 0
            
            caixa_aberto = self.caixa.get_caixa_aberto()
            if not caixa_aberto:
                messagebox.showerror("Erro", "Nenhum caixa aberto para fechar!")
                return
            
            usuario_id = self.auth.get_current_user()['id']
            
            if self.caixa.fechar_caixa(caixa_aberto['id'], usuario_id, valor_final):
                messagebox.showinfo("Sucesso", "Caixa fechado com sucesso!")
                self.verificar_caixa()
            else:
                messagebox.showerror("Erro", "Erro ao fechar caixa!")
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fechar caixa: {str(e)}")
    
    def voltar_dashboard(self):
        """Volta para o dashboard"""
        if hasattr(self.parent, 'main_window'):
            self.parent.main_window.show_dashboard()
        else:
            # Se não tiver main_window, tentar acessar via parent
            if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'main_window'):
                self.parent.parent.main_window.show_dashboard()

