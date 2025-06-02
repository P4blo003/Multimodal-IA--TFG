
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
    __base_path:Path = Path(base_dir)
    
    # Comprueba si se deben filtrar por extensiones.
    if extensions:
        __exts = { __ext if __ext.startswith('.') else f'.{__ext}' for __ext in extensions}
        __files = [str(__p.resolve()) for __p in base_dir.rglob('*') if __p.is_file() and __p.suffix.lower() in __exts]
    else:
        __files = [str(__p.resolve()) for __p in __base_path.rglob('*') if __p.is_file()]
    
    # Devuelve la lista de ficheros.
    return __files