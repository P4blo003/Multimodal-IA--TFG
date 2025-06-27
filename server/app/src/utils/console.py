# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: app/src/utils/console.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene funciones relacionadas con la consola. Permite mostrar
    cabeceras y mensajes en diferentes formatos.   
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- IMPORTS ---- #
# Librerías estándar
import shutil
from enum import Enum
from datetime import datetime
# Librerías externas

# Librerías internas


# ---- CLASES ---- #
class MessageType(Enum):
    """
    Clase que define los tipos de mensaje que se pueden imprimir por consola.
    
    Attributes:
        DEFAULT (int): Mensaje por defecto, sin formato especial.
        INFO (int): Mensaje informativo, con formato azul.
        WARNING (int): Mensaje de advertencia, con formato amarillo.
        ERROR (int): Mensaje de error, con formato rojo.
    """
    # -- Tipos -- #
    DEFAULT     = 0,
    INFO        = 1,
    WARNING     = 2,
    ERROR       = 3
    

# ---- FUNCIONES ---- #
def print_header(title:str, splitter:str) -> None:
    """
    Imprime la cabecera del servidor (por consola).
    
    Args:
        title (str): El título de la cabecera.
        splitter (str): El carácter que se usará para separar el título de la cabecera.
    """
    # Arregla el título.
    title = title.strip().upper()               # Elimina espacios al principio y al final, y lo convierte a mayúsculas.
    
    # Calcula el tamaño de la cabecera.
    cols:int = shutil.get_terminal_size().columns       # Obtiene el número de columnas.
    space:int = (cols - len(title) ) // 2               # Calcula el espacio a la izquierda.
    
    # Imprime la cabecera.
    print(f"\n{splitter * cols}")                 # Imprime la línea de separación.
    print(f"{' ' * space}{title}")              # Imprime el título centrado. 
    print(f"{splitter * cols}\n")               # Imprime la línea de separación.

def print_subHeader(title:str, splitter:str) -> None:
    """
    Imprime la subcabecera del servidor (por consola).
    
    Args:
        title (str): El título de la casubcabecerabecera.
        splitter (str): El carácter que se usará para separar el título de la subcabecera.
    """
    # Arregla el título.
    title = title.strip().upper()               # Elimina espacios al principio y al final, y lo convierte a mayúsculas.
    title = f" {title} "                        # Añade espacios antes y después del título.
    
    # Calcula el tamaño de la cabecera.
    cols:int = shutil.get_terminal_size().columns // 2  # Obtiene el número de columnas.
    space:int = (cols - len(title) ) // 2               # Calcula el espacio a la izquierda.
    
    # Imprime la cabecera.
    print(f"\n{splitter * space}{title}{splitter * space}")                 # Imprime la línea de separación.

def print_message(message:str, type:MessageType=MessageType.DEFAULT) -> None:
    """
    Imprime un mensaje por consola. Muestra cierta información en función del tipo
    de mensaje.
    
    Args:
        message (str): El mensaje por defecto a mostrar.
    """
    # Genera el string a imprimir.
    string:str = f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    
    # Añade información en función del tipo de mensaje.
    match (type):
        case MessageType.DEFAULT:
            string += " - DEFAULT"
        case MessageType.INFO:
            string += " - \033[32mINFO\033[0m"
        case MessageType.WARNING:
            string += " - \033[33mWARNING\033[0m"
        case MessageType.ERROR:
            string += " - \033[31mERROR\033[0m"
    
    # Añade el mensaje.
    string += f" - {message}"
    
    # Imprime el mensaje por consola.
    print(string)