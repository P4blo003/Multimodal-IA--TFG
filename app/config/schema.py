# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/config/schema.py
# Autor: Pablo González García
# Descripción:
# Módulo que define el esquema de validación de la configuración principal
# del asistente. Permite garantizar que el archivo `settings.yaml` cumple
# con los requisitos esperados en cuanto a tipos, formato y restricciones.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from pydantic import BaseModel, Field
from typing import List


# ---- CLASES ---- #
class SystemConfig(BaseModel):
    """
    Configuración del sistema.
    
    Attributes:
        logsDirectory (str): Ruta del directorio de logs.
        cacheDirectory (str): Ruta del directorio de cache.
    """
    # -- Atributos -- #
    logsDirectory:str       # La ruta del directorio de logs.
    cacheDirectory:str      # Ruta del directorio de cache.
    
class LoggerConfig(BaseModel):
    """
    Configuración del servicio de Ollama.
    
    Attributes:
        level (str): Indica el nivel mínimo de severidad de los mensajes que serán registrados.
        format (str): Formato de los mensajes del log.
        datefmt (str): Formato de la fecha de los mensajes del log.
        maxBytes (int): Tamaño máximo en bytes del fichero log.
        backupCount (int): Controla cuántos archivos de respaldo se conservan al hacer rotación de logs.
    """
    # -- Parámetros -- #
    level:str = Field(default='INFO', pattern="DEBUG|INFO|WARNING|ERROR|CRITICAL")
    format:str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    datefmt:str = '%Y-%m-%d %H:%M:%S'
    maxBytes:int = 10 * 1024 * 1024 # 10MB.
    backupCount:int = 5

class OllamaConfig(BaseModel):
    """
    Configuración del servicio local de Ollama.
    
    Attributes:
        executablePath (str): Ruta absoluta o relativa al binario de Ollama.
        host (str): Dirección IP o nombre de host donde se ejecuta Ollama.
        port (int): Puerto del servicio HTTP.
        silent (bool): Si se deben ocultar los mensajes del servidor.
        startupWaitSeconds (int): Tiempo de espera (segundos) tras el arranque.
        logFile (str): Ruta al archivo de log específico para Ollama.
        historyMaxSize (int): Tamaño máximo del historial de conversación almacenado.
    """
    # -- Parámetros -- #
    executablePath:str
    host:str
    port:int
    silent:bool
    startupWaitSeconds:int
    logFile:str
    historyMaxSize:int

class ModelConfig(BaseModel):
    """
    Configuración del modelo utilizado por Ollama.
    
    Attributes:
        name (str): Nombre del modelo.
        temperature (float): Parámetro que controla la aleatoriedad de las respuestas.
        maxTokens (int): Máximo de tokes a generar por respuesta.
    """
    # -- Parámetros -- #
    name:str
    temperature:float
    maxTokens:int

class ChatConfig(BaseModel):
    """
    Configuración general del comportamiento del chat.
    
    Attributes:
        type (str): Tipo de chat. Valores válidos: basic, prompted, rag.
        exitCommands (List[str]): Lista de comandos permitidos para salir del chat.
    """
    # -- Parámetros -- #
    type:str = Field(pattern="basic|prompted|rag")
    exitCommands:List[str]
    
class RagConfig(BaseModel):
    """
    Configuración general del sistema RAG.
    
    Attributes:
        backend (str): El backend a emplear. Puede ser 'haystack' o 'langchain'
        docDirectory (str): Directorio donde se almacenan los documentos a comprobar.
        validExtensions (List[str]): Lista con las extensiones válidas.
        embeddingModel (str): El modelo empleado para obtener los embeddings.
        modelDirectory (str): La ruta de almacenamiento del modelo.
        logFile (str): El log del backend rag.
        modelsFile (str): Fichero para almacenar los modelos descargados.
    """
    # -- Parámetros -- #
    backend:str
    docDirectory:str
    validExtensions:List[str]
    embeddingModel:str
    modelDirectory:str
    logFile:str
    modelsFile:str

class AppConfig(BaseModel):
    """
    Esquema completo del archivo de configuración.
    
    Attributes:
        logger (LoggerConfig): Sección de configuración de logs.
        ollama (OllamaConfig): Sección de configuración del Ollama.
        model (ModelConfig): Sección de configuración del modelo.
        chat (ChatConfig): Sección de configuración del chat.
    """
    # -- Parámetros -- #
    system:SystemConfig
    logger:LoggerConfig
    ollama:OllamaConfig
    model:ModelConfig
    chat:ChatConfig
    rag:RagConfig