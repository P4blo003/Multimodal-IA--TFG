# Configuración y ejecución local de un modelo de IA multimodal de gran tamaño para la consulta asistida de información sobre consumo eléctrico en una planta industrial.

## **Índice**

1. [Requisitos](#requisitos)
2. [Instalación y dependencias](#instalación-y-dependencias)
3. [Forma de uso](#forma-de-uso)

## **Requisitos**

- **Sistema operativo**: Linux (Con soporte para Bash)
- **Dependencias**:
  - Bash
  - [Python](https://www.python.org/downloads/)
  - [Hugging Face](https://huggingface.co/)


## **Instalación y dependencias**

![Python Version](https://img.shields.io/badge/python-3.12.6-blue)

### 1. Clonar el repositorio

Primero, debes clonar el repositorio del proyecto. Abre tu terminal y ejecuta el siguiente comando:
```bash
git clone https://github.com/P4blo003/Multimodal-IA--TFG.git
cd Multimodal-IA--TFG
```

### 2. Creaación del entorno virtual

Sefundo, crea el entorno virtual y luego activalo con los siguientes comandos:
```bash
python3 -m venv [nombre_del_entorno]
source venv/bin/activate
```

### 3. Instalar dependencias

Tercero, debes instalar las dependencias dependiendo de la versión python de tu equipo con el siguiente comando:
```bash
pip install -r dependencies/py<version>/requirements.txt
```

En caso de que la instalación no funcione, a continuación estan los comandos para instalar las dependencias una a una:
```bash
pip3 install colorama
pip3 install huggingface_hub
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip3 install transformers
```

## **Forma de uso**

### 1. Instalación del modelo

Para instalar un modelo, primero debes obtener el nombre del mismo. Por ejemplo en el caso del modelo de Deepseek 1.5B
puedes dirigirte a la página oficial de [Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B).

Tras tener el nombre, puede instalar el modelo con el siguiente script desde la carpeta Multimodal-IA--TFG.
```bash
./scripts/install-model.sh <nombre_modelo>
```
El programa comezará la instalación en el directorio ai-models.