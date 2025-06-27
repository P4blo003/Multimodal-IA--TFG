# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: ollama.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases y funciones relacionadas con el servicio de Ollama.    
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
import os
import json
from typing import List, Dict
from pathlib import Path
# Librerías externas
import requests
from requests import Response
# Librerías internas
from model.measure import OllamaModelDataDTO
from utils.file.csv import save_in_csv
from config.schema.ollama import ServiceConfig
from config.schema.common import BaseModelConfig


# ---- CLASES ---- #
class OllamaService:
    """
    Proporciona los métodos de interacciòn con la API de Ollama.
    """
    # -- Métodos por defecto -- #
    def __init__(self, service_cfg:ServiceConfig):
        """
        Inicializa la instancia.
        
        Args:
            service_cfg (ServiceConfig): Configuración del servicio.
        """
        # Inicializa las propiedades.
        self.__name:str = service_cfg.name
        self.__baseUrl:str = f"http://{service_cfg.host.ip}:{service_cfg.host.port}"
        self.__model:BaseModelConfig = service_cfg.model
        self.__measureFilePath:Path = Path(os.path.join('.server', 'etc', 'measure', f"{self.__model.tag}.csv"))
    
    # -- Propiedades -- #
    @property
    def Name(self) -> str:
        """
        Retorna el nombre del servicio.
        
        Returns:
            str: Nombre del servicio.
        """
        return self.__name
    
    @property
    def Model(self) -> BaseModelConfig:
        """
        Retorna el modelo del servicio de Ollama.
        
        Returns:
            BaseModelConfig: Etiqueta del modelo de Ollama.
        """
        # Retorna el modelo.
        return self.__model

    # -- Métodos públicos -- #
    def check_running(self) -> bool:
        """
        Comprueba si el servicio de Ollama está en ejecución.
        
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            bool: True si esta en ejecución y false en otro caso.
        """
        # Try-Except para manejo de errores.
        try:
            # Genera la URL para la petición.
            url:str = f"{self.__baseUrl}/api/tags"

            # Obtiene la respuesta de la API de Ollama.
            response:Response = requests.get(url=url)
            # Lanza una excepción en caso de que no haya sido correcta.
            response.raise_for_status()
            
            # Retorna si ha salido todo bien.
            return True
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"OllamaService.is_running() -> [{type(e).__name__}] No se ha podido comprobar si el servicio de Ollama está en ejecución. Trace: {e}")
        
    def list_installed_models(self) -> List[str]:
        """
        Lista los modelos instalados.
        
        Raises:
            OSError: En caso de que haya alguna excepción.
        Returns:
            List[str]: Listado con los modelos instalados.
        """
        # Try-Except para manejo de errores.
        try:
            # Genera la URL para la petición.
            url:str = f"{self.__baseUrl}/api/tags"

            # Obtiene la respuesta de la API de Ollama.
            response:Response = requests.get(url=url)
            # Lanza una excepción en caso de que no haya sido correcta.
            response.raise_for_status()
            
            # Retorna los modelos instalados.
            return response.json().get("models", [])   
            
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"OllamaService.list_installed_models() -> [{type(e).__name__}] No se han podido obtener los modelos instalados. Trace: {e}")
        
    def is_model_installed(self, model_tag:str) -> bool:
        """
        Comprueba si el modelo esta instalado.
        
        Args:
            model_tag (str): Etiqueta del modelo.
        Raises:
            OSError: En caso de que ocurra algún error.
        Returns:
            bool: True si el modelo esta instalado y false en otro caso.
        """
        # Try-Except para manejo de errores.
        try:           
            # Retorna si algún modelo coincide.
            return any(model_tag==model_name['model'] for model_name in self.list_installed_models())
        
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError()
    
    def install_model(self, model_tag) -> bool:
        """
        Instala el modelo de Ollama.
        
        Args:
            model_tag (str): Etiqueta del modelo.
        Raises:
            OSError: En caso de que ocurra algún error.
        Returns:
            bool: Si se ha instalado y False en caso contrario.
        """
        # Try-Except para manejo de errores.
        try:
            # Genera la URL para la petición.
            url:str = f"{self.__baseUrl}/api/pull"
            
            # Genera las cabeceras y los datos.
            headers:Dict = {'Content-Type':'application/json'}      # Cabeceras de la consulta.
            data:Dict = {
                'model':model_tag,
                'stream': False
            }
            
            # Obtiene la respuesta de la API de Ollama.
            response:Response = requests.post(url=url, headers=headers, data=json.dumps(data))
            # Lanza una excepción en caso de que no haya sido correcta.
            response.raise_for_status()
            
            # Ontiene los datos de la respuesta.
            json_content:Dict[str,any] = json.loads(response.text)
            # Comprueba si no se ha instaldo el modelo
            if json_content['status'] != 'success':
                # Lanza una excepción.
                raise OSError(f"No se pudo instalar el modelo. Status: {json_content['status']}")

        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"OllamaService.install_model() -> [{type(e).__name__}] No se ha podido instalar el modelo. Trace: {e}")
    
    def load_model(self, model_tag:str) -> None:
        """
        Carga el modelo en en GPU.
        
        Args:
            model_tag (str): Etiqueta del modelo.
        Raises:
            OSError: En caso de que ocurra algún error.
        """
        # Try-Except para manejo de errores.
        try:
            # Genera la URL para la petición.
            url:str = f"{self.__baseUrl}/api/chat"
            
            # Genera las cabeceras y los datos.
            headers:Dict = {'Content-Type':'application/json'}      # Cabeceras de la consulta.
            data:Dict = {
                'prompt': '',
                'model':model_tag,
                'stream': False
            }
            
            # Obtiene la respuesta de la API de Ollama.
            response:Response = requests.post(url=url, headers=headers, data=json.dumps(data))
            # Lanza una excepción en caso de que no haya sido correcta.
            response.raise_for_status()

        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"OllamaService.start_model() -> [{type(e).__name__}] No se ha podido cargar el modelo. Trace: {e}")
        
    def get_response(self, prompt:str) -> str:
        """
        Envía el prompt al modelo y genera la respuesta.
        
        Args:
            prompt (str): Prompt a enviar al modelo.
        Raises:
            OSError: En caso de que ocurra algún error.
        Returns:
            str: Respuesta generada por el modelo.
        """
        # Try-Except para manejo de errores.
        try:
            # Genera la URL para la petición.
            url:str = f"{self.__baseUrl}/api/generate"
            
            # Genera las cabeceras y los datos.
            headers:Dict = {'Content-Type':'application/json'}      # Cabeceras de la consulta.
            data:Dict = {
                'prompt': prompt,
                'model':self.__model.tag,
                'stream': False
            }
            
            # Obtiene la respuesta de la API de Ollama.
            response:Response = requests.post(url=url, headers=headers, data=json.dumps(data))
            # Lanza una excepción en caso de que no haya sido correcta.
            response.raise_for_status()
            
            # Carga el json.
            jsonData:Dict[str,any] = json.loads(response.text)
            
            # Almacena los parámetros obtenidos.
            ollamaModelData:OllamaModelDataDTO = OllamaModelDataDTO(
                totalDuration=(jsonData['total_duration'] / 1_000_000_000),
                loadDuration=(jsonData['load_duration'] / 1_000_000_000),
                promptEvalCount=jsonData['prompt_eval_count'],
                promptEvalDuration=(jsonData['prompt_eval_duration'] / 1_000_000_000),
                evalCount=jsonData['eval_count'],
                evalDuration=(jsonData['eval_duration'] / 1_000_000_000),
                speed=((jsonData['eval_count'] * 1_000_000_000) / jsonData['eval_duration'])
            )
            # Almacena el dato en un csv.
            save_in_csv(file_path=self.__measureFilePath, data=ollamaModelData)
            
            # Retorna la respuesta generada.
            return jsonData['response']
        
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"OllamaService.get_response() -> [{type(e).__name__}] No se ha podido obtener respuesta del modelo. Trace: {e}")