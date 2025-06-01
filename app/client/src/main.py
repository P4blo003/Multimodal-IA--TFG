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
import json
from model.query import Query
from model.response import Response

from yaspin import yaspin

import requests


# ---- FLUJO PRINCIPAL ---- #
if __name__ == "__main__":
    
    index = 1
    try:
        with open("docs/chat.deepseekr1_8b.txt", "a", encoding="utf-8") as file:
            with open("docs/questions.txt", "r", encoding="utf-8") as qfile:
                preguntas = [line.strip() for line in qfile if line.strip()]
                
            # Bucle infinito para el chat.
            for pregunta in preguntas:
                # Crea la query para enviar al servidor.
                query:Query = Query(content=pregunta)
                
                # Obtiene la respuesta del servidor.
                with yaspin(text="Generando respuesta ...") as sp:
                    response:requests.Response = requests.post(url="http://localhost:9000/chat/ask", json=query.__dict__)  # Envía la petición.
                
                # Comrpueba que larespuesta haya sido correcta.
                if response.status_code != 200:
                    print(f"🔶: Problema en POST | STATUS: {response.status_code}")       # Imprime el error.
                    continue        # Pasa a la siguiente iteración del búcle.
                
                resp:Response = Response.model_validate_json(response.content)    # Obtiene los datos.
                print(f"🤖: {resp.content}")        # Imprime la respuesta.       
                
                file.write(f"Query: {pregunta}\n")
                file.write(f"Speed: {resp.speed} tok/s\n")
                file.write(f"Response:\n{resp.content}\n")

        
    except KeyboardInterrupt:
        print()
        print("🔶: Ctrl+C detectado. Finalizando cliente.")
    
    except Exception as e:
        print(f"🔶: {e}")