# Modules
import warnings
warnings.filterwarnings("ignore")
import datetime

from pym2ai import PrintMessage
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
    
    try:
        ds = DeepSeek(DS_R1_Distill_Qwen_1v5B)
        
    except InvalidModelVersion as ex:
        PrintMessage(ex,"ERROR",3)
    
    # Imprime el final del programa.
    PrintMessage(f"End of program. Finish: {datetime.datetime.now()}","INFO",1)
    print()
    # ---- 
# ----