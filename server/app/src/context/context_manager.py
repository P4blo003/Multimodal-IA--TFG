# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: context_manager.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases y funciones relacionadas con la gestión del contexto.    
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
import os
from pathlib import Path
from typing import Dict, Type, TypeVar
from typing import cast
# Librerías externas
from pydantic import BaseModel
# Librerías internas
from config.schema.ollama import OllamaConfig
from config.schema.uvicorn import UvicornConfig
from config.schema.prompt import PromptConfig
from config.schema.rag import RagConfig
from config.loader import load_env, load_config


# ---- PARÁMETROS ---- #
T = TypeVar("T", bound=BaseModel)
K = TypeVar("K", bound=any)


# ---- CLASES ---- #
class ContextManager:
    """
    Gestiona el contexto de la aplicación.
    """
    # -- Atributos -- #
    __config_schema:Dict[str, Type] = {
        'ollama':OllamaConfig,
        'uvicorn':UvicornConfig,
        'prompt':PromptConfig,
        'rag':RagConfig
    }
    
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la instanica.
        """
        # Inicializa las propiedades.
        self.__env:Dict[str,any] = load_env(file_path=Path('.env'))
        self.__configs:Dict[str,BaseModel] = self.__load_configs()
        self.__services:Dict[str,any] = {}
    
    # -- Métodos privados -- #
    def __load_configs(self) -> Dict[str,BaseModel]:
        """
        Carga las configuraciones.
        
        Raises:
            OSError: En caso de que ocurra algún error.
        """
        # Try-Except para manejo de errores.
        try:
            # Variable a retornar.
            configs:Dict[str, BaseModel] = {}
            # Carga las configuraciones.
            for key, schema in self.__config_schema.items():
                # Obtiene el nombre del fichero de configuración.
                file_path:Path = Path(os.path.join(self.__env['ROOT_CFG_PATH'], f"{key}.yaml"))
                # Añade la configuración.
                configs[key] = load_config(file_path=file_path, t=schema)
            
            # Retorna las configuraciones.
            return configs
        
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"ContextManager.__load_configs() -> [{type(e).__name__}] No se ha podido cargar las configuraciones. Trace: {e}")
        
    # -- Métodos públicos -- #
    def get_cfg(self, key:str, t:Type[T]) -> T:
        """
        Retorna la configuración del tipo T asociada a la clave.
        
        Args:   
            key (str): Clave de la configuración.
            t (Type[T]): Tipo de la configuración a retornar.
        Rasises:
            OSError: En caso de que haya algún error.
        Returns:
            T: Clase con la configuración.
        """
        # Try-Except para manejo de errores.
        try:
            # Obtiene la configuración asociada.
            cfg:BaseModel = self.__configs.get(key, None)
            
            # Comprueba si no se ha obtenido configuración.
            if not cfg:
                # Lanza una excepción.
                raise ValueError(f"No existe la clave {key} en las configuraciones.")
            
            # Retorna la configuración.
            return cast(T, cfg)
        
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"ContextManager.get_cfg() -> [{type(e).__name__}]No se ha podido obtener la configuración. Trace: {e}")
    
    def add_service(self, key:str, service:any):
        """
        Añade el servicio dado al diccionario.
        
        Args:
            key (str): Clave del servicio.
            service (any): Servicio a añadir.
        Raises:
            OSError: En caso de que haya algún error.
        """
        # Try-Except para manejo de errores.
        try:
            # Comprueba si hay un servicio con la misma etiqueta.
            if self.__services.get(key, None):
                raise ValueError(f"El servicio <{key}> ya esta registrado.")
            
            # Añade el servicio.
            self.__services[key] = service
        
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"ContextController.add_service() -> [{type(e).__name__}] No se pudo añadir el servicio. Trace: {e}")
    
    def get_service(self, key:str, t:Type[K]) -> K:
        """
        Retorna el servicio de tipo T asociado a la clave.
        
        Args:
            key (str): Clave del servicio.
            t (Type[K]): Tipo del servicio a retornar.
        Raises:
            OSError: En caso de que haya cualquier error.
        Returns:
            K: Servicio.
        """
        # Try-Except para manejo de excepciones.
        try:
            # Obtiene el objeto asociado.
            service = self.__services.get(key, None)
            
            # Comprueba si no se ha obtenido servicio.
            if not service:
                # Lanza una excepción.
                raise ValueError(f"No existe la clave {key} en los servicios.")

            # Retorna el servicio.
            return cast(K, service)
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"ContextManager.get_cfg() -> [{type(e).__name__}]No se ha podido obtener el servicio. Trace: {e}")