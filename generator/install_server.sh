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
FOLDERS=("application/server" "data" "dependencies" "config")
BASE_DIR="server"


# ---- FLUJO PRINCIPAL ---- #

# Genera un directorio temporal.
TEMP_DIR=$(mktemp -d "$HOME/server.temp")

# Clona el repositorio con sparse checkout.
git clone "$GIT_URL" "$TEMP_DIR"

# Copia las carpetas seleccionadas al directorio base.
for folder in ""; do
    # Copia el directorio.
    cp -r "$folder" "$HOME/$BASE_DIR" || exit 1
    echo "Carpeta [$folder] creada."
done

# Limpia el directorio temporal.
cd "$HOME" || exit 1
rm -rf "$TEMP_DIR"

# Imprime información.
echo "Servidor preparado para la ejecución."