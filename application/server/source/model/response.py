# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/model/response.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene la clase relacionada con las respuestas generadas
# por el servidor.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from pydantic import BaseModel


# ---- CLASES ---- #
class ResponseDTO(BaseModel):
    """
    Clase que almacena el contenido de la respuesta del servidor.
    
    Attributes:
        session_id (str): ID de la sesión.
        content (str): El contenido de la respuesta.
    """
    # -- Atributos -- #
    session_id:str
    content:str