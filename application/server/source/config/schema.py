# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: server/source/config/schema.py
# Autor: Pablo González García
# Descripción:
# Módulo que define el esquema de validación de la configuración principal
# del asistente. Permite garantizar que el archivo `settings.yaml` cumple
# con los requisitos esperados en cuanto a tipos, formato y restricciones.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from pydantic import BaseModel
from typing import List
from pydantic import Field


# ---- CLASES ---- #
class SystemConfig(BaseModel):
    """
    Clase que almacena la configuración del sistema.
    
    Attributes:
        logDir (str): Directorio de almacenamiento de logs.
    """
    # -- Atributes -- #
    logDir:str


class LoggerConfig(BaseModel):
    """
    Almacena la configuración del logger de la aplicación.
    
    Attributes:
        level (str): Indica el nivel mínimo de severidad de los mensajes que serán registrados.
        format (str): Formato de los mensajes del log.
        datefmt (str): Formato de la fecha de los mensajes del log.
        maxBytes (int): Tamaño máximo en bytes del fichero log.
        backupCount (int): Controla cuántos archivos de respaldo se conservan al hacer rotación de logs.
        logDir (str): Directorio de logs.
    """
    # -- Atributos -- #
    level:str           = Field(default='INFO', pattern="DEBUG|INFO|WARNING|ERROR|CRITICAL")
    format:str          = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    datefmt:str         = '%Y-%m-%d %H:%M:%S'
    maxBytes:int        = 10 * 1024 * 1024          # 10MB.
    backupCount:int     = 5
    logDir:str          = 'logs'
    

class UvicornConfig(BaseModel):
    """
    Clase que almacena la configuración de uvicorn.
    
    Attributes:
        host (str): Host en el que se ejectua el servicio de uvicorn.
        port (int): Puerto en el que se ejecuta el servicio de uvicorn.
        reload (bool): True si se desea que cuando se modifique algun script, se
            reinicie el servicio uvicorn.
        logLevel (str): El nivel mínimo del log de uvicorn.
    """
    # -- Atributos -- #
    host:str
    port:int
    reload:bool
    logLevel:str = Field(default='INFO', pattern='DEBUG|INFO|WARNING|ERROR|CRITICAL')


class OllamaAPIModelConfig(BaseModel):
    """
    Clase que almacena la configuración del modelo empleado por la API de Ollama.
    
    Attributes:
        name (str): El nombre del modelo.
        temperature (float): Parámetro que controla la aleatoriedad de las respuestas.
    """
    # -- Atributos -- #
    name:str
    temperature:float
    

class OllamaAPIConfig(BaseModel):
    """
    Clase que almacena la configuración de la API de Ollama.
    
    Attributes:
        host (str): Host en el que se ejecuta la API de Ollama.
        port (int): Puerto en el que se ejecuta la API de Ollama.
        silent (bool): Si la salida de la API de Ollama debe ser silenciosa.
        startupWaitSeconds (int): Tiempo de espera hasta que la API se inicie.
        logFile (str): Fichero de salida de la API de Ollama.
        model (OllamaAPIModeloConfig): Configuración del modelo de la API de Ollama.
    """
    # -- Atributos -- #
    host:str
    port:int
    silent:bool
    startupWaitSeconds:int
    logFile:str
    model:OllamaAPIModelConfig
    

class OllamaConfig(BaseModel):
    """
    Clase que almacena la configuración de Ollama.
    
    Attributes:
        exe (str): Ruta al fichero binario de Ollama.
        api (OllamaAPIConfig): Configuración de la API de Ollama.
    """
    # -- Atributos -- #
    exe:str
    api:OllamaAPIConfig


class ChatConfig(BaseModel):
    """
    Clase que almacena la configuración del chat.
    
    Attributes:
        maxHistorySize (int): Tamaño máximo del historial del chat.
    """
    # -- Atributos -- #
    maxHistorySize:int


class EmbedderConfig(BaseModel):
    """
    Clase que almacena la configuración del embedder.
    
    Attributes:
        name (str): Nombre del modelo de embeddings.
        persistDir (str): Directorio de almacenamiento de modelos.
    """
    # -- Atributos -- #
    name:str
    persistDir:str


class RagConfig(BaseModel):
    """
    Clase que almacena la configuración del RAG.
    
    Attributes:
        backend (str): El backend empleado.
        dataDir (str): Directorio de donde obtener los datos.
        persistDir (str): Directorio de persistencia de los embeddings.
        storeName (str): Nombre para los almacenes.
        splitLength (int): Tamaño del chunk en tokens.
        splitOverlap (int): Overlap para mantener contexto entre chunks.
        topK (int): El número de chunks más relvantes.
        embeddingDim (int): Tamaño del embedding.
        embedder (EmbedderConfig): Configuración del modelo de embedding.
    """
    # -- Atributos -- #
    backend:str = Field(default='HAYSTACK', pattern='HAYSTACK|LANGCHAIN')
    dataDir:str
    persistDir:str
    storeName:str
    splitLength:int
    splitOverlap:int
    topK:int
    embeddingDim:int
    embedder:EmbedderConfig


class PromptConfig(BaseModel):
    """
    Clase que almacena la configuración del prompt.
    
    Attributes:
        templateFile (str): Fichero con el template del prompt.
        variables (List[str]): Variables que espera el prompt.
    """
    # -- Atributos -- #
    templateFile:str
    variables:List[str]
    
    
class ServerConfig(BaseModel):
    """
    Esquema completo del archivo de configuración.
    
    Attributes:
        system (SystemConfig): Configuración del sistema.
        logger (LoggerConfig): Configuración del logger.
        uvicorn (UvicornConfig): Configuración del servicio de uvicorn.
        ollama (OllamaConfig): Configuración de Ollama.
        chat (ChatConfig): Configuración del chat.
        rag (RagConfig): Configuración del RAG.
        prompt (PromptConfig): Configuración del prompt.
    """
    # -- Atributos -- #
    system:SystemConfig
    logger:LoggerConfig
    uvicorn:UvicornConfig
    ollama:OllamaConfig
    chat:ChatConfig
    rag:RagConfig
    prompt:PromptConfig