# Modules
from colorama import Fore
# ----


def PrintMessage(message:str, label:str, type:int=0):
    """
    Imprime un mensaje por consola.
    """
    color = Fore.WHITE

    if type == 1:
        color = Fore.RED
    elif type == 2:
        color = Fore.CYAN
    elif type == 3:
        color = Fore.YELLOW
    elif type == 4:
        color = Fore.GREEN
    
    print(f"[{color}{label}{Fore.RESET}]: {message}.")
