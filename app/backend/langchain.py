# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/backend/langchain.py
# Autor: Pablo González García
# Descripción: 

# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from .base import LAMBackend


# ---- CLASES ---- #
class LangChainBackend(LAMBackend):
    """
    Esta clase representa el backend de langChain. Implementa las funciones necesarias para
    hacer consultas al modelo empleando langChain.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la clase.
        """
        super().__init__()  # Constructor de LAMBackend.
        # Inicializa los parámetros.
        
        self.Logger.info("Backend iniciado. TYPE: LangChain")   # Imprime información.
        
    
    # -- Métodos públicos -- #