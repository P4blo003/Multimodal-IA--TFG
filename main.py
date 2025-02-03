# Modules
import warnings
warnings.filterwarnings("ignore")
import datetime
import os

from pym2ai import PrintMessage
from pym2ai.models import DS_R1_Distill_Qwen_1v5B
from pym2ai.models import InstallModel
# -------

# Variables
local_dir = os.path.join(os.path.expanduser("~"),"ai_cache")
# ----

# Main
if __name__ == "__main__":

    # Imprime cierta información de la ejecución.
    print() # Para dejar un espacio en la consola.
    PrintMessage(f"Running program. Init: {datetime.datetime.now()}","INFO",1)
    # ----    
    
    try:
        # Crea el directorio donde almacenar los modelos.
        if not os.path.exists(local_dir):
            os.mkdir(local_dir)

        InstallModel(DS_R1_Distill_Qwen_1v5B,local_dir)

    except KeyboardInterrupt:   # Para Ctrl+C.
        print()

    # Imprime el final del programa.
    PrintMessage(f"End of program. Finish: {datetime.datetime.now()}","INFO",1)
    print()
    exit(0)
    # ---- 
# ----