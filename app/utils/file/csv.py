

# ---- Módulos ---- #
import os
import csv

# ---- Funciones ---- #
def check_and_create_csv(file:str, headers:list[str]):
    """
    Comrpueba si un fichero CSV existe. Si no existe, lo crea y añade las cabeceras.
    
    Args:
        file (str): Nombre del fichero CSV.
        headers (list[str]): Cabeceras del CSV.
    """
    if not os.path.exists(file):                # En caso de que no exista el fichero:
        with open(file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=';')  # Crea el objeto writer para escribir en el CSV.
            writer.writeheader()                # Escribe las cabeceras en el fichero CSV.
            
def write_csv(file:str, data:dict, headers:list[str]):
    """
    Escribe los datos en un fichero CSV.
    
    Args:
        file (str): Nombre del fichero CSV.
        data (dict): Datos a escribir en el CSV.
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"El fichero {file} no existe.")

    with open(file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=';')
        writer.writerow(data)