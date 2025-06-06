#!/bin/bash

# -----------------------------------------------------------------------------
# MULTIMODAL-IA--TFG - Proyecto TFG
# (c) 2025 Pablo González García
# Universidad de Oviedo, Escuela Politécncia de Ingeniería de Gijón
# Archivo: generator/install_server.sh
# Autor: Pablo González García
# Descripción:
# Archivo de instalación del servidor.
# -----------------------------------------------------------------------------


# ---- VARIABLES GLOBALES ---- #
GIT_URL="https://github.com/P4blo003/Multimodal-IA--TFG.git"
FOLDERS=("application/server" "dependencies" "config")
BASE_DIR="server"


# ---- FLUJO PRINCIPAL ---- #

# Genera un directorio temporal.
TEMP_DIR=$(mktemp -d "$HOME/server.temp.XXX")
cd "$TEMP_DIR" || exit 1

# Clona el repositorio con sparse checkout.
echo -e "INFO\tClonando directorio de GitHub [$GIT_URL] ..."
git clone "$GIT_URL" "$TEMP_DIR" > /dev/null 2>&1 || exit 1
echo -e "OK\tDirectorio clonado."

# Crea el directorio donde copiar los ficheros.
mkdir "$HOME/$BASE_DIR"  || exit 1

# Copia las carpetas seleccionadas al directorio base.
for folder in "${FOLDERS[@]}"; do
    # Copia el directorio.
    cp -r "$folder" "$HOME/$BASE_DIR" || exit 1
    echo -e "OK\tCarpeta [$folder] creada en [$HOME/$BASE_DIR]"
done

# Limpia el directorio temporal.
cd "$HOME/$BASE_DIR" || exit 1
rm -rf "$TEMP_DIR"

# Genera las demás carpetas.
mkdir "bin" || exit 1
mkdir "bin/ollama" || exit 1
mkdir "data" || exit 1
mkdir "data/persistence" || exit 1
mkdir "data/raw" || exit 1
mkdir "logs" || exit 1
mkdir "resources" || exit 1

# Genera el entorno de ejecución del servidor.
python3 -m venv venv || exit 1
source venv/bin/activate || exit 1
echo -e "INFO\tInstalando librerías Python desde [dependencies/python_3.12.3/requirements.txt] ..."
pip install -r "dependencies/python_3.12.3/requirements.txt" > /dev/null 2>&1 || exit 1
echo -e "OK\tLibrerías instaladas."
deactivate

# Obtiene el binario de Ollama.
echo -e "INFO\tDescargando binario de Ollama ..."
VERSION=$(curl -s https://api.github.com/repos/ollama/ollama/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")') > /dev/null 2>&1 || exit 1
curl -LO "https://github.com/ollama/ollama/releases/download/${VERSION}/ollama-linux-amd64.tgz" > /dev/null 2>&1 || exit 1
tar -xzf ollama-linux-amd64.tgz -C "bin/ollama"
rm ollama-linux-amd64.tgz
echo -e "OK\tBinario descargado."

# Imprime información.
echo -e "OK\tServidor preparado para la ejecución."