

# ---- MÓDULOS ---- #
from .base import LAMBackend

# ---- CLASES ---- #
class HaystackBackend(LAMBackend):
    """
    Esta clase representa el backend de haystack. Implementa las funciones necesarias para
    hacer consultas al modelo empleando haystack.
    """
    # -- Métodos por defecto -- #
    def __init__(self):
        """
        Inicializa la clase.
        """
        super().__init__()  # Constructor de LAMBackend.
        # Inicializa los parámetros.
        
        self.Logger.info("Backend iniciado. TYPE: Haystack")   # Imprime información.
        