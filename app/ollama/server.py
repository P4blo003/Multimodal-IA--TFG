# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/ollama/server.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene la clase OllamaServer, que se encarga de
# iniciar y detener el servidor de Ollama.
# -----------------------------------------------------------------------------


# ---- Modulos ---- #
import os
import time
import subprocess
from pathlib import Path

from yaspin import yaspin

import logging
from common.logger import get_logger

from common.url import get_url

from .model import model_installed, install_model

from config.context import CONFIG, ENV


# ---- Clases ---- #
class OllamaServer:
    """
    Clase encargada de iniciar y detener el servidor de Ollama.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa el servidor de Ollama.
        """
        self.__logger:logging.Logger = get_logger(name=__name__, file="app.log")    # Crea el logger de la clase.
        self.__process:subprocess.Popen = None                                      # Inicializa el proceso como None.
    
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
    
    # -- Métodos privados -- #
    def __init_process(self) -> bool:
        """
        Inicia el subproceso del servidor Ollama. Espera unos segundos para asegurar
        que el servicio se inicia correctamente.
        """
        # Si el proceso ya está inicializado.
        if self.__process:
            return
        
        # TODO: Comprobar si ya hay algún servicio ejecutandoes en el host y puerto dados.
        
        # Si debe ser silencioso.
        if CONFIG.ollama.silent:
            with open(os.devnull, 'w') as devnull:
                self.__process = subprocess.Popen(
                    [str(CONFIG.ollama.executablePath)] + ["serve"],
                    env=ENV,
                    stdout=devnull,
                    stderr=devnull)
        # Si no debe ser silencioso.
        else:
            path:Path = Path(os.path.join(CONFIG.system.logsDirectory, CONFIG.ollama.logFile)) # Genera el path.
            with path.open('w', encoding='utf-8') as file:
                self.__process = subprocess.Popen(
                    [str(CONFIG.ollama.executablePath)] + ["serve"],
                    env=ENV,
                    stdout=file,
                    stderr=file)
        
        # Espera un tiempo para asegurar que el servidor se inicia correctamente.
        with yaspin(text="Iniciando servidor Ollama ...") as sp:
            time.sleep(CONFIG.ollama.startupWaitSeconds)
    
    def __check_model(self):
        """
        Comprueba que el modelo este instalado y en caso de que no lo este, lo instala.
        """
        # Si el modelo no esta instalado.
        if not model_installed(CONFIG.model.name):
            self.__logger.warning(f"Modelo {CONFIG.model.name} no encontrado.")  # Imprime información.
            # Instala el modelo.
            with yaspin(text="Instalando modelo ...") as sp:
                install_model(CONFIG.ollama.executablePath, CONFIG.model.name)
            self.__logger.info(f"Modelo {CONFIG.model.name} instalado.")                        # Imprime información.

    # -- Métodos públicos -- #
    def Start(self):
        """
        Inicia sel servidor Ollama ejecutando el bianrio como proceso hijo.
        Espera unos segundos para asegurar que el servidor se inicia correctamente.
        """
        # Inicia el subproceso.
        self.__init_process()
        # Imprime mensaje de información.
        self.__logger.info(f"Servicio Ollama iniciado PID: {self.__process.pid} | URL: {get_url(host=CONFIG.ollama.host, port=CONFIG.ollama.port)}")  # Imprime el mensaje.
        # Comprueba que exista el modelo y lo instala en caso de que no exista.
        self.__check_model()
    
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