# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/common/net.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene funciones relacionadas con URL, red, etc.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from enum import Enum
import socket


# ---- ENUMS ---- #
class RequestProtocol(Enum):
    """
    Enumerator que representa los tipos de protocolos.
    """
    # -- Atributos -- #
    HTTP = 0
    HTTPS = 1


# ---- FUNCIONES ---- #
def generate_url(host:str, port:int, protocol:RequestProtocol=RequestProtocol.HTTP) -> str:
    """
    Genera una URL para una dirección y protocolos dados.
    
    Args:
        host (str): Host de la dirección.
        port (int): Puerto de la dirección.
        protocol (RequestProtocol): Tipo de protocolo a emplear.
    
    Returns:
        str: La URL generada.
    """
    # Establece el protocolo.
    url:str = ""
    match (protocol):
        case RequestProtocol.HTTP:
            url += "http"
        case RequestProtocol.HTTPS:
            url += "https"

    # Añade el host y puertos.
    url += f"://{host}:{port}"
    
    # Devuelve la URL generada.
    return url

def address_in_use(host:str, port:int) -> bool:
    """
    Comprueba si la dirección ya esta en uso.
    
    Args:
        host (str): El host de la dirección.
        port (int): El puerto de la dirección.

    Returns:
        bool: True si la dirección ya esta en uso y False en otro caso.
    """
    # Abre un socket.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex((host, port))
    
    return result == 0  # Si es 0, significa que esta en uso.