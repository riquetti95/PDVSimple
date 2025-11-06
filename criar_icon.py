"""
Script para criar ícone do SimpleVendas
Gera um arquivo icon.ico para o executável
"""
try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("Pillow não está instalado!")
    print("Instale com: pip install Pillow")
    exit(1)

def criar_icone():
    """Cria o ícone do SimpleVendas"""
    
    # Tamanhos de ícone (Windows precisa de múltiplos tamanhos)
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []
    
    for size in sizes:
        # Criar imagem com fundo azul moderno
        img = Image.new('RGBA', size, color=(33, 150, 243, 255))  # Azul primário com alpha
        draw = ImageDraw.Draw(img)
        
        width, height = size
        
        # Desenhar fundo com gradiente azul
        for i in range(height):
            # Gradiente do azul claro para escuro
            ratio = i / height
            r = int(33 + ratio * 20)
            g = int(150 + ratio * 20)
            b = int(243 - ratio * 30)
            draw.line([(0, i), (width, i)], fill=(r, g, b, 255))
        
        # Desenhar carrinho de compras estilizado
        cart_width = int(width * 0.65)
        cart_height = int(height * 0.45)
        cart_x = (width - cart_width) // 2
        cart_y = int(height * 0.28)
        
        margin = max(2, int(width * 0.04))
        
        # Corpo principal do carrinho (retângulo arredondado)
        body_top = cart_y + margin
        body_bottom = cart_y + cart_height - int(margin * 0.8)
        body_left = cart_x + margin
        body_right = cart_x + cart_width - margin
        
        # Desenhar corpo do carrinho
        draw.rectangle(
            [body_left, body_top, body_right, body_bottom],
            fill='white', outline=None
        )
        
        # Rodas do carrinho
        wheel_size = max(4, int(width * 0.13))
        wheel_y = body_bottom - int(wheel_size * 0.4)
        
        # Roda esquerda
        wheel_left_x = body_left + int(margin * 0.8)
        draw.ellipse(
            [wheel_left_x, wheel_y,
             wheel_left_x + wheel_size, wheel_y + wheel_size],
            fill='white', outline=None
        )
        
        # Roda direita
        wheel_right_x = body_right - int(margin * 0.8) - wheel_size
        draw.ellipse(
            [wheel_right_x, wheel_y,
             wheel_right_x + wheel_size, wheel_y + wheel_size],
            fill='white', outline=None
        )
        
        # Alça do carrinho (arco)
        handle_x = body_right - int(margin * 0.3)
        handle_y = body_top - int(margin * 0.6)
        handle_radius = int(width * 0.12)
        
        # Desenhar alça como arco grosso
        if width >= 32:
            draw.arc(
                [handle_x - handle_radius, handle_y,
                 handle_x, handle_y + handle_radius],
                start=180, end=0, fill='white', width=max(2, int(width * 0.04))
            )
        
        # Texto "SV" (SimpleVendas) - apenas para tamanhos maiores
        if width >= 48:
            font_size = max(8, int(width * 0.22))
            
            # Tentar diferentes fontes
            font = None
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/calibri.ttf",
                "C:/Windows/Fonts/segoeui.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc"
            ]
            
            for font_path in font_paths:
                try:
                    if os.path.exists(font_path):
                        font = ImageFont.truetype(font_path, font_size)
                        break
                except:
                    continue
            
            if font is None:
                try:
                    font = ImageFont.load_default()
                except:
                    pass
            
            if font:
                text = "SV"
                # Calcular posição centralizada
                try:
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                except:
                    # Fallback para versões antigas do PIL
                    text_width = font.getsize(text)[0]
                    text_height = font.getsize(text)[1]
                
                text_x = (width - text_width) // 2
                text_y = body_top + (body_bottom - body_top - text_height) // 2 - int(margin * 0.3)
                
                # Desenhar texto com sombra sutil
                shadow_offset = max(1, int(width * 0.01))
                draw.text((text_x + shadow_offset, text_y + shadow_offset), 
                         text, fill='#1565C0', font=font)  # Sombra azul escuro
                draw.text((text_x, text_y), text, fill='white', font=font)
        
        images.append(img)
    
    # Salvar como .ico com múltiplos tamanhos
    images[0].save(
        'icon.ico',
        format='ICO',
        sizes=[(img.width, img.height) for img in images]
    )
    
    print("✓ Ícone criado com sucesso: icon.ico")
    print(f"  Tamanhos incluídos: {', '.join([f'{s[0]}x{s[1]}' for s in sizes])}")
    return True

if __name__ == "__main__":
    try:
        criar_icone()
        print("\nAgora você pode gerar o executável com:")
        print("  build.bat (Windows)")
        print("  ou")
        print("  pyinstaller --onefile --windowed --name='SimpleVendas' --icon=icon.ico main.py")
    except Exception as e:
        print(f"Erro ao criar ícone: {str(e)}")
        print("\nTente instalar Pillow:")
        print("  pip install Pillow")

