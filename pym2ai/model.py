# Modlos
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
# ----


class Model:

    def __init__(self, modelPath:str):
        """
        Constructor de la clase. Inicializa las propiedades por defecto.
        
        :param str modelPath:
            Ruta al directorio con los archivos del modelo.
        """
        self.__modelPath = modelPath

        self.__tokenizer = AutoTokenizer.from_pretrained(self.__modelPath)
        self.__model = AutoModelForCausalLM.from_pretrained(self.__modelPath, torch_dtype=torch.float16, device_map="auto")


    def Chat(self, prompt:str, max_length = 1024) -> str:
        """
        Envía un prompt al modelo y devuelve la respesta del mismo.

        :param str prompt:
            Prompt del usuario.
        :param int max_length:
            Máxima longitud de la respuesta.
        """
        inputs = self.__tokenizer(prompt, return_tensors="pt").to("cuda")
        output = self.__model.generate(**inputs, max_length=max_length, pad_token_id=self.__tokenizer.eos_token_id)
        response = self.__tokenizer.decode(output[0], skip_special_tokens=True)
        return response