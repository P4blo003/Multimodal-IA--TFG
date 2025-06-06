# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/client/src/main.py
# Autor: Pablo González García
# Descripción: 
# Punto de entrada del cliente. Obtiene las querys del cliente, las envía
# al servidor y obtiene la respuesta del mismo.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
import requests

from yaspin import yaspin

from model.query import QueryDTO
from model.response import ResponseDTO


# ---- FUNCIONES GLOBALES ---- #
SESSION_ID:int = None


# ---- FLUJO PRINCIPAL ---- #
if __name__ == "__main__":

    # Try-except para manejo de excepciones.
    try:      
        #Hacer una request y solicitar un ID.
        response:requests.Response = requests.get(url="http://localhost:9999/chat/init")
        
        # Comprueba el estado de la sesión.
        if response.status_code != 200:
            raise Exception("No se pudo obtener un ID de sesión por parte del servidor.")   # Lanza una excepción.
    
        SESSION_ID = ResponseDTO.model_validate_json(response.content).session_id      # Obtiene el ID recibido.
        print(f"Sesión iniciada | ID: {SESSION_ID}")            # Imprime información.
        
        response = requests.post(url=f"http://localhost:9999/chat/question/{SESSION_ID}", json=QueryDTO(content="Hola, que tal?").__dict__)

    # Si se detecta un Ctrl+C.
    except KeyboardInterrupt:
        print()
        print("🔶: Ctrl+C detectado. Finalizando cliente.")
    # Si se detecta alguna excepción.
    except Exception as e:
        print(f"🔶: {e}")