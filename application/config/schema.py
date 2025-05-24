# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: application/config/schema.py
# Autor: Pablo González García
# Descripción:
# Módulo que define el esquema de validación de la configuración principal
# del asistente. Permite garantizar que el archivo `settings.yaml` cumple
# con los requisitos esperados en cuanto a tipos, formato y restricciones.
# -----------------------------------------------------------------------------


# ---- MÓDULOS ---- #
from pydantic import BaseModel, Field


# ---- CLASES ---- #
class SystemConfig(BaseModel):
    """
    Almacena la configuraucón del sistema.

    Attributes:
        logsDirectory (str): Directorio donde almacenar los logs de la aplicación.
    """
    # -- Atributos -- #
    logsDirectory:str


class LoggerConfig(BaseModel):
    """
    Almacena la configuración del logger de la aplicación.
    
    Attributes:
        level (str): Indica el nivel mínimo de severidad de los mensajes que serán registrados.
        format (str): Formato de los mensajes del log.
        datefmt (str): Formato de la fecha de los mensajes del log.
        maxBytes (int): Tamaño máximo en bytes del fichero log.
        backupCount (int): Controla cuántos archivos de respaldo se conservan al hacer rotación de logs.
    """
    # -- Atributos -- #
    level:str = Field(default='INFO', pattern="DEBUG|INFO|WARNING|ERROR|CRITICAL")
    format:str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    datefmt:str = '%Y-%m-%d %H:%M:%S'
    maxBytes:int = 10 * 1024 * 1024 # 10MB.
    backupCount:int = 5


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
    Almacena la configuración del modelo.
    
    Attributes:
        exitCommands (list): Lista con los comandos de salida del chat.
        maxHistorySize (int): Máximo tamaño del historial del chat.
        promptDir (str): Nombre del directorio del prompt de jinja2.
        promptFile (str): Nombre del fichero del prompt de jinja2.
    """
    # -- Atributos -- #
    exitCommands:list
    maxHistorySize:int
    promptDir:str
    promptFile:str


class RagConfig(BaseModel):
    """
    Almacena la configuración relacionada con el RAG.
    
    Attributes:
        backend (str): El backend empleado.
        splitLength (int): Tamaño del chunk en tokens/palabras.
        splitOverlap (int): Overlap para mantener contexto entre chunks.
        topK (int): El número de chunks más relevantes que se recuperan.
        docDirectory (str): Directorio de documentos.
        persistDirectory (str): Donde se almacenan los embeddings calculados.
        embeddingDim (int): Tamaño del embedding.
        embeddingModel (str): Nombre del modelo de embedding.
        embeddingModelsFile (str): Fichero que registra la ubicación de los modelos de embedding.
        embeddingModelDirectory (str): Directorio de almacenamiento de modelos.
    """
    # -- Atributes -- #
    backend:str = Field(default='HAYSTACK', pattern="HAYSTACK|LANGCHAIN")
    splitLength:int
    splitOverlap:int
    topK:int
    docDirectory:str
    persistDirectory:str
    embeddingDim:int
    embeddingModel:str
    embeddingModelsFile:str
    embeddingModelDirectory:str


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

    
class AppConfig(BaseModel):
    """
    Esquema completo del archivo de configuración.
    
    Attributes:
        system (SystemConfig): Configuración del sistema.
        logger (LoggerConfig): Configuración del logger.
        ollama (OllamaConfig): Conffiguración de Ollama.
        model (ModelConfig): Configuración del modelo.
        chat (ChatConfig): Configuración del chat.
        rag (RagConfig): Configuración del rag.
        prompt (PromptConfig): Configuración del prompt.
    """
    # -- Atributes -- #
    system:SystemConfig
    logger:LoggerConfig
    ollama:OllamaConfig
    model:ModelConfig
    chat:ChatConfig
    rag:RagConfig
    prompt:PromptConfig