# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/src/utils/system.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene funciones relacionadas con el sistema, como listado de
# ficheros.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from pathlib import Path

# ---- FUNCIONES ---- #
def list_all_files(base_dir:str, extensions:list[str] = None) -> list[str]:
    """
    Devuelve una lista con las rutas de todos los ficheros bajo `base_dir`,
    incluidos los que están en subdirectorios. Opcionalmente filtrara por
    extensiones de fichero.
    
    Args:
        base_dir (str): Ruta raíz del directorio.
        extensions (list[str]): Lista de extensiones. Si se omite o es None,
            devuelve todos los ficheros.
    
    Returns:
        list[str]: Lista de rutas de los ficheros encontrados.
    """
    # Crea el Path.
    base_path:Path = Path(base_dir)
    
    # Comprueba si se deben filtrar por extensiones.
    if extensions:
        exts = { ext if ext.startswith('.') else f'.{ext}' for ext in extensions}
        files = [str(p.resolve()) for p in base_dir.rglob('*') if p.is_file() and p.suffix.lower() in exts]
    else:
        files = [str(p.resolve()) for p in base_path.rglob('*') if p.is_file()]
    
    # Devuelve la lista de ficheros.
    return files