#!/usr/bin/env python3

# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: main.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene el flujo principal del servidor.   
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar

# Librerías externas

# Librerías internas
import context.singleton as CtxSingleton
import core.factory.ollama as OllamaFactory
import core.factory.uvicorn as UvicornFactory
import core.factory.rag as RagFactory
import core.factory.prompt as PromptFactory
from core.services.ollama import OllamaService
from core.services.uvicorn import UvicornService
from core.services.rag import RagService
from utils import console


# ---- FUNCIONES ---- #
def start() -> None:
    """
    Inicializa las configuraciones y servicios. Además, comprubea que todo este inicializado e instalado.
    
    Raises:
        OSError: En caso de que haya algún error.
    """
    # Try-Except para manejo de errores.
    try:
        # Inicaliza la configuración.
        CtxSingleton.init()
        # Imprime la información.
        console.print_message(message='Contexto iniciado.', type=console.MessageType.INFO)
                
        # Inicializa y registra los servicios.
        CtxSingleton.get_ctx().add_service(key='ollama', service=OllamaFactory.create_ollama_service(ctx=CtxSingleton.get_ctx()))
        CtxSingleton.get_ctx().add_service(key='uvicorn', service=UvicornFactory.create_uvicorn_service(ctx=CtxSingleton.get_ctx()))
        CtxSingleton.get_ctx().add_service(key='rag', service=RagFactory.create_rag_service(ctx=CtxSingleton.get_ctx()))
        CtxSingleton.get_ctx().add_service(key='prompt', service=PromptFactory.create_prompt_service(ctx=CtxSingleton.get_ctx()))
        # Imprime la información.
        console.print_message(message='Servicios registrados.', type=console.MessageType.INFO)
        
        # Obtiene los servicios necesarios para facilitar el acceso.
        ollama_service:OllamaService = CtxSingleton.get_ctx().get_service(key='ollama', t=OllamaService)
        rag_service:RagService = CtxSingleton.get_ctx().get_service(key='rag', t=RagService)
        
        # Comprueba si el servicio de Ollama está en ejecución.
        ollama_service.check_running()
        
        # Comprueba si el modelo está instalado.
        if not ollama_service.is_model_installed(model_tag=ollama_service.Model.tag):
            # Imprime la información.
            console.print_message(message='El modelo no está instalado en Ollama. Instalando ...', type=console.MessageType.WARNING)
            # Instala el modelo.
            ollama_service.install_model(model_tag=ollama_service.Model.tag)
        # Imprime la información.
        console.print_message(message='Modelo de Ollama instalado.', type=console.MessageType.INFO)
        
        # Carga el modelo.
        ollama_service.load_model(model_tag=ollama_service.Model.tag)
        # Imprime la información.
        console.print_message(message='Modelo cargado.', type=console.MessageType.INFO)
        
        # Comprueba si el modelo de embeddings esta instalado.
        if not rag_service.is_model_installed(model_tag=rag_service.Model.tag):
            # Imprime la información.
            console.print_message(message='El modelo de embeddings no está instalado. Instalando ...', type=console.MessageType.WARNING)
            # Instala el modelo.
            rag_service.install_model(model_tag=rag_service.Model.tag)
        # Imprime la información.
        console.print_message(message='Modelo de embeddings instalado.', type=console.MessageType.INFO)

        # Imprime la información.
        console.print_message(message='Calculando embeddings.', type=console.MessageType.INFO)
        # Calcula los embeddings.
        rag_service.make_embeddings()
        # Imprime la información.
        console.print_message(message='Embeddings calculados.', type=console.MessageType.INFO)
        

    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"main::start() -> [{type(e).__name__}] No se ha podido iniciar el servidor. Trace: {e}")
    
    
# ---- FLUJO PRINCIPAL ---- #
if __name__ == '__main__':
    
    # Try-Except para manejo de excepciones.
    try:
        # Imprime la cabecera.
        console.print_header(title='Server', splitter='=')
        
        # Imprime la subcabecera.
        console.print_subHeader(title='Inicialización', splitter='*')
        # Inicia el servidor.
        start()
        
        # Obtiene el servicio de uvicorn para facilitar el acceso.
        uvicorn_service:UvicornService = CtxSingleton.get_ctx().get_service(key='uvicorn', t=UvicornService)
        
        # Imprime la subcabecera.
        console.print_subHeader(title='Uvicorn', splitter='*')
        # Inicia Uvicorn.
        uvicorn_service.run()
        
    # Si ocurre algún error.
    except Exception as e:
        # Imprime el error.
        console.print_message(message=f'main::main() -> {e}', type=console.MessageType.ERROR)