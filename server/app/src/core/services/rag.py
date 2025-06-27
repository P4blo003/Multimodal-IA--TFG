# -*- coding: utf-8 -*-


"""
*******************************************************************************************
    Nombre del Módulo: rag.py
    Proyecto: Multimodal-IA-TFG
    Autor: Pablo González García
    Fecha: 2025-06-16
    Descripción: Contiene clases y funciones relacionadas con el RAG. 
    Copyright (c) 2025 Pablo González García
    Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
*******************************************************************************************
"""


# ---- MÓDULOS ---- #
# Librerías estándar
import os
import time
from contextlib import redirect_stdout, redirect_stderr
from typing import List
from pathlib import Path
# Librerías externas

# Librerías internas
import context.singleton as CtxSingleton
from context.context_manager import ContextManager
from model.context import ContextDTO
from model.measure import RagModelDataDTO
from core.rag.document.base import BaseDocumentModule
from core.rag.document.haystack_module import HaystackDocumentModule
from core.rag.document.langchain_module import LangChainDocumentModule
from utils import hugging_face
from utils import console
from utils.file.csv import save_in_csv
from config.schema.common import EmbeddingModelConfig
from config.schema.rag import RagConfig


# ---- FUNCIONES ---- #
def create_document_module(ctx:ContextManager) -> BaseDocumentModule:
    """
    Creal el módulo de RAG de documentos en función del framework empleado.
    
    Args:
        ctx (ContextController): Gestor del contexto. Para obtener la configuración.
    Raises:
        OSError: En caso de que haya algún error.
    Returns:
        BaseDocumentModule: Módulo de RAG de documentos.
    """
    # Try-Except para manejo de errores.
    try:
        # Obtiene la configuración para facilitar el acceso.
        cfg:RagConfig = ctx.get_cfg(key='rag', t=RagConfig)
        
        # Comprueba el framwork empleado.
        match (cfg.document.framework):
            # Si es haystack.
            case 'HAYSTACK':
                # Retorna el módulo implementado con Haystack.
                return HaystackDocumentModule(rag_cfg=cfg)
            
            # Si es langchain.
            case 'LANGCHAIN':
                # Retorna el módulo implementado con LangChain.
                return LangChainDocumentModule(rag_cfg=cfg)

        # Si es un framework desconocido, lanza un aexcepción.
        raise ValueError(f"El framework <{cfg.document.framework}> no se reconoce.")

    # Si ocurre algún error.
    except Exception as e:
        # Lanza una excepción.
        raise OSError(f"rag::create_document_module() -> [{type(e).__name__}] No se pudo crear el módulo de RAG de documentos. Trace: {e}")


# ---- CLASES ---- #
class RagService:
    """
    
    """
    # -- Métodos por defecto -- #
    def __init__(self, rag_cfg:RagConfig):
        """
        Inicializa la instancia.
        
        Args:
            rag_cfg (RagConfig): Configuración del RAG.
        """
        # Inicializa las propiedades.
        self.__installModelDir:Path = Path(os.path.join('.server', rag_cfg.installModelDir))
        self.__model:EmbeddingModelConfig = rag_cfg.model
        
        
        if not self.is_model_installed(model_tag=self.__model):
            # Imprime el aviso.
            console.print_message(f"Modelo {self.__model} no instalado. Instalando ...", type=console.MessageType.WARNING)
            # Instala el modelo.
            self.install_model(model_tag=self.__model)
        
        # Imprime la información.
        console.print_message(f"Modelo {self.__model} no instalado. Instalando ...", type=console.MessageType.INFO)
        
        self.__documentRagModule:BaseDocumentModule = create_document_module(ctx=CtxSingleton.get_ctx())
        self.__measureFilePath:Path = Path(os.path.join('.server', 'etc', 'measure', f"{self.__model.tag.replace('/', '_')}.csv"))
    
    # -- Propiedades -- #
    @property
    def Model(self) -> EmbeddingModelConfig:
        """
        Retorna la configuración del modelo de embeddings.
        
        Returns:
            EmbeddingModelConfig: Configuración del modelo de embeddings.
        """
        # Retorna la configuración del modelo.
        return self.__model

    # -- Métodos públicos -- #
    def is_model_installed(self, model_tag:str) -> bool:
        """
        Comprueba si el modelo esta instalado en el sistema.
        
        Args:
            model_tag (str): Etiqueta del modelo.
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            bool: True si el modelo está instalado y False en otro caso.
        """
        # Try-Except para manejo de errores.
        try:
            # Lista las carpetas del directorio base.
            installed_models:List[str] = hugging_face.list_installed_models(root_path=self.__installModelDir)
            
            # Retorna si hay alguna coincidencia.
            return any(model_tag == model for model in installed_models)

        # Si ocurre algún error.
        except Exception as e:
                #Lanza una excepción.
                raise OSError(f"RagService.is_model_installed() -> [{type(e).__name__}] No se pudo comprobar si el modelo esta instalado. Trace: {e}")
    
    def install_model(self, model_tag:str):
        """
        Instala el modelo desde hugging face en un directorio local.
        
        Args:
            model_tag (str): Etiqueta del modelo.
        Raises:
            OSError: En caso de que haya algún error.
        """
        # Try-Except para manejo de errores.
        try:
            # Instala el modelo de manera silenciosa.
            with open(os.devnull, 'w') as devnull:
                with redirect_stdout(devnull), redirect_stderr(devnull):
                    hugging_face.install_model(model_tag=model_tag, local_dir=self.__installModelDir)
            
        # Si ocurre algún error.
        except Exception as e:
                #Lanza una excepción.
                raise OSError(f"RagService.install_model() -> [{type(e).__name__}] No se pudo instalar el modelo. Trace: {e}")
            
    def make_embeddings(self) -> None:
        """
        Calcula los embeddings.
        
        Raises:
            OSError: En caso de que haya algún error.
        """
        # Try-Except para manejo de errores.
        try:  
            # Obtiene el tiempo inicial.
            start:float = time.perf_counter()
            # Calcula los embeddings.
            self.__documentRagModule.make_embeddings()
            # Obtiene la duración.
            duration:float = time.perf_counter() - start
            
            # Almacena los parámetros obtenidos.
            ragModelData:RagModelDataDTO = RagModelDataDTO(
                action='EMBEDDING',
                duration=duration
            )
            # Almacena el dato en un csv.
            save_in_csv(file_path=self.__measureFilePath, data=ragModelData)
        
        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"RagService.make_embeddings() -> [{(type(e).__name__)}] No se pudieron calcular los embeddings. Trace: {e}")
    
    def get_relevant_context(self, query:str) -> List[ContextDTO]:
        """
        Obtiene el contexto relevante de los datos locales.
        
        Args:
            query (str): Consulta del usuario. Empleada para obtener el contexto.
        Raises:
            OSError: En caso de que haya algún error.
        Returns:
            List[ContextDTO]: Listado con el contexto obtenido.
        """
        # Try-Except para el manejo de excepciones.
        try:
            # Variable a retornar.
            context:List[ContextDTO] = []
            
            # Obtiene el tiempo inicial.
            start:float = time.perf_counter()
            # Obtiene el contexto relevante de documentos.
            context.extend(self.__documentRagModule.get_context(query=query))
            # Obtiene la duración.
            duration:float = time.perf_counter() - start
            
            # Almacena los parámetros obtenidos.
            ragModelData:RagModelDataDTO = RagModelDataDTO(
                action='RETRIEVE',
                duration=duration
            )
            # Almacena el dato en un csv.
            save_in_csv(file_path=self.__measureFilePath, data=ragModelData)
            
            # Retorna el contexto.
            return context

        # Si ocurre algún error.
        except Exception as e:
            # Lanza una excepción.
            raise OSError(f"RagService.get_relevant_context() -> [{type(e).__name__}] No se pudo obtener el contexto. Trace: {e}")