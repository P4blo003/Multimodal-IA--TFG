# Modules
from colorama import Fore
from prettytable import PrettyTable

import torch
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
    
def List_GPUs():
        """
        Lista las GPUs CUDA disponibles.
        """
        num_gpus = torch.cuda.device_count()

        if num_gpus > 0:
            print(f"- Num GPUs CUDA: {num_gpus}.")
            table = PrettyTable()
            table.field_names = ["GPU", "Nombre", "Memoria Total (GB)", "Memoria Utilizada (GB)", "Memoria Reservada (GB)"]
            
            for index in range(num_gpus):
                gpu_name = torch.cuda.get_device_name(index)
                total_memory = torch.cuda.get_device_properties(index).total_memory / (1024 ** 3)  # Memoria total en GB
                memory_allocated = torch.cuda.memory_allocated(index) / (1024 ** 3)  # Memoria utilizada en GB
                memory_reserved = torch.cuda.memory_reserved(index) / (1024 ** 3)  # Memoria reservada en GB
                
                table.add_row([index, gpu_name, f"{total_memory:.2f}", f"{memory_allocated:.2f}", f"{memory_reserved:.2f}"])
                
            print(table)
        else:
            print("No se encontró ninguna GPU CUDA.")