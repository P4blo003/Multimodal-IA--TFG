# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/server/core/model/response.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene la clase relacionada con la respuesta enviada por los
# endpoints.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from pydantic import BaseModel


# ---- CLASES ---- #
class Response(BaseModel):
    """
    Respuesta a enviar al cliente.
    
    Attributes:
        session_id (str): ID de la sesión.
        statusCode (int): Estado de la respuesta.
        content (str): Contenido de la respuesta.
    """
    # -- Atributos -- #
    session_id:str
    statusCode:int = 0
    content:str