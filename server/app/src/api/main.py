# -*- coding: utf-8 -*-

"""*******************************************************************************************
    Nombre del Módulo: main.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene las referencias de los endpoints. Es necesario para que
    uvicorn inicie correctamente FastAPI.
    
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENSE en la raíz del proyecto.
*******************************************************************************************"""


# ---- IMPORTS ---- #
# Librerías estándar
# Librerías externas
from fastapi import FastAPI
# Librerías internas
from .endpoints.chat import __ROUTER as chat_router


# ---- PARÁMETROS ---- #
__APP:FastAPI = FastAPI()


# ---- INICIALIZACIÓN ---- #
__APP.include_router(chat_router, prefix="/chat", tags=["chat"])      # Endpoint para el chat.