#!/usr/bin/env python3

# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: client.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Programa cliente que se encarga de enviar preguntas al servidor y mostrar 
        las respuestas.
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
from typing import Dict
import json
# Librerías externas
import requests
# Librerías internas


# ---- FLUJO PRINCIPAL ---- #
if __name__ == "__main__":
    
    # Genera variables para la ejecución.
    headers:Dict[str,any] = {'Content-Type':'application/json'}
    
    # Búcle infinito para el chat.
    while True:
        
        # Try-Except para manejar errores.
        try:
            
            # Solicita una pregunta al usuario.
            question = input("🧑 Pregunta:")
            
            # Envía la pregunta al servidor.
            msg:Dict[str,any] = {"content": question}
                
            # Solicita la respuesta al servidor.
            response:requests.Response = requests.post(url=f"http://localhost:49153/chat", headers=headers, json=msg)
            
            # Lanza excepción si hay error.
            response.raise_for_status()
            
            # Imprime la respuesta del servidor.
            print(f"🤖 Respuesta: {json.loads(response.text)['content']}")
        
        # Si se detecta Ctrl+C.
        except KeyboardInterrupt:
            # Imprime información.
            print("\nSaliendo del programa...")
            # Finaliza el programa.
            break
        
        # Si se detecta cualquier error.
        except Exception as e:
            # Imprimer información.
            print(f"No se ha podido obtener respuesta del servidor: {e}")