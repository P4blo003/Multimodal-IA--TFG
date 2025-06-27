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
echo -e "INFO - Clonando directorio de GitHub [$GIT_URL] ..."
git clone "$GIT_URL" "$TEMP_DIR" > /dev/null 2>&1 || exit 1
echo -e "OK - Directorio clonado."

# Copia el contenido de la carpeta servidor.
echo "INFO - Copiando ficheros en $WORK_DIR ..."
cp -r "$TEMP_DIR/server/." "$WORK_DIR/"

# Crea las carpetas necesarias.
echo "INFO - Generando directorios ..."
mkdir "$WORK_DIR/.server/data"
mkdir "$WORK_DIR/.server/data/chat"
mkdir "$WORK_DIR/.server/data/raw"
mkdir "$WORK_DIR/.server/rag"
mkdir "$WORK_DIR/.server/rag/models"
mkdir "$WORK_DIR/.server/rag/storage"
mkdir "$WORK_DIR/app/third-party/ollama/bin"
mkdir "$WORK_DIR/app/third-party/ollama/bin/ollama"

# Instala el binario de Ollama.
echo -e "INFO - Descargando binario de Ollama ..."
VERSION=$(curl -s https://api.github.com/repos/ollama/ollama/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")') > /dev/null 2>&1 || exit 1
curl -LO "https://github.com/ollama/ollama/releases/download/${VERSION}/ollama-linux-amd64.tgz" > /dev/null 2>&1 || exit 1
tar -xzf ollama-linux-amd64.tgz -C "$WORK_DIR/app/third-party/ollama/bin/ollama"
rm ollama-linux-amd64.tgz
echo -e "OK - Binario descargado."

# Genera ficheros por defecto.
echo "INFO - Generando ficheros ..."
cp "$WORK_DIR/app/third-party/ollama/.example.env" "$WORK_DIR/app/third-party/ollama/.env"
rm "$WORK_DIR/app/third-party/ollama/.example.env"
cp "$WORK_DIR/.example.env" "$WORK_DIR/.env"
rm "$WORK_DIR/.example.env"

# Genera el entorno de ejecución del servidor.
echo "INFO - Creando entorno ..."
cd "$WORK_DIR"
python3 -m venv venv || exit 1
source venv/bin/activate || exit 1
echo -e "INFO - Instalando librerías Python desde [dependencies/python_3.12.3/requirements.txt] ..."
pip install -r "dependencies/requirements.txt" || exit 1
echo -e "OK - Librerías instaladas."
deactivate

# Limpia el directorio temporal.
rm -rf "$TEMP_DIR"