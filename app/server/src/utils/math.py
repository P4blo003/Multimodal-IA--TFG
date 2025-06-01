# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: app/server/src/common/math.py
# Autor: Pablo González García
# Descripción:
# Módulo que contiene funciones relacionadas con cálculos matemáticos.
# -----------------------------------------------------------------------------


# ---- FUNCIONES ---- #
def ns_to_sec(ns:float) -> float:
    """
    Convierte el valor de nanosegundos a segundos.
    
    Args:
        ns (float): Nanosegundos.
    
    Returns:
        float: Valor en segundos.
    """
    # Devuelve el valor.
    return ns/1000000000