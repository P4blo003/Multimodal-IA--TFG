# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/common/url.py
# Autor: Pablo González García
# Descripción:
# Módulo con funciones relacionadas con urls.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from enum import Enum


# ---- CLASES ---- #
class UrlProtocol(Enum):
    """
    Enum que representa el protocolo que usa la URL.
    """
    # -- Valores -- #
    HTTP    = 0
    HTTPS   = 1

# ---- FUNCIONES ---- #
def get_url(host:str, port:int, protocol:UrlProtocol=UrlProtocol.HTTP) -> str:
    """
    Retorna la URL generada para un host y puerto.
    
    Args:
        host (str): Host de la URL.
        port (int): Puerto de la URL.
        protocol (UrlProtocol): El protocolo que usa la URL.

    Returns:
        str: URL completa de la forma `http://host:port`
    """
    # Establece el protocolo en función del parámetro dado.
    prot = ""
    match (protocol):
        case UrlProtocol.HTTP:
            prot = "http"
        case UrlProtocol.HTTPS:
            prot = "https"

    # Devuelve la URL.
    return f"{prot}://{host}:{port}"