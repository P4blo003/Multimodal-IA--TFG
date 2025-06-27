# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: csv.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene funciones relacionadas con el acceso, creación y eliminación
    de ficheros 'csv'.   
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
import csv
from typing import Dict, List
from pathlib import Path
# Librerías externas
from pydantic import BaseModel
# Librerías internas


# ---- FUNCIONES ---- #
def save_in_csv(file_path:Path, data:BaseModel) -> None:
    """
    Almacena el dato en un fichero csv.
    
    Args:
        file_path (Path): Ruta del fichero.
        data (BaseModel): Dato a añadir.
    Raises:
        OSError: En caso de que haya algún error.
    """
    # Try-Except para manejo de errores.
    try:
        # Convierte en diccionario plano.
        row:Dict[str,any] = data.model_dump()
        columns:List = list(row.keys())
        
        # Comprueba si existe el fichero.
        write_header = not file_path.exists()
        
        # Abre o crea el fichero.
        with file_path.open('a', newline='', encoding='utf-8') as fp:
            # Crea el objeto para escribir en el documento.
            writer = csv.DictWriter(fp, fieldnames=columns)
            # Si no hay cabeceras.
            if write_header:
                # Añade las cabeceras.
                writer.writeheader()
            # Añade la fila.
            writer.writerow(row)
    
    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"csv::save_csv() -> [{type(e).__name__}] No se pudo almacenar en el fichero csv. Trace: {e}")