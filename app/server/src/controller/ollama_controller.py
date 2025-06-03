# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/controller/ollama_controller.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene la clase para gestionar todo lo relacionado con
# Ollama.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import os
import time
from yaspin import yaspin
from pathlib import Path
from subprocess import Popen
from utils.process import start_subprocess

from logging import Logger
from utils.logger import create_logger

from config.context import CFG, ENV


# ---- CLASES ---- #
class OllamaController:
    """
    Controlador de Ollama. Gestiona todos los servicios relacionadaso con Ollama.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la instancia.
        """
        # Inicializa las propiedades.
        self.__ollamaServeProc:Popen    = None
        self.__logger:Logger            = create_logger(logger_name=__name__, cfg=CFG.logger, console=True, file='server.log')
    
    # -- Métodos públicos -- #
    def start_serve(self) -> None:
        """
        Inicializa el servidio de Ollama que permite la ejecución de los modelos.
        """
        # Comrpueba si el proceso de Ollama esta asignado.
        if self.__ollamaServeProc:
            self.__logger.warning("El subproceso de Ollama Serve ya esta asignado")       # Imprime el aviso.
            return                  # Finaliza el método.
        
        # Inicia el subproceso de Ollama serve.
        args = [str(CFG.ollama.exe)]+["serve"]
        file:Path = Path(os.path.join(CFG.logger.logDir, CFG.ollama.logFile))
        self.__ollamaServeProc = start_subprocess(args=args, env=ENV, file=file)          # Comienza el subproceso.
        
        # Espera un tiempo para asegurar que el servidor se inicia correctamente.
        with yaspin(text="Iniciando servicio Ollama ...") as sp:
            time.sleep(CFG.ollama.startupWaitSeconds)                                   # Espera x segundos para que se inicie el servicio de Ollama.
        
        self.__logger.info(f"Servicio de Ollama iniciado | PID: {self.__ollamaServeProc.pid}")       # Imprime la información.
    
    def stop_serve(self) -> None:
        """
        Detiene el servicio de Ollama que permite la ejecución de los modelos.
        """
        # Comprueba si el proceso de Ollama esta asignado.
        if not self.__ollamaServeProc:
            self.__logger.warning("El subproceso de Ollama Serve no está asignado")    # Imprime el aviso.
            return                  # Finaliza el método.
        
        # Finaliza el proecso.
        pid:int = self.__ollamaServeProc.pid        # Almacena el pid del subproceso.
        self.__ollamaServeProc.terminate()          # Termina el subproceso.
        self.__ollamaServeProc.wait()               # Espera a que el proceso finalice.
        self.__ollamaServeProc = None
        
        # Si hay un proceso de Ollama asignado.
        self.__logger.info(f"Servicio de Ollama detenido | PID: {pid}")       # Imprime la información.