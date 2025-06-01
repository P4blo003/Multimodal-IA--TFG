

# ---- MÓDULOS ---- #
import json
from model.response import Response

import requests

from utils.math import ns_to_sec

from config.context import CFG


# ---- CLASES ---- #
class OllamaService:
    """
    Clase encargada de aportar todas las funcionalidades de Ollama.
    """
    # -- Métodos estáticos -- #
    @staticmethod
    def get_response(prompt:str) -> Response:
        """
        Envía el prompt al modelo de Ollama y devuelve la respuesta generada.
        
        Args:
            promt (str): El prompt a enviar al modelo.
        Returns:
            Response: La respuesta generada por el modelo.
        """
        # Respuesta a devolver.
        resp:Response = Response(content="")
        
        # Crea la URL completa.
        url:str = f"http://{CFG.ollama.host}:{CFG.ollama.port}/api/generate"
        
        # Genera los campos de la consulta.
        headers:dict = {'Content-Type':'application/json'}      # Cabeceras de la consulta.
        data:dict = {
            'model':CFG.model.name,
            'prompt':prompt,
            'stream': False
        }
        
        # Obtiene la respuesta del modelo.
        response:requests.Response = requests.post(url=url, headers=headers, data=json.dumps(data))     # Envía la petición.
        
        # Comprueba el estado de la respuesta.
        if response.status_code != 200:
            return
        
        # Obtiene los datos.
        text:str = response.text
        data:dict = json.loads(text)
        # Procesa los datos obtenidos y los alamcena en la respuesta.
        resp.content = str(data['response']).strip()
        resp.loadDuration = ns_to_sec(ns=data['load_duration'])
        resp.promptEvalDuration = ns_to_sec(ns=data['prompt_eval_duration'])
        resp.responseGenDuration = ns_to_sec(ns=data['eval_duration'])
        resp.promptTokens = data['prompt_eval_count']
        resp.responseTokens = data['eval_count']
        resp.speed = resp.responseTokens / resp.responseGenDuration
        
        # Devuelve la respueta generada.
        return resp