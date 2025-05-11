# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/ollama/server.py
# Autor: Pablo González García
# Descripción: 

# -----------------------------------------------------------------------------

# ---- Modulos ---- #
import os
import subprocess

import logging
from utils.log.logger import get_logger

from config.context import OLLAMA_CFG

# ---- Clases ---- #
class OllamaServer:
    """
    Clase encargada de iniciar y detener el servidor de Ollama.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Constructor que prepara el entorno.
        """
        self.__env = os.environ.copy()    # Copia las variables de entorno.
        self.__env['OLLAMA_HOST'] = f"{OLLAMA_CFG.host}:{OLLAMA_CFG.port}"    # Establece los valores.
        self.__cfg = OLLAMA_CFG
        self.__logger:logging.Logger = get_logger(name=__name__, file="app.log", file_only=True)  # Crea el logger de la clase.
        self.__process:subprocess.Popen = None                  # Inicializa el proceso como None.
    
    # -- Propiedades -- #
    @property
    def PID(self) -> int:
        """
        Devuelve el PID del proceso del servidor Ollama.
        """
        # Si el proceso no está inicializado.
        if not self.__process:
            return None
        # Retorna el PID.
        return self.__process.pid

    # -- Métodos -- #
    def Start(self):
        """
        Inicia sel servidor Ollama ejecutando el bianrio como proceso hijo.
        Espera unos segundos para asegurar que el servidor se inicia correctamente.
        """
        # Si el proceso ya está inicializado.
        if self.__process:
            return
        # Si debe ser silencioso.
        if self.__cfg.silent:
            with open(os.devnull, 'w') as devnull:
                self.__process = subprocess.Popen(
                    [str(self.__cfg.bin)] + ["serve"],
                    env=self.__env,
                    stdout=devnull,
                    stderr=devnull)
        # Si no debe ser silencioso.
        else:
            with open(self.__cfg.file, 'w') as file:
                self.__process = subprocess.Popen(
                    [str(self.__cfg.bin)] + ["serve"],
                    env=self.__env,
                    stdout=file,
                    stderr=file)
        
        self.__logger.info(f"Servidor Ollama iniciado PID: {self.__process.pid} | URL: https://{self.__cfg.host}:{self.__cfg.port}")  # Imprime el mensaje.
        
    def Stop(self):
        """
        Termina el proceso del servidor Ollama si está activo.
        """
        # Si el proceso no está inicializado.
        if not self.__process:
            return
        # Finaliza el proceso.
        pid:int = self.__process.pid # Guarda el PID.
        self.__process.terminate()
        self.__process.wait()      # Espera a que el proceso finalice.
        self.__process = None      # Establece el proceso como None.
        
        self.__logger.info(f"Servidor Ollama detenido PID: {pid}")