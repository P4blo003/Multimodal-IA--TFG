# Modules
import torch
# -------

class GPUMngTorch:

    def __init__(self):
        pass

    @classmethod
    def Print_GPUs(self):

        if torch.cuda.is_available():
            num = torch.cuda.device_count()
            print(f"Num GPUs CUDA: {num}.")
            for index in range(num):
                print(f"\t{index}) {torch.cuda.get_device_name(index)}")
                print(f"\tTotal mem: {torch.cuda.get_device_properties(index).total_memory/10024**3}")
                print(f"\tMultiprocesamiento: {torch.cuda.get_device_properties(index).multi_processor_count}")
        else:
            print("CUDA no disponible. No se detectaron GPUs.")