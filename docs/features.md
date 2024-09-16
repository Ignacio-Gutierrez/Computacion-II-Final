# Funcionalidades por Entidad

## Cliente
- **Conexión al Servidor:** Se conecta al servidor mediante sockets TCP.
- **Autenticación y Registro:** Envía nombre de usuario y contraseña al servidor para autenticarse o registrarse.
- **Envío de Jugadas:** Envía movimientos (columnas donde desea colocar fichas) al servidor.
- **Recepción de Actualizaciones:** Recibe actualizaciones sobre el estado del tablero y el resultado del juego (ganador, empate, jugada inválida).
- **Solicitar Historial:** Solicita y recibe el historial de partidas del jugador.

## Servidor
- **Gestión de Conexiones:** Acepta y maneja múltiples conexiones de clientes simultáneamente.
- **Validación y Gestión de Jugadas:**
  - Recibe y valida los movimientos enviados por los clientes.
  - Actualiza el estado del juego en función de las jugadas.
  - Verifica si hay un ganador o si el juego ha terminado en empate.
  - Envía mensajes a los clientes sobre el estado del juego.
- **Manejo de Partidas:**
  - Mantiene una cola de jugadores esperando para jugar.
  - Asigna jugadores a partidas cuando hay suficientes participantes (dos o más).
- **Comunicación entre Procesos:**
  - Utiliza pipes para comunicarse entre el proceso de lógica del juego y el proceso de consultas.
- **Interacción con la API:**
  - Realiza consultas a la API para validar usuarios.
  - Envía resultados de partidas a la API para su almacenamiento en el historial.
  - Consulta el historial de partidas de un jugador a la API.

## API para la Gestión de Usuarios
- **Registro de Usuarios:**
  - Permite la creación de nuevos usuarios.
- **Autenticación de Usuarios:**
  - Verifica las credenciales de los usuarios para permitirles acceder al juego.
- **Almacenamiento de Datos:**
  - Almacena el historial de partidas de los usuarios.
  - Permite consultar el historial de partidas.