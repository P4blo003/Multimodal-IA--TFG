# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/server/core/model/query.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene la clase relacionada con la query recibida por los
# endpoints.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from pydantic import BaseModel


# ---- CLASES ---- #
class Query(BaseModel):
    """
    Query recibida del cliente.
    
    Attributes:
        session_id (str): ID de la sesión.
        content (str): Contenido de la query.
    """
    # -- Atributos -- #
    session_id:str
    content:str