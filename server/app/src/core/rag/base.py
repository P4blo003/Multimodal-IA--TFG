# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: base.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases y funciones base relaciondas con el RAG. 
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
from abc import ABC
from abc import abstractmethod
from typing import List
# Librerías externas

# Librerías internas
from model.context import ContextDTO


# ---- CLASS ---- #
class BaseRagModule(ABC):
    """
    Clase base que representa un módulo de RAG. Contiene las funciones a implementar
    por los módulos.
    """
    # -- Métodos abstractos -- #
    @abstractmethod
    def get_context(self, query:str) -> List[ContextDTO]:
        """
        @Override: Obtiene el contexto de la fuente de datos.
        
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            ContextDTO: Listado con el contexto.
        """
        pass
    