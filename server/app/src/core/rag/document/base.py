# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: base.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases y funciones base relaciondas con el módulo de RAG
    de documentos.
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
from abc import abstractmethod
# Librerías externas

# Librerías internas
from core.rag.base import BaseRagModule


# ---- CLASS ---- #
class BaseDocumentModule(BaseRagModule):
    """
    Clase base que representa un módulo de RAG. Contiene las funciones a implementar
    por los módulos de documentos.
    """
    # -- Métodos abstractos -- #
    @abstractmethod
    def make_embeddings(self) -> None:
        """
        @Override: Calcula los embeddings de los documentos.
        
        Raises:
            OSError: En caso de que haya algún error.
        """
        pass