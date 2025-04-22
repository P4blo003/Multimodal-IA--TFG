# ---- Modulos ---- #
from dotenv import load_dotenv
import os

# ---- Propiedades ---- #
load_dotenv()

MODEL_PATH:str = os.getenv("MODEL_PATH")