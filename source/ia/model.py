# ---- Módulos ---- #
from abc import ABC, abstractmethod

from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline

# ---- Clases ---- #
class IA_Model():
    
    # -- Métodos por defecto -- #
    def __init__(self, modelId:str):
        """
        Constructor parametrizado. Inicializa las propieades con los valores
        dados.
        
        :param str modelId:
            Identificador del modelo.
        """
        # Parámetros:
        self.__modelID:str = modelId
        
        self.Initialize()   # Inicializa los parámetros.
        
    # -- Getters -- #
    @property
    def ModelId(self) -> str:
        """
        Devuelve el identificador del modelo.
        """
        return self.__modelID

    # -- Métodos abstractos -- #
    @abstractmethod
    def Initialize(self):
        """
        @Override: Inicializa los paráemtros del modelo.
        """
        pass

class LocalLLM(IA_Model):
    """
    Clase que representa un modelo de lenguaje local.
    """
    def __init__(self, modelId:str):
        """
        Constructor parametrizado. Inicializa las propieades con los valores
        dados.
        
        :param str modelId:
            Identificador del modelo.
        """
        # Properties:
        self.__tokenizer = None
        self.__model = None
        self.__generator = None
        
        # Llama al constructor de la clase padre:
        super().__init__(modelId)
    
    # -- Getters -- #
    @property
    def Toekenizer(self):
        """
        Devuelve el tokenizador del modelo.
        """
        return self.__tokenizer
    @property
    def Model(self):
        """
        Devuelve el modelo.
        """
        return self.__model
    @property
    def Generator(self):
        """
        Devuelve el pipeline del modelo.
        """
        return self.__generator
    
    # -- Métodos de AI_Model -- #
    def Initialize(self):
        """
        Inicializa los paráemtros del modelo.
        """
        self.__tokenizer = AutoTokenizer.from_pretrained(self.ModelId)
        self.__model = AutoModelForCausalLM.from_pretrained(self.ModelId,
                                                            device_map="auto",
                                                            torch_dtype="auto")
        self.__generator = pipeline("text-generation",model=self.Model, tokenizer=self.Toekenizer)
    
    # -- Métodos -- #
    def MakeQuestion(self, prompt:str):
        
        response = self.Generator(prompt, max_new_tokens=256, do_sample=True)
        return response[0]['generated_text']