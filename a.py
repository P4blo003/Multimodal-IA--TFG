# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécnica de Ingeniería de Gijón
# Archivo: src/ingestion/document_loader.py
# Descripción: Módulo para cargar, preprocesar e indexar documentos en tiempo de ejecución.
# -----------------------------------------------------------------------------

import os
from typing import List, Literal, Union
from utils.logger import get_logger

# Haystack
from haystack import Pipeline
from haystack.components.converters import MultiFileConverter
from haystack.components.preprocessors import DocumentPreprocessor
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore as HSInMemoryStore

# LangChain
from langchain.schema.document import Document as LCDocument
from langchain.document_loaders import UnstructuredFileLoader


class DocumentLoader:
    """
    Clase encargada de cargar y procesar documentos desde un directorio dado.
    Puede operar en dos modos: usando Haystack o LangChain como backend.
    Permite añadir documentos en tiempo de ejecución (notificación externa).
    """

    def __init__(self, cfg: dict, backend: Literal["haystack", "langchain"] = "haystack"):
        """
        Inicializa el cargador de documentos.

        Args:
            cfg (dict): Configuración del sistema (rutas, extensiones, etc.).
            backend (Literal): Backend deseado ('haystack' o 'langchain').
        """
        self._logger = get_logger(__name__)
        self._cfg = cfg
        self._backend = backend
        self._doc_dir = cfg.get("path", "./documents")  # Ruta base de documentos
        self._valid_exts = cfg.get("valid_extensions", [".pdf", ".docx", ".txt", ".csv", ".md"])

        if backend == "haystack":
            self._store = HSInMemoryStore()
            self._init_haystack_pipeline()
        elif backend == "langchain":
            self._store: List[LCDocument] = []
        else:
            raise ValueError(f"Backend no soportado: {backend}")

        self._logger.info(f"DocumentLoader inicializado con backend '{backend}'.")

    def _init_haystack_pipeline(self):
        """
        Inicializa el pipeline de Haystack para conversión, preprocesamiento y escritura.
        """
        self._pipeline = Pipeline()
        self._pipeline.add_component("converter", MultiFileConverter())
        self._pipeline.add_component(
            "preprocessor",
            DocumentPreprocessor(split_by="word", split_length=512, split_overlap=50)
        )
        self._pipeline.add_component("writer", DocumentWriter(document_store=self._store))

        self._pipeline.connect("converter", "preprocessor")
        self._pipeline.connect("preprocessor", "writer")

    def _get_valid_files(self, directory: str) -> List[str]:
        """
        Obtiene todos los archivos válidos desde un directorio.

        Args:
            directory (str): Ruta al directorio de documentos.

        Returns:
            List[str]: Lista de rutas de archivos válidos.
        """
        if not os.path.exists(directory):
            self._logger.warning(f"Directorio no encontrado: {directory}")
            return []

        return [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in self._valid_exts
        ]

    def _process_haystack(self, files: List[str]):
        """
        Procesa archivos usando el pipeline de Haystack.

        Args:
            files (List[str]): Lista de rutas de archivos a procesar.
        """
        if not files:
            self._logger.warning("No se encontraron archivos válidos para procesar.")
            return
        self._pipeline.run(data={"sources": files})
        self._logger.info(f"{len(files)} archivos procesados e indexados con Haystack.")

    def _process_langchain(self, files: List[str]):
        """
        Procesa archivos con LangChain cargándolos como LCDocument.

        Args:
            files (List[str]): Lista de rutas de archivos a procesar.
        """
        for path in files:
            try:
                loader = UnstructuredFileLoader(path)
                docs = loader.load()
                self._store.extend(docs)
                self._logger.info(f"{len(docs)} documentos añadidos desde {os.path.basename(path)}")
            except Exception as e:
                self._logger.error(f"Error cargando archivo {path}: {e}")

    def load_all(self):
        """
        Carga e indexa todos los documentos del directorio configurado.
        """
        self._logger.info("Iniciando carga de documentos...")
        files = self._get_valid_files(self._doc_dir)
        self._process_backend(files)

    def add_file(self, path: str):
        """
        Añade un documento individual en tiempo de ejecución.

        Args:
            path (str): Ruta absoluta o relativa al nuevo archivo.
        """
        if not os.path.exists(path):
            self._logger.error(f"Archivo no encontrado: {path}")
            return

        ext = os.path.splitext(path)[1].lower()
        if ext not in self._valid_exts:
            self._logger.warning(f"Extensión no válida: {ext}")
            return

        self._logger.info(f"Añadiendo nuevo archivo: {os.path.basename(path)}")
        self._process_backend([path])

    def _process_backend(self, files: List[str]):
        """
        Ejecuta el procesamiento en función del backend elegido.

        Args:
            files (List[str]): Lista de rutas de archivos a procesar.
        """
        if self._backend == "haystack":
            self._process_haystack(files)
        else:
            self._process_langchain(files)

    def get_store(self) -> Union[HSInMemoryStore, List[LCDocument]]:
        """
        Retorna el almacén de documentos según el backend configurado.

        Returns:
            Union[HSInMemoryStore, List[LCDocument]]: Almacén de documentos procesados.
        """
        return self._store