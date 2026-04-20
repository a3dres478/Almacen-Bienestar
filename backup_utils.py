import os
import shutil
from datetime import datetime
from limpiar_excel import limpiar_datos_operativos


def crear_backup_excel(ruta_excel, carpeta_destino):
    """
    Crea un backup del archivo Excel en la carpeta destino con nombre único.
    Ejemplo de nombre: Respaldo_YYYY_MM_DD_HHMMSS.xlsx
    Args:
        ruta_excel (str): Ruta absoluta al archivo Excel original.
        carpeta_destino (str): Carpeta donde guardar el backup.
    Returns:
        str: Ruta completa del backup creado, o None si falla.
    """
    try:
        if not os.path.exists(ruta_excel):
            print(f"❌ Archivo original no existe: {ruta_excel}")
            return None
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino, exist_ok=True)
        fecha = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        nombre_backup = f"Respaldo_{fecha}.xlsx"
        ruta_backup = os.path.join(carpeta_destino, nombre_backup)
        if os.path.exists(ruta_backup):
            print(f"❌ Ya existe un backup con ese nombre: {ruta_backup}")
            return None
        shutil.copy2(ruta_excel, ruta_backup)
        return ruta_backup
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return None


def verificar_backup(ruta_backup):
    """
    Verifica que el backup existe y no está vacío.
    Args:
        ruta_backup (str): Ruta al archivo de backup.
    Returns:
        bool: True si el backup es válido, False si no.
    """
    try:
        if not os.path.exists(ruta_backup):
            print(f"❌ Backup no existe: {ruta_backup}")
            return False
        if os.path.getsize(ruta_backup) == 0:
            print(f"❌ Backup está vacío: {ruta_backup}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error al verificar backup: {e}")
        return False


def reiniciar_periodo(ruta_excel, carpeta_destino):
    """
    Orquesta el flujo de reinicio de periodo:
    1. Crea backup
    2. Verifica backup
    3. Si backup es válido, limpia datos operativos
    4. Si falla backup o verificación, NO modifica el Excel original
    Args:
        ruta_excel (str): Ruta absoluta al archivo Excel original.
        carpeta_destino (str): Carpeta donde guardar el backup.
    Returns:
        bool: True si todo fue exitoso, False si hubo error.
    """
    try:
        ruta_backup = crear_backup_excel(ruta_excel, carpeta_destino)
        if not ruta_backup:
            print("❌ No se pudo crear el backup. Abortando reinicio.")
            return False
        if not verificar_backup(ruta_backup):
            print("❌ Verificación de backup fallida. Abortando reinicio.")
            return False
        # Solo limpiar si backup fue exitoso
        if limpiar_datos_operativos(ruta_excel):
            print(f"✅ Periodo reiniciado. Backup en: {ruta_backup}")
            return True
        else:
            print("❌ Error al limpiar datos operativos. El backup permanece intacto.")
            return False
    except Exception as e:
        print(f"❌ Error en reinicio de periodo: {e}")
        return False
