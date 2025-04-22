# ---- Modulos ---- #
from dotenv import load_dotenv
import os

from typing import List

# ---- Propiedades ---- #
load_dotenv()

MODEL_CACHE_PATH:str = os.path.join(os.getcwd(), os.getenv("MODEL_CACHE_PATH"))    # Carga el directorio de cache.