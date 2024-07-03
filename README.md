# ScrapyGeoservices

## Descripción
ScrapyGeoservices es una herramienta diseñada para interactuar con servicios de Esri y Geoserver. Esta aplicación permite consultar capas geográficas y generar reportes en formatos JSON y Excel.

## Requisitos

- Python 3.10 o superior
- owslib 0.31.0 o superior

## Instalación

1. Clona este repositorio en tu máquina local:
    ```sh
    git clone https://github.com/haroldavenia/ScrapyGeoservices.git
    cd ScrapyGeoservices
    ```

2. Crea un entorno virtual e instálalo:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # En Windows
    source venv/bin/activate  # En macOS/Linux
    ```

3. Instala las dependencias necesarias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

### Compilar a .exe

Para compilar el proyecto a un ejecutable (.exe), utiliza PyInstaller con el archivo de especificaciones:

```sh
pyinstaller main.spec
