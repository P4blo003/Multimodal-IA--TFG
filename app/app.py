# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/app.py
# Autor: Pablo González García
# Descripción: 
# Flujo principal del programa.
# -----------------------------------------------------------------------------

# ---- Modulos ---- #
import time

import logging
from utils.log.logger import get_logger

from ollama.server import OllamaServer
from ollama.client import OllamaClient
from ollama.classes import Response

# ---- Main ---- #
if __name__ == "__main__":
    
    # ---- Declaración de variables globales ---- #
    logger:logging.Logger = get_logger(name=__name__, file="app.log")      # Crea el logger de main.
    server:OllamaServer = None        # Inicializa el servidor como None.
    client:OllamaClient = None        # Inicializa el cliente como None.
    
    # ---- Declaración de funciones ---- #
    def end_program(exit_value:int = 0):
        """
        Finaliza el programa. Muestra un mensaje en el log informando del código de salida
        del mismo.
        
        Args:
            exit_value (int): Valor de salida del programa. Por defecto vale 0.
        """
        logger.info(f"Finalizado programa ({exit_value})")  # Imprime el mensaje.
        exit(exit_value)        # Finaliza el programa con el código de salida.
        
    # ---- Lógica principal ---- #
    logger.info("Iniciado programa.")   # Imprime el inicio del programa.
    
    # Inicializa el servidor y cliente de Ollama.
    server = OllamaServer()                 # Inicia el servidor de ollama.
    server.Start()                          # Inicia el servidor.    
    time.sleep(5)                           # Espera 5 segundos para que el servidor esté listo.
    
    client = OllamaClient()                 # Inicia el cliente de ollama.
    prompt = ""                             # Inicializa el prompt como vacío.
    
    try:
        
        while prompt.upper() != "QUIT":     # Mientras el prompt no sea "QUIT".
            prompt = input("🧠: ")            # Solicita un mensaje al usuario.
            
            if prompt.upper() == "QUIT":    # Si el mensaje es "QUIT":
                break                       # Sale del bucle.
            
            reply:Response = client.send_message(prompt) # Envía el mensaje al modelo.
        
            if reply:                               # Si la respuesta no es None.
                print(f"[Elapsed time: {reply.total_time} seconds.]")   # Imrpime el tiempo total de la respuesta.
                print(f"🤖 ({reply.model}): {reply.response}")          # Imprime la respuesta.
            
    except KeyboardInterrupt:
        print()                                 # Imprime una línea en blanco.
        logger.info("Interrupción del programa por teclado.")
        server.Stop()                           # Detiene el servidor.
        end_program(exit_value=0)               # Finaliza el programa.
    
    server.Stop()                           # Detiene el servidor.
    end_program(exit_value=0)           # Finaliza el programa.