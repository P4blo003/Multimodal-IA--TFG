# Asistente inteligente para una planta industrial basado en modelos de IA de gran tamaño.

## **Descripción del Proyecto**

Se trata de diseñar e implementar un prototipo de asistente inteligente basado en modelos de inteligencia artificial de gran tamaño (LAMs) de caracter abierto para dar soporte al análisis de información y la toma de decisiones en una planta de producción industrial. Para ello se estudiará previamente toda la oferta de LAMs de caracter abierto, así como las herramientas que permitan construir modelos multimodales a partir de los anteriores, tales como Haystack y LangChain. Para la sintonización de los modelos a utilizar por el asistente no se considerará su reentrenamiento, sino que se utilizarán exclusivamente técnicas de prompting y RAG. (Retrieval Augmented Generation, que posibilita la consulta de documentación técnica y bases de datos), proporcionando así el contexto necesario a los modelos.

## **Índice**
1. [Arquitectura del sistema](#arquitectura-del-sistema)
2. [Instalación y dependencias](#instalación-y-dependencias)
3. [Ejecución](#ejecución)
4. [Uso](#uso)
5. [Estructura del repositorio](#estructura-del-repositorio)
6. [Creditos y referencias](#créditos-y-referencias)

## **Arquitectura del Sistema**
- Arquitectura **cliente-servidor**:
    - Cliente: CLI o frontend que realiza las preguntas.
    - Servidor: Expone endpoints y orquesta modelos, RAG y sesión.
- Componentes:
    - Módulo RAG: Responsable de recuperar información contextual relevante.
    - Controlador Conversacional: Mantiene el estado de la sesión y compone el prompt final.
    - API Local de Ollama: Despliega el modelo de conversación.
    - Controlador de Sesión: Gestiona las sesiones de chat entre el cliente y el servidor.
    - Interfaz del Cliente: Se maneja a través de un script.

## **Instalación y dependencias**
![Python Version](https://img.shields.io/badge/python-3.12.3-blue)

- pip / virtualenv
- Docker (opcional para Ollama): Pero no implementado.
- Modelos compatibles con Ollama

Para instalar el modelo, se deben seguir los siguientes pasos:
```bash
# Clonar el repositorio:
git clone https://github.com/P4blo003/Multimodal-IA--TFG.git
cd Multimodal-IA--TFG
```
En el repositorio estan tanto el cliente como el servidor. En función de lo que desee el usuario, 
se pueden preparar solo el entorno del servidor o del cliente.

Para preparar el entorno del servidor:
```bash
# Ejecutar el shell:
./setup/create_server.sh <nombre_carpeta>
```
Este script creará la carpeta <nombre_carpeta> en el directorio raiz del usuario. En esta carpeta
se añadiran todos los ficheros necesarios y se instalarn las dependencias.

Para preparar el entorno del cliente:
```bash
# Ejecutar el shell:
./setup/create_client.sh <nombre_carpeta>
```
Este script creará la carpeta <nombre_carpeta> en el directorio raiz del usuario. En esta carpeta
se añadiran todos los ficheros necesarios y se instalarn las dependencias.

## **Ejecución**
Para ejecutar los scripts, se debe estar dentro de las respectivas carpetas creadas:

Para ejecutar el servidor:
```bash
# Ejecutar el script.
cd ~/<nombre_carpeta>
python3 server/ource/main.py
```
Para ejecutar el cliente:
```bash
# Ejecutar el script.
cd ~/<nombre_carpeta>
python3 client/source/main.py
```

## **Uso**
Para hacer uso del prototipo, el servidor debe estar arrancado antes de ejecutar el cliente.
Una vez iniciados ambos, se podrán introducir preguntas desde la consola. Estas serán enviadas
al servidor y se procesaran para generar la respuesta.

## **Estructura del repositorio**


## **Créditos y Referencias**
- Basado en modelos LLM vía Ollama y HuggingFace.
- RAG con [Haystack](#https://haystack.deepset.ai/) y [LangChain](#https://www.langchain.com/).
- Parte de un TFG en Ingeniería Informática - Universidad de Oviedo.