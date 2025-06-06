# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/core/hugging_face.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene la clase que proprorciona los servicios
# de HuggingFace.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
from typing import List
from contextlib import redirect_stdout, redirect_stderr
from utilities.system import create_path
from utilities.system import list_dirs
from huggingface_hub import snapshot_download


# ---- CLASES ---- #
class HuggingFaceService:
    """
    Clase encargada de gestionar los servicios de HuggingFace.
    """
    # -- Métodos estáticos -- #
    @staticmethod
    def model_installed(model_name:str, dir:str) -> bool:
        """
        Comprueba si el modelo está instalado en el sistema.
        
        Args:
            model_name (str): Nombre del modelo.
            dir (str): Directorio donde estan almacenados los modelos.
        
        Returns:
            bool: True si el modelo esta instalado y False en otro caso.
        """
        # Obtiene el directorio base.
        dir_values:List[str] = dir.split(os.path.sep)
        path_values:List[str] = model_name.split(os.path.sep)
        base_dir:List[str] = path_values[:-1]                 # Obtiene todos los elementos menos el último.
        model:str = path_values[len(path_values)-1] # Obtiene el nombre del modelo.
        
        # Obtiene el listado de carpetas.
        folders:List[str] = list_dirs(create_path(*dir_values, *base_dir))
        
        # Comprueba el número de resultados.
        if not folders or len(folders) == 0:
            return False

        # Comprueba si hay coincidencias.
        return any(os.path.basename(folder) == model for folder in folders)
    
    @staticmethod
    def install_model(model_name:str, dir:str) -> None:
        """
        Instala el modelo desde hugging face, lo almacena en el directorio pasado por
        parámetro y almacena la información en el fichero json.
        
        Args:
            model_name (str): Nombre del modelo a instalar.
            dir (str): Directorio donde estan almacenados los modelos.
        """
        # Instala el modelo y obtiene el path donde lo descargar.
        with open(os.devnull, 'w') as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                snapshot_download(repo_id=model_name, local_dir=os.path.join(dir, model_name))