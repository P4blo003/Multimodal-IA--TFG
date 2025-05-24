# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/external/ollama/core.py
# Autor: Pablo González García
# Descripción: 
# Módulo encargado de gestionar todo lo reclacionado con el servicio
# de Ollama.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
import time
from subprocess import Popen
from pathlib import Path

from logging import Logger
from common.logger import create_logger
from common.net import address_in_use, generate_url
from common.process import start_subprocess

from .model import model_installed, install_model

from yaspin import yaspin

from config.context import CFG, ENV


# ---- CLASES ---- #
class OllamaManager:
    """
    Instancia que se encarga de gestionar el servicio de Ollama. Ayuda a la gestión
    del subproceso de Ollama, así como de la instalación/comprobación de los
    modelos de ia.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la instancia.
        """
        # Inicializa las propiedades.
        self.__logger:Logger = create_logger(logger_name=__name__, file="app.log")
        self.__subProcess:Popen = None
        self.__url:str = generate_url(host=CFG.ollama.host, port=CFG.ollama.port)
    
    # -- Propiedades -- #
    @property
    def PID(self) -> int:
        """
        Devuelve el PID del subproceso encargado de ejecutar el binario de
        Ollama.
        
        Returns:
            int: PID del subproceso.
        """
        # Si existe un subproceso.
        if self.__subProcess:
            return self.__subProcess.pid

        # En caso de que no exista un subproceso.
        return None 
    @property
    def Url(self) -> str:
        """
        Devuelve la URL del servicio Ollama.
        
        Returns:
            str: Url del servicio de Ollama.
        """
        return self.__url
    
    # -- Métodos públicos -- #
    def StartService(self) -> any:
        """
        Inicializa el servicio de Ollama. Ejecuta el binario de Ollama similar
        al comando `ollama serve`.
        """
        # Comprueba si el subproceso todavía está asignado.
        if self.__subProcess:
            self.__logger.error(f"El subproceso todavía esta asignado. PID: {self.PID}")      # Imprime información.
            return
        
        # Comprueba si la dirección esta en uso.
        if address_in_use(host=CFG.ollama.host, port=CFG.ollama.port):
            self.__logger.error(f"La dirección {CFG.ollama.host}:{CFG.ollama.port} ya está en uso.")    # Imprime información.
            return
        
        # Inicia el subproceso de Ollama serve.
        __args = [str(CFG.ollama.exe)]+["serve"]
        __file:Path = Path(os.path.join(CFG.system.logsDirectory, CFG.ollama.logFile))
        self.__subProcess = start_subprocess(args=__args, env=ENV, file=__file)
        
        # Espera un tiempo para asegurar que el servidor se inicia correctamente.
        with yaspin(text="Iniciando servicio Ollama ...") as sp:
            time.sleep(CFG.ollama.startupWaitSeconds)
            
        self.__logger.info(f"Servicio de Ollama iniciado. URL: {self.Url} | PID: {self.PID}")          # Imprime información.
    
    def StopService(self) -> any:
        """
        Detiene el subproceso que ejecuta el servicio de Ollama.
        """
        # Comprueba si el subproceso todavía está asignado.
        if not self.__subProcess:
            self.__logger.error("No hay un subproceso asignado.")       # Imprime información.
            return
        
        # Finaliza el proecso.
        __pid:int = self.__subProcess.pid   # Almacena el pid del subproceso.
        self.__subProcess.terminate()       # Termina el subproceso.
        self.__subProcess.wait()            # Espera a que el proceso finalice.
        self.__subProcess = None
        
        self.__logger.info(f"Servicio de Ollama detenido. PID: {__pid}")        # Imprime información.
    
    def CheckModel(self) -> any:
        """
        Comprueba si el modelo está instalado y en caso de que no lo este, lo instala.
        """
        # Comprueba si el model está instalado.
        if not model_installed(ollama_url=self.Url, model_name=CFG.model.name):
            self.__logger.warning(f"Modelo {CFG.model.name} no instalado.")     # Imprime información.
        
            # Instala el modelo.
            with yaspin(text=f"Instalando modelo {CFG.model.name} ...") as sp:
                # Instala el modelo.
                install_model(bin_path=CFG.ollama.exe, model_name=CFG.model.name, env=ENV)
        
        self.__logger.info(f"Modelo {CFG.model.name} instalado.")                # Imprime información.