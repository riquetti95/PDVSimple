"""
Estilos modernos compartilhados para as telas
"""
import tkinter as tk

class ModernStyles:
    """Classe com estilos modernos para reutilização"""
    
    # Cores
    BG_COLOR = "#f5f5f5"
    CARD_BG = "#ffffff"
    ENTRY_BG = "#fafafa"
    BORDER_COLOR = "#e0e0e0"
    PRIMARY_COLOR = "#2196F3"
    PRIMARY_DARK = "#1976D2"
    SUCCESS_COLOR = "#4CAF50"
    SUCCESS_DARK = "#45a049"
    DANGER_COLOR = "#f44336"
    WARNING_COLOR = "#FF9800"
    INFO_COLOR = "#2196F3"
    TEXT_COLOR = "#333333"
    TEXT_SECONDARY = "#757575"
    TEXT_LIGHT = "#9E9E9E"
    
    # Fontes
    FONT_FAMILY = "Segoe UI"
    FONT_TITLE = (FONT_FAMILY, 18, "bold")
    FONT_SUBTITLE = (FONT_FAMILY, 11)
    FONT_LABEL = (FONT_FAMILY, 10, "bold")
    FONT_BODY = (FONT_FAMILY, 10)
    FONT_BUTTON = (FONT_FAMILY, 10, "bold")
    FONT_SMALL = (FONT_FAMILY, 9)
    
    @staticmethod
    def get_entry_style():
        """Retorna estilo padrão para Entry"""
        return {
            'font': ModernStyles.FONT_BODY,
            'relief': tk.FLAT,
            'bd': 1,
            'highlightthickness': 1,
            'highlightbackground': ModernStyles.BORDER_COLOR,
            'highlightcolor': ModernStyles.PRIMARY_COLOR,
            'bg': ModernStyles.ENTRY_BG,
            'fg': ModernStyles.TEXT_COLOR,
            'insertbackground': ModernStyles.PRIMARY_COLOR
        }
    
    @staticmethod
    def get_button_style(color='primary', size='normal'):
        """Retorna estilo padrão para Button"""
        colors = {
            'primary': (ModernStyles.PRIMARY_COLOR, ModernStyles.PRIMARY_DARK),
            'success': (ModernStyles.SUCCESS_COLOR, ModernStyles.SUCCESS_DARK),
            'danger': (ModernStyles.DANGER_COLOR, "#d32f2f"),
            'warning': (ModernStyles.WARNING_COLOR, "#F57C00")
        }
        
        bg, active_bg = colors.get(color, colors['primary'])
        padding = {'normal': (20, 12), 'small': (15, 8), 'large': (30, 15)}[size]
        
        return {
            'font': ModernStyles.FONT_BUTTON,
            'relief': tk.FLAT,
            'bd': 0,
            'cursor': "hand2",
            'bg': bg,
            'fg': "white",
            'activebackground': active_bg,
            'activeforeground': "white",
            'padx': padding[0],
            'pady': padding[1]
        }

