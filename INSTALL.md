# Instrucciones de Instalación y Despliegue

## 1. Clonar Repositorio

1. Abre una terminal.
2. Clona el repositorio usando `git`:

    ```bash
    git clone https://github.com/Ignacio-Gutierrez/Computacion-II-Final.git
    cd Computacion-II-Final/app
    ```

## 2. Configurar el Entorno para ejecutar la API
Crea y activa un entorno virtual para evitar conflictos de dependencias.

    ```bash
    python3 -m venv db_service
    source db_service/bin/activate
    ```
### 2.1. Instalar dependencias
Instala las dependencias del proyecto especificadas en el archivo `server_requirements.txt`.

    ```bash
    pip install -r server_requirements.txt
    ```
### 2.2 Configurar variables de entorno
Crea un archivo `.env` en el directorio `db_api_service` y añade las siguientes variables de entorno:

    ```bash
    export DATABASE_PATH=/ruta/a/la/base/de/datos
    export DATABASE_NAME=nombre_de_la_base_de_datos
    ```
Asegúrate de reemplazar los valores con las rutas y nombres correctos para tu entorno.

### 2.3 Ejecutar la API Flask
Para lanzar el servicio API Flask, ejecuta Gunicorn con el siguiente comando:

    ```bash
    cd db_api_service
    gunicorn -w 1 -b 127.0.0.1:6666 app:app
    ```
Este comando ejecuta la API en `localhost` en el puerto `6666`.
(Se puede cambiar, se debe modificar el archivo de configuración del servidor para que direccione al nuevo `host`:`port`)

## 3. Desplegar el Servicio de Juego
1. En otra terminal:

    ```bash
    cd game_service
    ```
Crear archivo `config.ini` que contenga las configuraciones del servidor y de la API:
    ```
    [server]
    HOST = ::  
    PORT = 8888

    [api]
    HOST = localhost   
    PORT = 6666
    ```
si cambió `host`:`port` en la ejecución de la API o desea usar otros se debe modificar acá

2. Inicia el servidor de juego:

    ```bash
    python3 main.py
    ```
## 4. Ejecutar el Cliente
1. El directorio `client`, se puede ejecutar el cliente Telnet para conectarte al servidor de juego.

    ```bash
    cd cliente
    ```
Crear archivo `config.ini` que contenga las configuraciones del servidor:
    ```
    [server]
    HOST = ::  
    PORT = 8888
    ```
si cambió `host`:`port` en la ejecución de la API o desea usar otros se debe modificar acá

2. Ejecutar el cliente Telnet para conectarte al servidor de juego.

    ```bash
    python3 cliente.py -u <username> -p <password> -a <jugar>/<historial> -ip <ipv4>/<ipv6>
    ```
    -u: Nombre de usuario (username) del usuario.
    -p: Contraseña (password) del usuario.
    -a: Acción que desea realizar el usuario, puede ser jugar para comenzar una partida o historial para ver partidas anteriores.
    -ip: Dirección IP del servidor (puede ser ipv4 o ipv6)

## Notas Adicionales
- Asegúrase de que el archivo `.env` y `config.ini` estén correctamente configurado antes de iniciar el servidor y correctamente posicionados.
- Asegúrarse que el puerto especificado en `PORT` no esté en uso por otro servicio.