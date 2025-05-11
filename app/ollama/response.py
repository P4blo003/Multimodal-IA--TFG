
# ---- Módulos ---- #
from .classes import Response

# ---- Funciones ----
def process_response(reply) -> Response:
    """
    Procesa la respuesta del modelo de Ollama y la formatea para su uso.
    
    Args:
        reply (str): Respuesta del modelo.
    """
    ns_to_s = lambda ns: round(ns / 1e9, 3)  # Convierte nanosegundos a segundos.
    
    response:Response = Response()          # Inicializa el objeto a devolver.
    
    # Establece los parámetros.
    response.model = reply.get("model")
    response.response = reply.get("response")
    response.tokens_prompt = reply.get("prompt_eval_count")
    response.generated_tokens = reply.get("eval_count")
    response.total_time = ns_to_s(reply.get("total_duration", 0))
    response.load_model_time = ns_to_s(reply.get("load_duration", 0))
    response.eval_prompt_time = ns_to_s(reply.get("prompt_eval_duration", 0))
    response.generation_time = ns_to_s(reply.get("eval_duration", 0))
    # Retorna la respuesta formateada.
    return response