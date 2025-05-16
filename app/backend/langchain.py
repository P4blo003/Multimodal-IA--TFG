

# ---- MÓDULOS ---- #
from .base import LAMBackend


# ---- CLASES ---- #
class LangChainBackend(LAMBackend):
    """
    Esta clase representa el backend de langChain. Implementa las funciones necesarias para
    hacer consultas al modelo empleando langChain.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la clase.
        """
        super().__init__()  # Constructor de LAMBackend.
        # Inicializa los parámetros.
        
        self.Logger.info("Backend iniciado. TYPE: LangChain")   # Imprime información.
        
    
    # -- Métodos públicos -- #