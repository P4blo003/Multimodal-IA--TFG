
# ---- Múdulos ---- #
import os
import subprocess

# ---- Funciones ---- #
def install_model(bin_path:str, model:str):
    """
    Instala el modelo de Ollama.
    
    Args:
        bin_path (str): Ruta al binario de Ollama.
        model (str): Nombre del modelo a instalar.
    """
    with open(os.devnull, 'w') as devnull:
        process = subprocess.run(
            [bin_path, "run", model],
            check=True,
            stdout=devnull,
            stderr=devnull
        )