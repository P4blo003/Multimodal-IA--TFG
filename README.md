# Configuración y ejecución local de un modelo de IA multimodal de gran tamaño para la consulta asistida de información sobre consumo eléctrico en una planta industrial.

## **Índice**
1. [Instalación y dependencias](#instalación-y-dependencias)

## **Instalación y dependencias**
![Python Version](https://img.shields.io/badge/python-3.9.6-blue)
![Python Version](https://img.shields.io/badge/python-3.12.6-blue)

### 1. Clonar el repositorio

Primero, debes clonar el repositorio del proyecto. Abre tu terminal y ejecuta el siguiente comando:
```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
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
pip install -r dependencies/py[version]/requirements.txt
```

### 4. Instalar el modelo

Cuarto, instala el modelo que desees con el siguiente comando:
```bash
./scripts/install-model.sh [nombre_del_modelo]
```