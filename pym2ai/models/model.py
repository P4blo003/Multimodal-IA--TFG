# Modulos
# ----

# Clases
class Model:
    
    def __init__(self, modelVersion:str):
        """
        Constructor de la clase.

        :param str modelVersion:
            Versión del modelo.
        """
        self.modelVersion = modelVersion
        
    def __repr__(self):
        """
        Devuelve el formato string del objeto.
        """
        return f"Model: {self.modelVersion}"     

    @property
    def model_version(self):
        """
        Retorna la versión del modelo.
        """
        return self.modelVersion
# ----