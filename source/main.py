# ---- Modulos ---- #
from config.settings import MODEL_CACHE_PATH
from ia.model import LocalLLM

# ---- Función principal ---- #
if __name__ == "__main__":
    
    # Imprime información de ejecución:
    print("Running program ...")
    
    localLLM = LocalLLM(modelId="deepseek-ai/DeepSeek-R1-Distill-Llama-8B")
    
    print("🧠 Pregunta: ¿Quién eres?")
    response = localLLM.MakeQuestion("¿Quién eres?")
    print("🤖 Respuesta: ", response)