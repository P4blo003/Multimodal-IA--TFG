# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/utils/yaml.py
# Autor: Pablo González García
# Descripción: 
# Este módulo proporciona funciones de lectura de ficheros YAML.
# -----------------------------------------------------------------------------

# ---- Modulos ---- #
import os
import yaml

# ---- Funciones ---- #
def load(file:str, mode:str='r'):
    """
    Intenta abrir el arhcivo YAML y devuelve su valor o None.
    
    Args:
        file (str): Ruta del archivo a leer.
        mode (str): Modo en el que se abre el fichero. Puede ser
        solo lectura (`r`) o escritura (`w`).
        
    Raise:
        FileNotFoundError: En caso de que el fichero no exista.
    """
    # En caso de que el fichero no exista.
    if not os.path.exists(file):
        raise FileNotFoundError(f"No se encontro el fichero {file}.")
    # Abre el archivo y retorna el valor.
    with open(file=file, mode=mode) as file:
        return yaml.safe_load(file)