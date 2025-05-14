# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/ollama/client.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene la clase base relacionada con la estrategia del
# prompting empleada.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from abc import ABC, abstractmethod
from typing import List, Dict


# ---- CLASES ---- #
class PromptStrategy(ABC):
    """
    Interfaz para las distintass estrategias de generación de prompts.
    """
    # -- Métodos -- #
    @abstractmethod
    def build_prompt(self, user_input:str, history:List[Dict[str, str]]):
        """
        Construye el prompt final a partir del input del usuario.
        
        Args:
            user_input (str): Entrada del usuario.
            history (List[Dict[str, str]]): Historial del chat.
        """
        pass