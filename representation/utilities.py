# ---- Modulos ----
from tabulate import tabulate
# ----

# ---- Funciones ----
def print_table(headers:list, data:list):
    """
    Imprime los datos pasados por parámetro en un formato tabla.
    
    :param list headers:
        Las cabeceras de la tabla.
    :param list data:
        Los datos de la tabla.
    """
    print(tabulate(data, headers=headers, tablefmt="grid"))
# ----