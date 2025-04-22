# ---- Clases ---- #
class LocalModel():
    
    # -- Métodos por defecto -- #
    def __init__(self, model_id:str, keepCache:bool=False):
        """
        Constructor parametrizado. Inicializa las propiedades.
        
        :param str model_id:
            ID del modelo a cargar.
        :param bool localCache:
            Si el modelo debe estar guardado en cache. Si no encuentra al modelo descargado,
            los descarga en la respectiva carpeta.
        """
        # Parámetros:
        self.__modelId:str = model_id
        self.__keepCache:bool = keepCache
    
    # -- Getters --
    @property
    def ModelId(self) -> str:
        """
        Devuelve el ID del modelo.
        """
        return self.__modelId

    @property
    def KeepCache(self) -> bool:
        """
        Devuelve el estado del cache.
        """
        return self.__keepCache