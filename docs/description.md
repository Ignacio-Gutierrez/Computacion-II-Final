# Descripción de la Aplicación

El proyecto consiste en una aplicación cliente-servidor para el juego **Cuatro en Línea**, implementado en Python. La aplicación permite a múltiples usuarios conectarse desde diferentes dispositivos para jugar en línea. El sistema utiliza un servidor central que gestiona las partidas, mientras que los clientes se encargan de enviar los movimientos realizados por los jugadores y recibir actualizaciones sobre el estado del juego.

## Funcionamiento del Cliente
Cada cliente actúa como una interfaz que permite al usuario jugar **Cuatro en Línea**. Los clientes se conectan al servidor y envían las jugadas (la columna donde desean colocar su ficha) al servidor. Además, los clientes reciben actualizaciones en tiempo real sobre el estado del tablero de juego, incluyendo mensajes que indican cuándo un jugador ha ganado, empatado o cometido una jugada inválida.

## Funcionamiento del Servidor
El servidor central gestiona múltiples partidas de **Cuatro en Línea** de manera concurrente. Cada vez que un cliente envía una jugada, el servidor valida el movimiento, actualiza el tablero y verifica si ha habido un ganador o si el juego ha terminado en empate. Si se cumple alguna de estas condiciones, el servidor envía un mensaje informativo a los jugadores.

El servidor se basada en **dos procesos paralelos**: uno encargado de la **lógica del juego** y otro que gestiona las **consultas** a la base de datos y a la API de gestión de usuarios. Estos procesos se comunican entre sí mediante **pipes** para intercambiar información de manera eficiente.

Para manejar las conexiones de múltiples clientes simultáneamente, el servidor utiliza **concurrencia** implementada con el módulo `asyncio`. Esto permite que cada cliente pueda interactuar con el servidor sin bloquear a otros jugadores. Los clientes y el servidor se comunican de manera asíncrona, intercambiando mensajes a través de sockets.

## Gestión de Usuarios y API
Además de la funcionalidad de juego, la aplicación incluye una **API REST** que gestiona la **base de datos de usuarios**. Esta API es responsable de registrar y autenticar usuarios, así como de almacenar y consultar el historial de partidas. Aunque la API no forma parte directa de la lógica del juego, es necesaria para gestionar el acceso de los jugadores y llevar un seguimiento de las partidas jugadas.

La API utiliza **Flask** como framework para manejar las solicitudes HTTP y se conecta a una base de datos para almacenar información de los usuarios. Las funciones principales de la API incluyen:
- Registro de nuevos usuarios.
- Autenticación de usuarios existentes.
- Almacenamiento del historial de partidas, incluyendo resultados y datos relacionados con cada sesión de juego.

## Tecnología Utilizada
- **Concurrencia:** Implementada en el servidor mediante `asyncio` para manejar múltiples conexiones simultáneas de clientes.
- **Paralelismo:** El servidor está dividido en dos procesos: uno encargado de manejar la lógica del juego y otro encargado de gestionar las consultas a la base de datos y la API. Estos procesos están conectados a través de `pipes` para comunicarse de manera eficiente.
- **Comunicación Asíncrona:** El servidor y los clientes se comunican utilizando sockets de manera no bloqueante.
- **Flask y Gunicorn:** Se utiliza Flask como microframework para la gestión de la API, y Gunicorn como servidor de aplicaciones.
- **Manejo de Estado del Juego:** El servidor actualiza el estado del juego y envía actualizaciones a los clientes.
- **Persistencia de Datos:** La API gestiona la base de datos de usuarios y el historial de partidas, permitiendo realizar consultas a través de uno de los procesos del servidor.


# Gráfico de la Arquitectura
```
+----------------+         +-------------------------------------------------------------------+
|    Cliente     |         |                                Servidor                           |
|                |         |                                                                   |
|                |         |           Proceso 1                        Proceso 2              |
|  +----------+  |   TCP   |   +-----------------------+  Pipe   +-------------------------+   |
|  |  Jugador |  +-------->|   |   Lógica de Juego y   +-------->| Consultas, Interacción  |   |
|  |   (CLI)  |  |         |   | manejo de de clientes |<--------+       con la API        |   |
|  +----------+  |         |   +-----------------------+   Pipe  +------------+------------+   |
+----------------+         +--------------------------------------------------|----------------+
                                                                              |
                                                                              | HTTP 
                                                                              v
                                                                +---------------------------+
                                                                |            API            |
                                                                |  +---------------------+  |
                                                                |  | Gestión de Usuarios |  |
                                                                |  |   y de Partidas     |  |
                                                                |  +---------------------+  |
                                                                +---------------------------+
```

## Nodos Principales:
1. **Cliente**:
   - Cada jugador utiliza un cliente que se conecta al servidor mediante sockets TCP.
   - Envía jugadas (movimientos) y recibe actualizaciones sobre el estado del tablero.
2. **Servidor**:
   - Centraliza la gestión de las partidas, recibiendo las jugadas de los jugadores y enviando las respuestas correspondientes.
   - Está dividido en dos procesos paralelos:
     - **Proceso de lógica del juego:** Gestiona las partidas y valida las jugadas de los jugadores.
     - **Proceso de consultas:** Maneja las interacciones con la API para la gestión de usuarios y almacenamiento de datos.
   - Estos dos procesos se comunican entre sí mediante `pipes`.
3. **API para la Gestión de Usuarios**:
   - Permite registrar, autenticar y gestionar usuarios a través de solicitudes HTTP.
   - Almacena el historial de partidas y permite obtener un listado de partidas del jugador que se le pida.

## Conectividad y Mecanismos de Comunicación:
- **Sockets TCP:** Se utilizan para la comunicación entre el cliente y el servidor. El servidor escucha en un puerto determinado para recibir las conexiones entrantes de los clientes.
- **Pipes IPC:** Los dos procesos del servidor (lógica del juego y consultas) se comunican utilizando `pipes` para intercambiar información.
- **API REST:** La API maneja solicitudes HTTP para gestionar usuarios y almacenar datos.
- **Flujos de Comunicación Asíncrona:** Cliente y servidor se comunican de manera no bloqueante a través de `asyncio`. El servidor y la API se comunican mediante solicitudes HTTP.

## Flujos de Comunicación:
1. **Conexión Cliente-Servidor:**
   - El cliente envía una solicitud para unirse a una partida.
   - El servidor acepta la conexión y guarda al jugador en una cola de jugadores que esperan jugar.
   - Cuando hay dos o más jugadores en la cola, el servidor retira a los dos primeros y comienza la partida.

2. **Autenticación y/o Registro:**
   - El cliente envía su nombre de usuario (username) y contraseña (password) al servidor.
   - El servidor valida las credenciales o registra al usuario en el sistema mediante la API.
   - El proceso de consultas del servidor interactúa con la API para verificar las credenciales del usuario y gestionar el registro.

3. **Jugar partida o Ver historial:**
    - **El cliente solicita jugar:**
        - El cliente envía el movimiento (columna donde desea colocar su ficha).
        - El proceso de lógica del juego recibe la jugada, la valida y actualiza el estado del juego.
    - **El cliente solicita historial:**
        - El cliente recibe su historial de partidas.

4. **Envío de Resultados:**
   - El servidor envía los resultados de las partidas a la API para almacenarlos en el historial.