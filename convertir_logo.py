#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convertidor de Logo - Convierte la imagen del cocodrilo a PNG
"""

import os
import sys

try:
    from PIL import Image
except ImportError:
    print("\n[ERROR] Pillow no está instalado")
    print("Instálala con: pip install Pillow")
    sys.exit(1)


def convertir_logo():
    """Convierte una imagen al formato PNG requerido."""
    
    print("\n" + "="*80)
    print("CONVERTIDOR DE LOGO PARA GESTOR DE ALMACENES")
    print("="*80 + "\n")
    
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Buscar archivos de imagen
    extensiones = ['.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']
    archivo_imagen = None
    
    print("Buscando imágenes en la carpeta actual...")
    print()
    
    for archivo in os.listdir(ruta_actual):
        if archivo.lower().endswith(tuple(extensiones)):
            print(f"Encontrada: {archivo}")
            archivo_imagen = os.path.join(ruta_actual, archivo)
    
    if not archivo_imagen:
        print("\n[ERROR] No se encontró ninguna imagen")
        print("Coloca una imagen (jpg, png, bmp, etc.) en esta carpeta")
        print(f"Carpeta actual: {ruta_actual}")
        input("\nPresiona Enter para salir...")
        return False
    
    # Convertir imagen
    try:
        print(f"\nConvirtiendo {os.path.basename(archivo_imagen)}...")
        
        img = Image.open(archivo_imagen)
        
        # Hacer la imagen cuadrada (el logo es más ancho que alto)
        # Ajustamos a 256x256 (tamaño bueno para iconos)
        if img.width != img.height:
            print(f"  Tamaño original: {img.width}x{img.height}")
            # Crear una imagen cuadrada con fondo transparente
            size = max(img.width, img.height)
            img_cuadrada = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            offset = ((size - img.width) // 2, (size - img.height) // 2)
            img_cuadrada.paste(img, offset, img if img.mode == 'RGBA' else None)
            img = img_cuadrada
        
        # Redimensionar a tamaño estándar
        img.thumbnail((256, 256), Image.Resampling.LANCZOS)
        
        # Convertir a RGB si es necesario (para PNG)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Crear fondo blanco
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Guardar como PNG
        ruta_salida = os.path.join(ruta_actual, "logo.png")
        img.save(ruta_salida, "PNG", quality=95)
        
        print(f"\n[OK] Logo guardado como: {ruta_salida}")
        print(f"[OK] Tamaño final: {img.width}x{img.height}")
        print("\n[!] Ahora ejecuta INICIAR.bat para correr la aplicación con tu logo")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] No se pudo convertir la imagen: {e}")
        return False


if __name__ == "__main__":
    if convertir_logo():
        print("\n[OK] Conversion completada exitosamente!")
        input("\nPresiona Enter para salir...")
    else:
        input("\nPresiona Enter para salir...")
        sys.exit(1)
