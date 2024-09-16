# Informe de Diseño del Sistema

## Decisiones Principales de Diseño


### 1. Uso de Asyncio y Multiprocessing

**Decisión:**
El servidor utiliza `asyncio` para manejar la concurrencia y está dividido en dos procesos paralelos: uno para la lógica del juego y otro para las consultas a la API.

**Justificación:**
-**Concurrencia:** `asyncio` permite que el servidor maneje muchas conexiones simultáneamente sin bloquearse. Esto es esencial para ofrecer una experiencia de juego fluida con varios jugadores, ya que el servidor puede procesar múltiples acciones al mismo tiempo sin ralentizarse.
-**Paralelismo:** Separar la lógica del juego y las consultas a la API en dos procesos diferentes mejora el rendimiento. Esto asegura que el juego y las interacciones con la API se gestionen de forma independiente, evitando que uno interfiera con el otro y permitiendo que el servidor funcione de manera más eficiente.

### 2. Comunicación Asíncrona

**Decisión:**
La comunicación entre el cliente y el servidor se realiza mediante sockets TCP de manera asíncrona.

**Justificación:**
Usar `asyncio` para manejar las conexiones y la lógica del juego en lugar de crear un proceso para cada partida ofrece varias ventajas. Como el servidor solo recibe inputs pequeños de los jugadores (la posición de las fichas) no es eficiente usar un proceso o hilo completo para cada partida, asyncio permite gestionar muchas conexiones y tareas al mismo tiempo dentro de un solo proceso, lo que ahorra memoria y recursos del sistema. Además, hace que el servidor sea más rápido y eficiente al responder a los jugadores, ya que maneja las solicitudes de manera más ágil. Esto resulta en un servidor que puede soportar más jugadores simultáneamente.

### 4. API REST para la Gestión de Usuarios

**Decisión:**
Se utiliza una `API REST`, implementada con Flask, para gestionar usuarios y almacenar datos de partidas.

**Justificación:**
La `API REST` facilita la interacción entre el servidor y la base de datos de usuarios a través de solicitudes HTTP, permitiendo operaciones como el registro, autenticación y almacenamiento del historial de partidas. Esto proporciona una interfaz clara y estandarizada para la gestión de datos de usuarios, sobre la cual se puede estblecer un sistema de sesiones mas robusto en un futuro.