# Modules
from colorama import Fore

# -------

def PrintMessage(message:str,label:str,msgType:int=0):
    """
    Imprime el mensaje pasado por parámetro junto con la etiqueta
    dada con un color determinado.
    
    - :samp:`[INFO] : Esto es un ejemplo`
    
    :param str message:
        Mensaje a imprimir.
    :param str label:
        Etiqueta del mensaje a imprimir.
    :param int msgType:
        Tipo del mensaje. Representa con que color se muestra la
        etiqueta.

        - 0: White.
        - 1: Cyan.
        - 2: Green.
        - 3: Red.
    """
    
    color = None
    
    if msgType == 0:
        color=Fore.WHITE
    elif msgType == 1:
        color=Fore.CYAN
    elif msgType == 2:
        color=Fore.GREEN
    elif msgType == 3:
        color=Fore.RED
    else:
        return
    
    print(f"[{color}{label}{Fore.RESET}] {message}")