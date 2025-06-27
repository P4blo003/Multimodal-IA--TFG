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
echo -e "INFO\t - Clonando directorio de GitHub [$GIT_URL] ..."
git clone "$GIT_URL" "$TEMP_DIR" > /dev/null 2>&1 || exit 1
echo -e "OK\t - Directorio clonado."

# Copia el contenido de la carpeta servidor.
echo "Copiando ficheros en $WORK_DIR ..."
cp -r "$TEMP_DIR/server/." "$WORK_DIR/"

# Crea las carpetas necesarias.
echo "INFO\t - Generando directorios ..."
mkdir "$WORK_DIR/.server/data"
mkdir "$WORK_DIR/.server/data/chat"
mkdir "$WORK_DIR/.server/data/raw"
mkdir "$WORK_DIR/.server/rag"
mkdir "$WORK_DIR/.server/rag/models"
mkdir "$WORK_DIR/.server/rag/storage"
mkdir "$WORK_DIR/app/third-party/ollama/bin"
mkdir "$WORK_DIR/app/third-party/ollama/bin/ollama"

# Instala el binario de Ollama.
echo -e "INFO\t - Descargando binario de Ollama ..."
VERSION=$(curl -s https://api.github.com/repos/ollama/ollama/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")') > /dev/null 2>&1 || exit 1
curl -LO "https://github.com/ollama/ollama/releases/download/${VERSION}/ollama-linux-amd64.tgz" > /dev/null 2>&1 || exit 1
tar -xzf ollama-linux-amd64.tgz -C "$WORK_DIR/app/third-party/ollama/bin/ollama"
rm ollama-linux-amd64.tgz
echo -e "OK\t - Binario descargado."

# Genera ficheros por defecto.
echo "INFO\t - Generando ficheros ..."
cp "$WORK_DIR/app/third-party/ollama/.example.env" "$WORK_DIR/app/third-party/ollama/.env"
cp "$WORK_DIR/.example.env" "$WORK_DIR/.env"

# Limpia el directorio temporal.
rm -rf "$TEMP_DIR"