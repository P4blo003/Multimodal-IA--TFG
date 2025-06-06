# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/core/ollama.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene las clases y funciones relacionadas con Ollama.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
import time
import json
from typing import Dict
from subprocess import Popen
from pathlib import Path
from requests import Response
from yaspin import yaspin
from utilities.system import create_subprocess, create_process
from utilities.network import get_response, post_response

from logging import Logger
from utilities.logger import create_logger

from config.schema import OllamaConfig, SystemConfig, LoggerConfig


# ---- VARIABLES GLOBALES ---- #
API_TAG:str = 'API'                 # Tag para referenciar el proceso de ejecución de la API.


# ---- CLASES ---- #
class OllamaController:
    """
    Clase encargada de gestionar los servicios de Ollama.
    """
    # -- Métodos por defecto -- #
    def __init__(self, logger_cfg:LoggerConfig):
        """
        Inicializa la instancia.
        
        Args:
            logger_cfg (LoggerConfig): Configuración del logger.
        """
        # Inicializa las propiedades.
        self.__logger:Logger = create_logger(logger_name=__name__, cfg=logger_cfg, console=True, file="server.log")
        self.__process:Dict[int, Popen] = {}
        
        self.__logger.info("Controlador de Ollama iniciado.")       # Imprime la información.
    
    
    # -- Métodos públicos -- #
    def start_api(self, ollama_cfg:OllamaConfig, system_cfg:SystemConfig, env:dict) -> None:
        """
        Inicializa la ejecución de la API de Ollama.
        
        Args:
            ollama_cfg (OllamaConfig): Configuración de Ollama.
            system_cfg (SystemConfig): Configuración del sistema.
            env (Dict[str, any]): Variables de entorno.
        """
        # Obtiene el proceso asociado a la API.
        api_process:Popen = self.__process.get(API_TAG)
        
        # Comprueba si hay un proceso en ejecución.
        if api_process:         # Si todavía hay un proceso asignado.
            self.stop_api()     # Finaliza el proceso.
        
        # Inicia el subproceso.
        args = [str(ollama_cfg.exe)]+["serve"]                                      # Genera los argumentos del binario.
        file:Path = Path(os.path.join(system_cfg.logDir, ollama_cfg.api.logFile))   # Crea el PATH del fichero de salida.
        self.__process[API_TAG] = create_subprocess(args=args, env=env, file=file)  # Crea el proceso.
        
        # Espera un tiempo para asegurar que el servidor se inicia correctamente.
        with yaspin(text="Iniciando servicio Ollama ...") as sp:
            time.sleep(ollama_cfg.api.startupWaitSeconds)                           # Espera x segundos para que se inicie el servicio de Ollama.
        
        self.__logger.info(f"Subproceso de la API de Ollama iniciado [{self.__process[API_TAG].pid}].")     # Imprime la información.
    
    def stop_api(self) -> None:
        """
        Finaliza la ejecución de la API de Ollama.
        """
        # Obtiene el proceso asociado a la API.
        api_process:Popen = self.__process.get(API_TAG)
        
        # Comprueba si hay un proceso en ejecución.
        if not api_process:     # Si no hay ningún proceso asignado.
            return
        
        # Detiene el proceso.
        pid:int = api_process.pid       # Obtiene el PID del proceso.
        api_process.terminate()         # Termina el subproceso.
        self.__process[API_TAG] = None  # Establece como None el proceso asignado a la API.
        
        self.__logger.info(f"Subproceso de la API de Ollama detenido [{pid}].")     # Imprime la información.

    def check_model(self,ollama_cfg:OllamaConfig, env:dict) -> None:
        """
        Comprueba si el modelo esta instalado y en caso de que no lo esté, lo instala.
        
        Args:
            ollama_cfg (OllamaConfig): Configuración de Ollama.
            env (dict): Variables de entorno.
        """
        # Comprueba si el modelo está instalado.
        if not OllamaService.model_installed(ollama_cfg=ollama_cfg):
            # Instala el modelo.
            OllamaService.install_model(ollama_cfg=ollama_cfg, env=env)
        
        self.__logger.info(f"Modelo [{ollama_cfg.api.model.name}] instalado.")       # Imprime la información.


class OllamaService:
    """
    Clase que proporciona acceso a los servicios de Ollama.
    """
    # -- Métodos estáticos -- #
    @staticmethod
    def model_installed(ollama_cfg:OllamaConfig) -> bool:
        """
        Comrpueba si el modelo esta instalado en el sistema.
    
        Args:
            ollama_cfg (OllamaConfig): Configuración de Ollama.
        
        Returns:
            bool: True si el modelo esta instalado y False en otro caso.
        """
        # Genera la URL de la API de ollama.
        url:str = f"http://{ollama_cfg.api.host}:{ollama_cfg.api.port}/api/tags"
        
        # Solicita el listado de modelos de Ollama.
        response:Response = get_response(url=url)
        installed_models = response.json().get("models", [])
        # Retorna si existe algún modelo con el nombre dado.
        return any(model.get("name", "").startswith(ollama_cfg.api.model.name) for model in installed_models)

    @staticmethod
    def install_model(ollama_cfg:OllamaConfig, env:dict, reinstall:bool=False) -> None:
        """
        Instala el modelo dado.
        
        Args:
            ollama_cfg (OllamaConfig): Configuración de Ollama.
            env (dict): Variables de entorno.
            reinstall (bool): True si se desea reinstalar el modelo. False en otro caso.
        """
        # Inicia el proceso.
        args = [str(ollama_cfg.exe)]+["pull"]+[ollama_cfg.api.model.name]      # Genera los argumentos del binario.
        
        # Instala el modelo.
        with yaspin(text=f"Instalando modelo [{ollama_cfg.api.model.name}] ...") as sp:
            create_process(args=args, env=env)                        # Crea el proceso.
    
    @staticmethod
    def get_response(prompt:str, ollama_cfg:OllamaConfig) -> str:
        """
        Envía el prompt al modelo y recibe la respuesta.
        
        Args:
            prompt (str): El prompt del modelo.
            ollama_cfg (OllamaConfig): Configuración de Ollama.

        Returns:
            str: Respuesta generada por el modelo.
        """
        # Crea la URL completa.
        url:str = f"http://{ollama_cfg.api.host}:{ollama_cfg.api.port}/api/generate"
        
        # Genera los campos de la consulta.
        headers:Dict = {'Content-Type':'application/json'}      # Cabeceras de la consulta.
        data:Dict = {
            'model':ollama_cfg.api.model.name,
            'prompt':prompt,
            'stream': False
        }

        # Obtiene la respuesta del modelo.
        response:Response = post_response(url=url, headers=headers, data=json.dumps(data))     # Envía la petición.
        
        # Comprueba el estado de la respuesta.
        if response.status_code != 200:
            raise Exception("No se pudo obtener respuesta del modelo.")
        
        # Obtiene los datos.
        data:Dict = json.loads(response.text)

        # Devuelve la respueta generada.
        return data['response']