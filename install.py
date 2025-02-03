# Modules
import sys

from pym2ai.installer import Installer
from pym2ai.utilities import PrintMessage
# ----


if __name__ == "__main__":
    print()
    
    # Comprobación de argumentos
    args = sys.argv

    if len(args) != 2:
        PrintMessage(f"Mal forma de uso.","ERROR",1)
        print(f"| USO: python3 {args[0]} <nombre_modelo>")
        print("\t | nombre_modelo: Nombre del modelo para instalar.")
        print()
        exit(1)

    model = args[1]
    installer = Installer()

    try:
        installer.Install_Model(model=model)
    except Exception as ex:
        PrintMessage(f"No se pudo descargar el modelo [{model}]","ERROR",1)
        print()
        exit(1)
    
    exit(0)