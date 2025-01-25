# Modules
import torch
import tensorflow as tw
# -------

def List_GPUs(module:str='TORCH'):
    """
    Imprime la lista de GPUs CUDA disponibles.

    :param str module:
        Nombre del módulo a usar. Los disponibles son:

            - TORCH.
            - TENSORFLOW.
    """

    if module.upper() == 'TORCH':
        print(f"Lista de GPUs CUDA: {torch.cuda.device_count()}")
        for index in range(torch.cuda.device_count()):
            print(f"{index}) {torch.cuda.get_device_name(index)}")
    elif module.upper() == "TENSORFLOW":
        gpus = tw.config.list_physical_devices('GPU')
        print(f"Lista de GPUs CUDA: {len(gpus)}")
        for index, device in enumerate(gpus):
            print(f"{index}) {device.name}")
