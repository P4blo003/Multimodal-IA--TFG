# Modules
import os
from huggingface_hub import snapshot_download

from pym2ai.utilities import PrintMessage
# ----


class Installer:
    """
    Esta clase ayuda a la hora de instalar las dependencias.
    """
    def __init__(self):
        """
        Constructor de la clase.
        """
        self.__filePath = f"{os.path.expanduser("~")}/ai"
    
    def Install_Model(self, model:str):
        """
        Instala el modelo en el directorio.

        :param str modelName:
            Modelo para instalar.
        """
        if not os.path.exists(self.__filePath):
            PrintMessage(f"No se ha encontrado el directorio [{self.__filePath}].\n| Creando directorio ...","WARNING",3)
            os.mkdir(self.__filePath)   # Crea el directorio.
        
        PrintMessage(f"DIR={self.__filePath} | MODEL={model} > Iniciando descarga ...","INFO",2)

        # Descargar el modelo en el directorio especificado
        snapshot_download(repo_id=model, local_dir=self.__filePath)

    def List_Models(self):
        """
        Lista los modelos instalados.
        """
        pass