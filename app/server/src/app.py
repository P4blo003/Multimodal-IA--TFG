# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/server/src/app.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene todas las dependencias de FastAPI. Necesario para
# poder iniciar uvicorn.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from fastapi import FastAPI

from api.endpoint import chat


# ---- VARIABLES GLOBALES ---- #
api:FastAPI = None


# ---- INICIALIZACIÓN ---- #
# Inicializa FastAPI.
api = FastAPI()
# Añade los endpoints.
api.include_router(chat.router, prefix="/chat", tags=["chat"])
