# Funcionalidades de Cada Entidad

## Cliente
- **Registro de usuarios**: Permite a los usuarios crear una cuenta en el sistema.
- **Inicio de sesión**: Autentica a los usuarios y obtiene un token JWT para acceder a las funcionalidades del juego.
- **Búsqueda de partidas**: Permite a los usuarios buscar y unirse a partidas disponibles.
- **Inicio de partidas**: Permite a los usuarios comenzar una nueva partida una vez que se han emparejado con un oponente.
- **Interfaz del juego 4 en línea**: Proporciona la interfaz gráfica para jugar el juego "4 en línea".
- **Enviar y recibir actualizaciones del estado del juego**: Permite al cliente enviar y recibir información en tiempo real sobre el estado de la partida.

## Servidor

### Servidor DB-Auth
- **Gestión de registro de usuarios**: Maneja la creación y actualización de cuentas de usuario en la base de datos.
- **Autenticación de usuarios**: Verifica las credenciales de los usuarios y emite un token JWT para sesiones válidas.
- **Almacenamiento de resultados de partidas en la base de datos**: Guarda los resultados de las partidas (ganadores, perdedores, fecha, hora) en la base de datos para futuras consultas.

### Servidor Game
- **Emparejamiento de jugadores**: Organiza y empareja a los jugadores en partidas disponibles o en cola de espera.
- **Manejo de la lógica del juego**: Gestiona las reglas del juego "4 en línea", incluyendo la verificación de movimientos y determinación del ganador.
- **Gestión de múltiples conexiones de clientes de forma concurrente**: Maneja múltiples sesiones de juego simultáneamente, asegurando que las interacciones entre clientes y el servidor sean efectivas y eficientes.

## Base de Datos
- **Almacenamiento de información de los usuarios**: Guarda detalles como nombre de usuario, contraseña (cifrada) y otros datos relacionados con los usuarios.
- **Registro de historial de partidas**: Almacena el historial de partidas jugadas, incluyendo los jugadores involucrados, fecha y hora de cada partida, y los resultados (ganador y perdedor).
