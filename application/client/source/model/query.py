# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/client/src/model/query.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene la clase relacionada con la query recibida por los
# endpoints.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from pydantic import BaseModel


# ---- CLASES ---- #
class QueryDTO(BaseModel):
    """
    Clase que almacena el contenido de la query que espera el servidor.
    
    Attributes:
        content (str): El contenido de la query.
    """
    # -- Atributos -- #
    content:str