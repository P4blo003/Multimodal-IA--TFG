# Modulos
from huggingface_hub import snapshot_download
import os

from pym2ai import PrintMessage
# ----

# Funciones
def InstallModel(model:str, path:str):
    """
    Descarga el modelo en el directorio.

    :param str model:
        Nombre del modelo a descargar.
    :param str path:
        Directorio donde almacenar los ficheros del modelo.
    """

    if not os.path.exists(path=path):
        return
    
    print("Downloading model ...")
    try:
        snapshot_download(repo_id=model, cache_dir=path)
        PrintMessage(f"Modelo descargado en [{path}]", "OK", 2)
    except Exception as ex:
        PrintMessage(f"No se pudo descargar el modelo {model}.", "INFO", 3)
# ----