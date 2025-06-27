# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: uvicorn.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases y funciones relacionadas con el servicio de Uvicorn.    
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar

# Librerías externas
import uvicorn
# Librerías internas
from config.schema.uvicorn import UvicornConfig


# ---- CLASES ---- #
class UvicornService:
    """
    Proporciona métodos del servicio de Uvicorn.
    """
    # -- Métodos por defecto -- #
    def __init__(self, uvicorn_cfg:UvicornConfig):
        """
        Inicializa la instancia.
        
        Args:
            uvicorn_cfg (UvicornConfig): Configuración de Uvicorn.
        """
        # Inicializa las propiedades.
        self.__host:str = uvicorn_cfg.host.ip
        self.__port:int = uvicorn_cfg.host.port
        self.__reload:bool = uvicorn_cfg.reload
    
    # -- Métodos públicos -- #
    def run(self) -> None:
        """
        Inicia la ejecución del servicio de Uvicorn.
        
        Raises:
            OSError: En caso de que haya algún error.
        """
        # Try-Except para manejo de excepciones.
        try:
            # Inicia el servicio de Uvicorn.
            uvicorn.run('api.main:__APP', host=self.__host, port=self.__port, reload=self.__reload)
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError()