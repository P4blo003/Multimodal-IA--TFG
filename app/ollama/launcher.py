# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: src/app.py
# Autor: Pablo González García
# Descripción: 

# -----------------------------------------------------------------------------

# ---- Modulos ---- #
import os
import subprocess

from .classes import OllamaConfig

# ---- Funciones ---- #
def run_ollama(cfg:OllamaConfig) -> subprocess.Popen:
    """
    Lanza el servicio de ollama. En caso de que el valor de silent sea True,
    no se mostrarán los mensajes generados por el propio servicio.
    
    Args:
        cfg (OllamaConfig): Clase que almacena la configuración de ollama.
    
    Returns:
        Subproceso generado.
    """
    # Obtiene las variables de entorno.
    env = os.environ.copy()
    env['OLLAMA_HOST'] = f"{cfg.host}:{cfg.port}"
    # Si debe ser silencioso.
    if cfg.silent:
        with open(os.devnull, 'w') as devnull:
            process = subprocess.Popen(
                [str(cfg.bin)] + ["serve"],
                env=env,
                stdout=devnull,
                stderr=devnull)
    # Si no debe ser silencioso.
    else:
        with open(cfg.file, 'w') as file:
            process = subprocess.Popen(
                [str(cfg.bin)] + ["serve"],
                env=env,
                stdout=file,
                stderr=file)
    
    # Retorna el subproceso.
    return process