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
WORK_DIR="$HOME/$BASE_DIR"
mkdir "$WORK_DIR"

# Clona el repositorio en el directorio temporal.
echo -e "INFO\tClonando directorio de GitHub [$GIT_URL] ..."
git clone "$GIT_URL" "$TEMP_DIR" > /dev/null 2>&1 || exit 1
echo -e "OK\tDirectorio clonado."

# Copia el contenido de la carpeta servidor.
echo "Copiando ficheros en $WORK_DIR ..."
cp -r "$TEMP_DIR/server/." "$WORK_DIR/"

# Instala el binario de Ollama.


# Limpia el directorio temporal.
rm -rf "$TEMP_DIR"