# Modules
import torch
from prettytable import PrettyTable
# ----

def List_GPUs() -> int:
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
        num_gpus = -1

    return num_gpus