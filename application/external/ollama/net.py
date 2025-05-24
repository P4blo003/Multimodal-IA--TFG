# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/external/ollama/net.py
# Autor: Pablo González García
# Descripción: 
# Módulo que contiene clases y funciones relacionadas con las peticiones
# al servicio de Ollama.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import json
from requests import post
from requests import Response
from dataclasses import dataclass
from typing import Optional

from common.math import ns_to_sec


# ---- CLASES ---- #
@dataclass
class OllamaResponse:
    """
    Almacena los datos de la respuesta obtenida por el modelo Ollama.
    
    Attributes:
        statusCode (int): Estado de la respuesta.
        response (Optional[str]): Respuesta obtenida.
        loadDuration (Optional[float]): Duración total en cargar el modelo, en segundos.
        promptEvalDuration (Optional[float]): Tiempo empleado en evaluar el prompt, en segundos.
        responseGenDuration (Optional[float]): Duración total en generar la respuesta, en segundos.
        promptTokens (Optional[int]): Número de tokens en el prompt.
        responseTokens (Optional[int]): Número de tokens en la respuesta.
        speed (Optional[float]): Velocidad de generación de la respuesta, en tokens/segundo.
    """
    # -- Atributes -- #
    statusCode:int = 0
    response:str= "NaN"
    loadDuration:float = 0.0
    promptEvalDuration:float = 0.0
    responseGenDuration:float = 0.0
    promptTokens:int = 0
    responseTokens:int = 0
    speed:float = 0.0
    

# ---- FUNCIONES ---- #
def generate_chat_response(ollama_url:str, model_name:str, prompt:str) -> OllamaResponse:
    """
    Envía una query al modelo de Ollama y devuelve la respuesta obtenida.
    
    Args:
        ollama_url (str): Url del servicio de Ollama.
        model_name (str): El modelo de Ollama.
        prompt (str): El prompt a enviar al modelo.
    
    Returns:
        OllamaResponse: Estructura OllamaResponse con los datos de la respuesta.
    """
    # Respuesta a devolver.
    resp:OllamaResponse = OllamaResponse()
    
    # Crea la URL completa.
    __url:str = f"{ollama_url}/api/generate"
    
    # Genera los campos de la consulta.
    __headers:dict = {'Content-Type':'application/json'}      # Cabeceras de la consulta.
    __data:dict = {
        'model':model_name,
        'prompt':prompt,
        'stream': False
    }
    
    # Obtiene la respuesta del modelo.
    __response:Response = post(url=__url, headers=__headers, data=json.dumps(__data))     # Envía la petición.
    resp.statusCode = __response.status_code
    # Si la respuesta es correcta.
    if __response.status_code == 200:
        __text:str = __response.text
        __data:dict = json.loads(__text)
        # Procesa los datos obtenidos y los alamcena en la respuesta.
        resp.response = str(__data['response']).strip()
        resp.loadDuration = ns_to_sec(ns=__data['load_duration'])
        resp.promptEvalDuration = ns_to_sec(ns=__data['prompt_eval_duration'])
        resp.responseGenDuration = ns_to_sec(ns=__data['eval_duration'])
        resp.promptTokens = __data['prompt_eval_count']
        resp.responseTokens = __data['eval_count']
        resp.speed = resp.responseTokens / resp.responseGenDuration
    
    # Devuelve la respuesta.
    return resp

def install_model(ollama_url:str, model_name:str) -> int:
    """
    Realiza una petición POST al servicio Ollama para instalar el modelo.
    
    Args:
        ollama_url (str): Url del servicio de Ollama.
        model_name (str): El modelo de Ollama.
        
    Returns:
        int: El estado de la respuesta del servicio de Ollama.
    """
    # Crea la URL completa.
    __url:str = f"{ollama_url}/api/pull"
    
    # Genera los campos de la consulta.
    __data:dict = {'name': model_name}
    
    # Instala el modelo.
    response = post(url=__url, json=__data)
    
    # Devuelve el estado de la respuesta.
    return response.status_code