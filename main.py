# Modules
import warnings
warnings.filterwarnings("ignore")
import datetime

from pym2ai import PrintMessage

# -------

# Main
if __name__ == "__main__":

    # Imprime cierta información de la ejecución.
    print() # Para dejar un espacio en la consola.
    PrintMessage(f"Running program. Init: {datetime.datetime.now()}","INFO",1)
    # ----
    
    
    # Imprime el final del programa.
    PrintMessage(f"End of program. Finish: {datetime.datetime.now()}","INFO",1)
    print()
# ----