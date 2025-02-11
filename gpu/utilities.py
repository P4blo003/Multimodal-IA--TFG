# ---- Modulos ----
import torch
from representation import print_table
# ----

# ---- Funciones ----
def list_gpus():
    """
    Imprime la lista de GPUs CUDA disponibles. Muestra además las propiedades
    de las mismas como la memoria total y la memoria reservada.
    """
    
    if not torch.cuda.is_available():       # Si no tiene CUDA disponible.
        print("CUDA not available.")
        return
    
    num_gpus = torch.cuda.device_count()    # Obtiene el número de gpus.
    
    # Datos de la tabla.
    headers = ['NOMBRE', 'MEM TOTAL', 'MEM ASIGNADA', 'MEM RESERVADA']
    gpus_data = []

    for index in range(num_gpus):   # Para cada GPU disponible.
        props = torch.cuda.get_device_properties(index)     # Obtiene las propeidades de la GPU.
        total_mem = props.total_memory / 1e9  # Convertir a GB
        allocated_mem = torch.cuda.memory_allocated(index) / 1e9  # Memoria asignada por PyTorch en GB
        reserved_mem = torch.cuda.memory_reserved(index) / 1e9  # Memoria reservada por PyTorch en GB
        gpus_data.append([props.name, f"{total_mem:.2f} GB", f"{allocated_mem:.2f} GB", f"{reserved_mem:.2f} GB"])
        
    print_table(headers=headers,data=gpus_data)     # Imprime la tabla.
# ----