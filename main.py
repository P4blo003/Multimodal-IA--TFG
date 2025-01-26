# Modules
import warnings
warnings.filterwarnings("ignore")

import datetime

from pym2ai import List_GPUs
# -------

# Main
if __name__ == "__main__":

    # Imprime cierta información de la ejecución.
    print() # Para dejar un espacio en la consola.
    print(f"Running program. Init: {datetime.datetime.now()}")
    # ----

    List_GPUs('tensorflow') # Liasta las GPUs CUDA.
# ----