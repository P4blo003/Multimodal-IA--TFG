

# ---- MÓDULOS ---- #
import os
import io
from contextlib import redirect_stderr, redirect_stdout

from huggingface_hub import snapshot_download


# ---- FUNCIONES ---- #
def get_real_name(hugging_name:str) -> str:
    """
    Obtiene el nombre real del modelo. Esta función ayuda a procesar los nombres de los
    modelos de hugging face, ya que vienen de la forma `sentence-transformer/nombre`
    
    Args:
        hugging_name (str): El nombre del modelo obtenido de hugging face.
    
    Returns:
        str: El nombre real del modelo.
    """
    # Separa el nombre por el caracter '/'.
    values:list = hugging_name.split("/")
    return values[len(values)-1]    # Retorna el último elemento.

def install_model(model:str, dir:str, silent:bool=False) -> bool:
    """
    Instala el modelo en local.
    
    Args:
        model (str): Nombre completo del modelo a instalar.
        dir (str): Directorio donde se almacenan los modelos.
        silent (bool): Si la salida debe ser silenciosa.

    Returns:
        bool: True si el modelo se ha instalado y false en otro caso.
    """
    # Genera el path.
    path:str = os.path.join(dir, model)
    # Si la salida debe ser silenciosa.
    if silent:
        fnull = io.StringIO()
        with redirect_stdout(fnull), redirect_stderr(fnull):
            # Instala el modelo.
            path = snapshot_download(repo_id=model, cache_dir=path)
    # Si la salida no debe ser silenciosa.
    else:
        # Instala el modelo.
            path = snapshot_download(repo_id=model, cache_dir=path)
    # Comprueba que se ha instalado el modelo.
    if os.path.exists(path=path):
        return True
    # Devuelve falso en caso de que no exista.
    return False
    
    