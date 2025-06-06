# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/api/main.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene todas las dependencias de FastAPI. Necesario para
# poder iniciar uvicorn.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from fastapi import FastAPI
from .endpoint.chat import router as chat_router


# ---- VARIABLES GLOBALES ---- #
app:FastAPI = FastAPI()


# ---- INICIALIZACIÓN ---- #
# Añade los endpoints.
app.include_router(chat_router, prefix="/chat", tags=["chat"])      # Endpoint para el chat.