# Asistente inteligente para una planta industrial basado en modelos de IA de gran tamaño.

## **Descripción del Proyecto**

Se trata de diseñar e implementar un prototipo de asistente inteligente basado en modelos de inteligencia artificial de gran tamaño (LAMs) de caracter abierto para dar soporte al análisis de información y la toma de decisiones en una planta de producción industrial. Para ello se estudiará previamente toda la oferta de LAMs de caracter abierto, así como las herramientas que permitan construir modelos multimodales a partir de los anteriores, tales como Haystack y LangChain. Para la sintonización de los modelos a utilizar por el asistente no se considerará su reentrenamiento, sino que se utilizarán exclusivamente técnicas de prompting y RAG. (Retrieval Augmented Generation, que posibilita la consulta de documentación técnica y bases de datos), proporcionando así el contexto necesario a los modelos.

## **Índice**
1. [Arquitectura del sistema](#arquitectura-del-sistema)
2. [Instalación y dependencias](#instalación-y-dependencias)
    1. [Instalación del servidor.](#servidor)
    2. [Instalación del cliente.](#cliente)
3. [Ejecución](#ejecución)
4. [Uso](#uso)
5. [Estructura del repositorio](#estructura-del-repositorio)
6. [Creditos y referencias](#créditos-y-referencias)

## **Arquitectura del Sistema**


## **Instalación y dependencias**
![Python Version](https://img.shields.io/badge/python-3.12.3-blue)

En la siguiente tabla se muestran las herramientas necesarias para instalar los componentes y las versiones
con las que han sido ejecutadas.

| Herramienta | Uso principal                          | Versión mínima recomendada        |
|-------------|-------------------------------------|----------------------------------|
| `git`       | Clonar repositorios y manejar checkout | 2.43.0                           |
| `curl`      | Descargar archivos y hacer peticiones HTTP | 8.5.0                          |
| `tar`       | Descomprimir archivos `.tgz`         | 1.35                                |
| `python3`   | Ejecutar entorno virtual y scripts Python | 3.12.3 (recomendado)             |
| `pip`       | Instalar paquetes Python en el entorno virtual | 24.0                             |

### **Servidor**
El servidor es el encargado de ejecutar los modelos. Recibe las querys de los clientes y devuelve
las respuestas.
Para instalar el servidor en tu equipo, debes ejecutar el código del shell disponible en
`generator/install_server.sh`.
Para ejecutarlo, lanzalo de la siguiente manera:
```bash
# Lanza el shell.
./install_server.sh
```
También puedes copiar el siguiente código:
```bash
# Variables globales.
GIT_URL="https://github.com/P4blo003/Multimodal-IA--TFG.git"
FOLDERS=("application/server" "dependencies" "config")
BASE_DIR="server"

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
```
Esto generar el servidor en el directorio base del usuario: `~/server`

### **Cliente**
El cliente es el encargado de recibir la query del usuario, enviarla al servidor y mostrar la respuesta
obtenida.
Para instalar el cliente en tu equipo, debes ejecutar el código del shell disponible en
`generator/install_client.sh`.
Para ejecutarlo, lanzalo de la siguiente manera:
```bash
# Lanza el shell.
./install_client.sh
```
También puedes copiar el siguiente código:
```bash

```
Esto generar el servidor en el directorio base del usuario: `~/client`

## **Ejecución**


## **Uso**


## **Estructura del repositorio**


## **Créditos y Referencias**
- Basado en modelos LLM vía Ollama y HuggingFace.
- RAG con [Haystack](#https://haystack.deepset.ai/) y [LangChain](#https://www.langchain.com/).
- Parte de un TFG en Ingeniería Informática - Universidad de Oviedo.