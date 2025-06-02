# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/server/src/config/schema.py
# Autor: Pablo González García
# Descripción:
# Módulo que define el esquema de validación de la configuración principal
# del asistente. Permite garantizar que el archivo `settings.yaml` cumple
# con los requisitos esperados en cuanto a tipos, formato y restricciones.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from pydantic import BaseModel, Field


# ---- CLASES ---- #
class UvicornConfig(BaseModel):
    """
    Almacena la configuración de uvicorn.
    
    Attributes:
        host (str): Host de uvicorn.
        port (int): Puerto de uvicorn.
    """
    # -- Atributos -- #
    host:str
    port:int
    

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


class OllamaConfig(BaseModel):
    """
    Almacena la configuración de ollama.
    
    Attributes:
        exe (str): Ruta del binario.
        host (str): Host del servicio ollama.
        port (int): Puerto del servicio ollama.
        silent (bool): Si se debe mostrar los mensajes del propio servicio de ollama.
        startupWaitSeconds (int): Tiempo de espera para el inicio del servicio (5 segundos).
        logFile (str): Nombre del fichero de logs de ollama.
    """
    # -- Atributes -- #
    exe:str
    host:str
    port:int
    silent:bool
    startupWaitSeconds:int
    logFile:str


class ModelConfig(BaseModel):
    """
    Almacena la configuración del modelo.
    
    Attributes:
        name (str): Nombre del modelo a utilizar.
        temperature (float): Parámetro que controla la aleatoriedad de las respuestas.
    """
    # -- Atributos -- #
    name:str
    temperature:float


class ChatConfig(BaseModel):
    """
    Almacena la configuración del chat.
    
    Attributes:
        maxHistorySize (int): Tamaño máximo del historial.
    """
    # -- Atributos -- #
    maxHistorySize:int


class EmbeddingRagConfig(BaseModel):
    """
    Almacena la configuración relacionada con el embedding del RAG.
    
    Attributes:
        model (str): Modelo de embedding.
        file (str): Fichero que registra la ubicación de los modelos de embedding.
        persistDirectory (str): Directorio de almacenamiento de modelos.
    """
    # -- Atributos -- #
    model:str
    file:str
    persistDirectory:str


class RagConfig(BaseModel):
    """
    Almacena la configuración relacionada con el RAG.
    
    Attributes:
        backend (str): El backend empleado. Puede ser HAYSTACK | LANGCHAIN
        docDirectory (str): Directorio de documentos.
        persistDirectory (str): Directorio de persisntencia de los embeddings calculados.
        splitLength (int): Tamaño del chunk en tokens/palabras. (En LangChain es similar a chunk_size).
        splitOverlap (int): Overlap para mantener contexto entre chunks. (En LangChain es similar a chunk_overlap).
        topK (int): El número de chunks más relevantes que se recuperan.
        embeddingDim (int): Dicmensión del embedding.
        embedding (EmbeddingRagConfig): Configuración específica para el embedding.
    """
    # -- Atributes -- #
    backend:str = Field(default='HAYSTACK', pattern="HAYSTACK|LANGCHAIN")
    docDirectory:str
    persistDirectory:str
    splitLength:int = Field(default=1000, ge=1, le=10000)
    splitOverlap:int = Field(default=100, ge=0, le=1000)
    topK:int = Field(default=5, ge=1, le=100)
    embeddingDim:int
    embedding:EmbeddingRagConfig


class PromptConfig(BaseModel):
    """
    Almacena la configuración relacionada con el prompt.
    
    Attributes:
        templateFile (str): Fichero con el template del prompt.
        variables (list[str]): Variables que espera el prompt.
    """
    # -- Atributes -- #
    templateFile:str
    variables:list[str]
    

class ServerConfig(BaseModel):
    """
    Esquema completo del archivo de configuración.
    
    Attributes:
        uvicorn (UvicornConfig): Configuración de uvicorn.
        logger (LoggerConfig): Configuración del logger.
        ollama (OllamaConfig): Conffiguración de Ollama.
        model (ModelConfig): Configuración del modelo.
        chat (ChatConfig): Configuración del chat.
        rag (RagConfig): Configuración del rag.
        prompt (PromptConfig): Configuración del prompt.
    """
    # -- Atributes -- #
    uvicorn:UvicornConfig
    logger:LoggerConfig
    ollama:OllamaConfig
    model:ModelConfig
    chat:ChatConfig
    rag:RagConfig
    prompt:PromptConfig