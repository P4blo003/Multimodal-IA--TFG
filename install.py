# ---- Modulos
import sys

from pym2ai import PyM2Ai

from pym2ai.utilities import PrintMessage
# ----

# Variables
__NUM_ARGS__ = 2
# ----

if __name__ == "__main__":

    args = sys.argv
    num_args = len(args)

    if num_args != __NUM_ARGS__:
        PrintMessage(f"BAD PROGRAM CALL", "ERROR", 1)
        print("USO: install.py <model_name>")
        exit(1)

    model = args[1]     # Obtiene el modelo.

    PrintMessage(f"DOWNLOADING [{model}] ...","INFO",2)
    pym = PyM2Ai()      # Objeto parainstalar los modelos.

    try:
        print(f"{"*"*10}")
        pym.InstallModel(model=model)   # Instala el modelo.
        print(f"{"*"*10}")
        PrintMessage(f"MODEL <{model}> INSTALLED", "OK", 4)
    except Exception as ex:
        PrintMessage(f"ERROR DOWNLOADING MODEL.", "ERROR", 1)
        print(f"{"*"*10}")
        print(ex)
        print(f"{"*"*10}")
        exit(1)