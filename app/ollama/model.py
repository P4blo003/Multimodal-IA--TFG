# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/ollama/model.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene funciones relacionadas con los modelos de Ollama,
# como el listado o instalación.
# -----------------------------------------------------------------------------

# ---- Múdulos ---- #
import os
import subprocess

# ---- Funciones ---- #
def install_model(bin_path:str, model:str):
    """
    Instala el modelo de Ollama.
    
    Args:
        bin_path (str): Ruta al binario de Ollama.
        model (str): Nombre del modelo a instalar.
    """
    with open(os.devnull, 'w') as devnull:
        process = subprocess.run(
            [bin_path, "run", model],
            check=True,
            stdout=devnull,
            stderr=devnull
        )