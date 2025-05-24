

# ---- MÓDULOS ---- #
import os

from haystack.components.builders import PromptBuilder


# ---- FUNCIONES ---- #
def create_prompt_builder(file_path:str, variables:list[str]) -> any:
    """
    Crea y configura un prompt builder en función del fichero con el template.
    
    Args:
        file_path (str): Ruta al fichero del template.
        variables (list[str]): Lista con las variables que espera el prompt builder.
    
    Raises:
        FileNotFoundError: Si no se encuentra el fichero del template.
        
    Returns:
        PromptBuilder: Prompt builder configurado.
    """
    # Comprueba si el fichero existe.
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El fichero no existe. PATH: {file_path}")
    
    # Si el fichero si existe.
    with open("config/prompt.template.txt", "r", encoding="utf-8") as file:
            __template = file.read()
    
    # Devuelve el prompt builder.
    return PromptBuilder(template=__template, required_variables=variables)
    