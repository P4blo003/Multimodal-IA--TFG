# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/server/src/main.py
# Autor: Pablo González García
# Descripción: 
# Punto de entrada del servidor FastAPI. Configura el servidor, inicia los
# servicios uxiliares como OllamController y gestiona el ciclo de vida
# del servidor.
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
