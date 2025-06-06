# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/utilities/system.py
# Autor: Pablo González García
# Descripción:
# Módulo con clases y funciones relacionadas con el sistema.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
from subprocess import Popen
from subprocess import run
from typing import Optional, List, Dict, Union
from pathlib import Path
    
    
# ---- FUNCIONES ---- #
def create_subprocess(args:Union[List[str], str], env:Optional[Dict[str, any]]=None, file:Optional[Path]=None) -> Popen:
    """
    Crea e inicializa un subproceso a partir de los argumentos dados.
    
    Args:
        args (Union[List[str],str]): Argumentos del subproceso.
        anv (Optional[Dict[str, any]]): Variables de entorno.
        file (Optional[Path]): Ruta al archivo de salida.

    Returns:
        Popen: Subproceso creado.
    """
    # Genera el fichero de salida.
    output_stream = file.open('w', encoding='utf-8') if file else open(os.devnull, 'w', encoding='utf-8')
    
    # Try-Except para el manejo de excepciones.
    try:
        # Crea el proceso.
        process:Popen = Popen(args=args, env=env, stdout=output_stream, stderr=output_stream)

    # Funciones a ejecutar al final.
    finally:
        # Si no se va a usar el archivo fuera, lo cerramos tras lanzar el proceso.
        if not file:
            output_stream.close()
    
    # Retorna el proceso.
    return process


def create_process(args:Union[List[str], str], env:Optional[Dict[str, any]]=None, file:Optional[Path]=None) -> None:
    """
    Crea e inicializa un proceso a partir de los argumentos dados.
    
    Args:
        args (Union[List[str],str]): Argumentos del subproceso.
        anv (Optional[Dict[str, any]]): Variables de entorno.
        file (Optional[Path]): Ruta al archivo de salida.
    """
    # Genera el fichero de salida.
    output_stream = file.open('w', encoding='utf-8') if file else open(os.devnull, 'w', encoding='utf-8')
    
    # Try-Except para el manejo de excepciones.
    try:
        # Crea y ejecuta el proceso.
        run(args=args, check=True, stdout=output_stream, stderr=output_stream, env=env)

    # Funciones a ejecutar al final.
    finally:
        # Si no se va a usar el archivo fuera, lo cerramos tras lanzar el proceso.
        if not file:
            output_stream.close()


def create_path(*args) -> str:
    """
    Crea la ruta completa para los argumentos dados.
    
    Args:
        args: Argumentos a añadir a la ruta.
    
    Returns:
        str: Ruta generada.
    """
    # Retorna la ruta.
    return os.path.join(*args)


def list_dir(base_dir:str, extensions:list[str] = None, recursive:bool=False) -> List[str]:
    """
    Lista los archivos en un directorio base, opcionalmente filtrando por extensiones
    y permitiendo la búsqueda recursiva.

    Args:
        base_dir (str): Ruta del directorio base desde el cual listar archivos.
        extensions (Optional[List[str]]): Lista de extensiones (con o sin punto) para filtrar archivos.
        recursive (bool): Si True, busca archivos de forma recursiva en subdirectorios.
        
    Returns:
        List[str]: Lista de rutas absolutas de los archivos encontrados.
    """
    # Crea el Path.
    base_path = Path(base_dir)

    # Comprueba que el directorio exista.
    if not base_path.exists() or not base_path.is_dir():
        raise ValueError(f"La ruta '{base_dir}' no es un directorio válido.")
    
    # Normaliza extensiones a formato con punto, en minúsculas.
    exts = {f".{ext.lower().lstrip('.')}" for ext in extensions} if extensions else None
    
    # Elige el iterador adecuado: recursivo o no.
    paths = base_path.rglob('*') if recursive else base_path.glob('*')
    
    # Filtra archivos según extensión si aplica.
    files = [str(p.resolve()) for p in paths if p.is_file() and (exts is None or p.suffix.lower() in exts)]

    # Retorna los ficheros.
    return files

def list_dirs(base_dir:str) -> List[str]:
    """
    Lista las carpetas dentro de un directorio.
    
    Args:
        base_dir (str): Ruta del directorio base desde el cual listar las carpetas.
        
    Returns:
        List[str]: Lista con las carpetas obtenidas.
    """
    # Crea la ruta de instalación del modelo.
    path:Path = Path(base_dir)
    
    # Comprueba si existe la ruta.
    if not path.exists() or not path.is_dir():  # Si no existe o no es un directorio.
        return False
        
    # Retorna el listado.
    return [p for p in path.iterdir() if p.is_dir()]