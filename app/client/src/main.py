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

from model.query import Query
from model.response import Response


# ---- FUNCIONES GLOBALES ---- #
SESSION_ID:int = None


# ---- FLUJO PRINCIPAL ---- #
if __name__ == "__main__":

    # Try-except para manejo de excepciones.
    try:      
        #Hacer una request y solicitar un ID.
        response:requests.Response = requests.get(url="http://localhost:9000/chat/init")
        
        # Comprueba el estado de la sesión.
        if response.status_code != 200:
            raise Exception("No se pudo obtener un ID de sesión por parte del servidor.")   # Lanza una excepción.
    
        SESSION_ID = Response.model_validate_json(response.content).session_id      # Obtiene el ID recibido.
        print(f"Sesión iniciada | ID: {SESSION_ID}")            # Imprime información.
        
        # Bucle infinito para el chat.
        while True:
            # Obtiene el input del usuario.
            user_input:str = input("🧠: ")
            # Genera la query.
            query:Query = Query(session_id=SESSION_ID, content=user_input)
            
            # Realiza la petición al servidor.
            with yaspin(text="Generando respuesta ...") as sp:
                response:requests.Response = requests.post(url="http://localhost:9000/chat/ask", json=query.__dict__)
            
            # Comrpueba que larespuesta haya sido correcta.
            if response.status_code != 200:
                print(f"🔶: Problema en POST | STATUS: {response.status_code}")       # Imprime el error.
                continue        # Pasa a la siguiente iteración del búcle.
            
            # Imprime la respuesta obtenida.
            resp:Response = Response.model_validate_json(response.content)    # Obtiene los datos.
            print(f"🤖: {resp.content}")        # Imprime la respuesta. 

    # Si se detecta un Ctrl+C.
    except KeyboardInterrupt:
        print()
        print("🔶: Ctrl+C detectado. Finalizando cliente.")
    # Si se detecta alguna excepción.
    except Exception as e:
        print(f"🔶: {e}")