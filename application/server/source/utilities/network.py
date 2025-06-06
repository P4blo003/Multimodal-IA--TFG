# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/utilities/network.py
# Autor: Pablo González García
# Descripción:
# Módulo con clases y funciones relacionadas con peticiones.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from typing import Dict
from requests import Response
from requests import get, post


# ---- FUNCIONES ---- #
def get_response(url:str) -> Response:
    """
    Realiza una petición GET a la URL dada y procesa la respuesta.
    
    Args:
        url (str): URL a la que hacer la petición GET.
    
    Response:
        Response: Respuesta obtenida de la petición.
    """
    # Realiza la petición.
    response:Response = get(url=url)
    
    # Lanza una excepcion en caso de que no haya sido correcta.
    response.raise_for_status()
    
    # Retorna la respuesta.
    return response

def post_response(url:str, headers:Dict, data:str) -> Response:
    """
    Realiza una petición POST a la URL dada y procesa la respuesta.
    
    Args:
        url (str): URL a la que hacer la petición POST.
        json (Dict): Datos a enviar.
        data (str): Datos a enviar.
    
    Response:
        Response: Respuesta obtenida de la petición.
    """
    # Realiza la petición.
    response:Response = post(url=url, headers=headers, data=data)
    
    # Lanza una excepcion en caso de que no haya sido correcta.
    response.raise_for_status()
    
    # Retorna la respuesta.
    return response