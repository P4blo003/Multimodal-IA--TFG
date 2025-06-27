#!/usr/bin/env bash

# *****************************************************************************************
#   Nombre del Shell: launch_ollama.sh
#   Proyecto: Multimodal-IA-TFG
#   Autor: Pablo González García
#   Fecha: 2025-06-16
#   Descripción: Ejecuta el binario de Ollama de manera segura.  
#   Copyright (c) 2025 Pablo González García
#   Licencia: MIT License. Ver el archivo LICENCE en la raíz del proyecto.
# *****************************************************************************************


# Activa el modo estricto y seguro. Impide que el script continue en estados incorrectos, lo que reduce
# errores difíciles de detectar y mejorar la fiabilidad.
#       -E: Garantiza que la función trap ERR se aplique también dentro de funciones, subshells y sustituciones
#           de comandos.
#       -e: Hace que el script se detenga inmediatamente si cualquier comando devuelve un exit
#           status != 0.
#       -u: Si el script usa una variable no definida, falla inmediatamente.
#           pipefail: Asegura que en un atubería, si cualquiera de los comandos falla, el pipeline considera eso como
#           fallo.
set -Eeuo pipefail

# Indica al bash cómo dividir cadenas de texto en listas de palabras. Permite manipular listas de forma más
# predecible y evita errores inesperados.
IFS=$'\n\t'

# Obtiene el directorio del script para referencias relativas.
root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)"

# Especifica la función de limpieza.
cleanup() {
    # TODO: Implementar para liberar recursos.
    :
}

# Define que la función 'cleanup' se ejecutará cuando ocurra:
#       EXIT: Al terminar el script por cualquier motivo.
#       ERR: Al detectar un fallo.
#       SIGINT: Cuando se interrumpe el proceso con Ctrl+C.
#       SIGTERM: Cuando se envía una señal de terminación.
# Garantiza que, incluso ante errores o abortos, el script limpie el entorno, exitando estados inconsistentes o residuos
# tras su ejecución.
trap cleanup EXIT ERR SIGINT SIGTERM

# Carga la configuración (.env si existe).
if [ -f "${root_dir}/.env" ]; then
    # Imprime la información.
    echo "Info: Cargando configuración desde .env ..."
    # Evita tener que escribir 'export VAR=' para cada variable individualmente.
    set -a
    # Lee y ejecuta el contenido del archivo .env.
    source "${root_dir}/.env"
    # Realizado tras 'set -a' para limitar el alcance del auto-export.
    set +a
fi

# Obtiene la IP de la variable de entorno.
IP="${1:-${OLLAMA_IP:-127.0.0.1}}"
# Obtiene el puerto de la variable de entorno.
PORT="${2:-${OLLAMA_PORT:-11434}}"

# Valida la IP.
if ! [[ "$IP" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]; then
    # Imprime el error.
    echo "Error: La IP tiene un formato incorrecto" >&2
    # Finaliza el script.
    exit 1
fi

# Comprueba si cada valor de la IP es correcto.
# Itera sobre los valores de la IP
IFS='.' read -r -a values <<< "$IP"
for value in "${values[@]}"; do
    # Comprueba el valor.
    if (( value < 0 || value > 255 )); then
        # Imprime el error.
        echo "Error: Valor de la IP tiene un formato incorrecto -> $value" >&2
        # Finaliza el script.
        exit 1
    fi
done

# Valida el puerto.
if ! [[ "$PORT" =~ ^[0-9]+$ ]] || ((PORT < 1 || PORT > 65535)); then
    # Imprime el error.
    echo "Error: Puerto inválido -> $PORT" >&2
    # Finaliza el script.
    exit 1
fi

# Valida si el puerto esta libre.
if command -v ss &>/dev/null && ss -tuln | grep -q "${IP}:${PORT}"; then
    # Imprime el error.
    echo "Error: El puerto ya está en uso -> $PORT" >&2
    # Finaliza el script.
    exit 10
fi

# Verifica que exista el binario de Ollama.
ollama_bin="${OLLAMA_BIN_PATH:-$(command -v ollama || echo "${root_dir}/bin/ollama/bin/ollama")}"
# Comprueba si existe.
if [ ! -x "$ollama_bin" ]; then
    # Imprime el error.
    echo "Error: Ollama no instalado en el sistema y no se encontró binario en $ollama_bin" >&2
    # Finaliza el script.
    exit 20
fi

# Exporta las variables de entorno para Ollama.
export OLLAMA_HOST="${IP}:${PORT}"

# Imprime la información.
echo "Iniciando Ollama desde ($ollama_bin) ..."

# Redirige la salida stdout y stderr.
exec 1>>"$root_dir/ollama.serve.log"
exec 2>&1

# Lanza Ollama.
exec "$ollama_bin" serve