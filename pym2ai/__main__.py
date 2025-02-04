# Modulos
import json
import os
import hashlib

from huggingface_hub import snapshot_download

from pym2ai.exceptions import InvalidModel

from .config import __MODELS_DIRECTORY__, __MODELS_SCHEMA__
# ----


class PyM2Ai:

    def __init__(self):
        """
        Constructor de la clase. Inicializa las propiedades por defecto.
        """
        self.__modelsDirectory = os.path.join(os.path.expanduser("~"), __MODELS_DIRECTORY__)
        self.__modelsSchema = os.path.join(self.__modelsDirectory, __MODELS_SCHEMA__)

        self.__installedModels = None

        # Si el directorio no existe, lo crea.
        if not os.path.exists(self.__modelsDirectory):
            os.mkdir(self.__modelsDirectory)

        if not os.path.exists(self.__modelsSchema):

            datos = {"models":[]}
            # Guardar los datos en un archivo JSON
            with open(self.__modelsSchema, "w", encoding="utf-8") as file:
                json.dump(datos, file, indent=4, ensure_ascii=False)

    # ---- Propiedades

    @property
    def installedModels(self) -> dict:
        
        if not self.__installedModels:
            self.__load_models()
        
        return self.__installedModels
    
    # ---- Funciones Auxiliares

    def __load_models(self):
        """
        Carga los modelos desde el archivo json.
        """
        # Cargar el archivo JSON
        with open(self.__modelsSchema, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        self.__installedModels = {}

        for id, model in datos["models"].items():
            self.__installedModels[id] = model
            
    
    # ---- Funciones

    def Reload(self) -> dict:
        """
        Recarga los modelos del archivo.
        """
        self.__load_models() 
        return self.__installedModels
    
    def InstallModel(self, model:str) -> dict:

        dirPath = os.path.join(self.__modelsDirectory,model)

        # Si no existe el directorio, lo crea.
        if not os.path.exists(dirPath):
            os.makedirs(dirPath, exist_ok=True)

        try:
            snapshot_download(repo_id=model, local_dir=dirPath)     # Download the model.
            print("\n\n")   # Salto de línea.
        except Exception as ex:
            os.rmdir(dirPath)   # Elimina el directorio.
            raise InvalidModel(ex) # Finaliza la función.
        
        id = hashlib.sha256(model.encode()).hexdigest()[:16]
        name = model

        self.__installedModels[id] = name

        datos = {"models":self.__installedModels}
        # Guardar los datos en un archivo JSON
        with open(self.__modelsSchema, "w", encoding="utf-8") as file:
            json.dump(datos, file, indent=4, ensure_ascii=False)
