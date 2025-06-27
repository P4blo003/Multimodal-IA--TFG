# Asistente inteligente para una planta industrial basado en modelos de IA de gran tamaño.

## **Descripción del Proyecto**

Se trata de diseñar e implementar un prototipo de asistente inteligente basado en modelos de inteligencia artificial de gran tamaño (LAMs) de caracter abierto para dar soporte al análisis de información y la toma de decisiones en una planta de producción industrial. Para ello se estudiará previamente toda la oferta de LAMs de caracter abierto, así como las herramientas que permitan construir modelos multimodales a partir de los anteriores, tales como Haystack y LangChain. Para la sintonización de los modelos a utilizar por el asistente no se considerará su reentrenamiento, sino que se utilizarán exclusivamente técnicas de prompting y RAG. (Retrieval Augmented Generation, que posibilita la consulta de documentación técnica y bases de datos), proporcionando así el contexto necesario a los modelos.

## **Índice**
* Información del proyecto
* [Instalación](#instalación)
* [Forma de uso](#forma-de-uso)
* Futuras implementaciones
* Licencia

## **Instalación**
Para instalar el prototipo en tu equipo, simplemente ejecuta el siguiente script. Esto instalará todo lo necesario para ejecutar
el servidor en la carpeta raíz de tu usuario. Este fichero se encuentra en el siguiente [enlace](generator/install_server.sh).
```bash
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
mkdir "$WORK_DIR/.server/etc/measure"
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
pip install -r "dependencies/requirements.txt" > /dev/null 2>&1 || exit 1
pip3 install -U torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
echo -e "OK - Librerías instaladas."
deactivate

# Limpia el directorio temporal.
rm -rf "$TEMP_DIR"
```

## **Forma de uso**
A continuación, se muestra los pasos a realizar para ejecutar el servidor e interactuar con el.
Se tiene en cuenta que el prototipo ya ha sido instalado, siguiendo las [instrucciones](#instalación) detalladas 
en este documento.
1. Ubicate en la carpeta de la instalación. Esta es la carpeta `server`, ubicada en el directorio raíz de tu usuario.
Puedes acceder a ella con el siguiente comando.
```bash
cd ~/server
```
2. Ejecuta el proceso de Ollama. Este se encargara de ejecutar el modelo de conversación. Para ello, ejecuta el
el script ubicado en el siguiente [enlace](server/app/third-party/ollama/launch_ollama.sh). Puedes ejecutar el sifguiente comando para ejecutarlo.
```bash
# Recuerda que estas en la carpeta .../server
./app/third-party/ollama/launch_ollama.sh
# Importante: El fichero debe tener permisos de ejecución.
```
3. Activa el entorno de python.
```bash
# Recuerda que estas en la carpeta .../server
source venv/bin/activate
```
4. Ejecuta el servidor.
```bash
# Recuerda que estas en la carpeta .../server
python3 app/src/main.py
```

Importante: El prototipo obtiene los datos de los documentos que se encuentren dentro de la carpeta [server/.server/data_raw](server/.server/data/raw/).

Ya puedes comenzar a probar el prototipo. Para ello, puedes hacerlo de varias maneras. Si bien el prototipo esta en
una fase temprana, existen varias maneras de comunicarse con el:

### **Curl**
El servidor funciona mediante una API REST, por lo que es posible preguntar mediante el comando `curl`. Es importante
remarcar que en este caso el chat no tendrá un historial de la conversación. Para ello puedes ejecutar el siguiente
comando.
```bash
curl -X POST "http://<ip_prototipo>:<puerto_prototipo>/chat" \
  -H "Content-Type: application/json" \
  -d '{"content": <query>}'
```
- ip_prototipo: La IP establecida en el fichero de configuración de [uvicorn](server/.server/etc/configs/uvicorn.yaml)
- puerto_prototipo: El puerto establecido en el fichero de configuración de [uvicorn](server/.server/etc/configs/uvicorn.yaml)
- query: La pregunta que deseas hacer al prototipo.

### **Script**
También puedes ejecutar el script que simula un cliente simple. Para ello, ejecuta el siguiente comando.
```bash
# Recuerda que estas en la carpeta .../server
python3 app/src/test/query.py
```
Esto simulará una espcie de chat por consola con el prototipo.
