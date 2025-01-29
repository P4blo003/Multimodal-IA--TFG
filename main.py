# Modules
import warnings
warnings.filterwarnings("ignore")
import datetime

from pym2ai import PrintMessage
from pym2ai import List_GPUs
from pym2ai import InvalidModelVersion

from pym2ai import DeepSeek
from pym2ai.models import DS_R1_Distill_Qwen_1v5B
# -------

# Main
if __name__ == "__main__":

    # Imprime cierta información de la ejecución.
    print() # Para dejar un espacio en la consola.
    PrintMessage(f"Running program. Init: {datetime.datetime.now()}","INFO",1)
    # ----    
    
    # Lista las GPUs disponibles
    gpus = List_GPUs()     # Lista las GPUs disponibles.
    # ----

    try:
        device_id = None
        while(device_id == None):  # Hasta que se introduzca una gpu válida
            try:
                device_id = int(input("> Introduce GPU: ")) # Solicita la gpu.

                if device_id < 0 or device_id >= gpus:  # Si esta fuera del rango.
                    PrintMessage(f"Invalid GPU. Given: {device_id} | Range: [0,{gpus})","WARNING",4)
                    device_id = None

            except Exception:   # Si ocurre algún error.
                device_id = None
                PrintMessage(f"Invalid input.","WARNING",4)

    except KeyboardInterrupt:   # Para Ctrl+C.
        PrintMessage(f"End of program. Finish: {datetime.datetime.now()}","INFO",1)
        print()

    # Imprime el final del programa.
    PrintMessage(f"End of program. Finish: {datetime.datetime.now()}","INFO",1)
    print()
    # ---- 
# ----