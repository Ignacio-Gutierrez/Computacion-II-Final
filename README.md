# Computacion-II-Final

# Cuatro en Línea - README

Proyecto **Cuatro en Línea**. Aplicación que permite jugar al juego "Cuatro en Linea" en línea.

## Descripción

La aplicación está compuesta por un cliente y un servidor. El cliente permite a los jugadores interactuar con el juego o ver su historial de partidas, mientras que el servidor gestiona la lógica del juego, maneja múltiples partidas y se comunica con una API para la gestión de usuarios y el almacenamiento de las partidas.

## Instalación

Para obtener información sobre cómo instalar y ejecutar el proyecto consulta el archivo [INSTALL.md](INSTALL.md).

## Uso Básico

### Ejecutar la Aplicación

1. **Iniciar el Servidor**

   Las instrucciones para iniciar el servidor y la API están en el archivo [INSTALL.md](INSTALL.md).

2. **Iniciar el Cliente**

   Los clientes pueden ser ejecutados desde la línea de comandos. Asegurarse de tener el cliente configurado previo a conectarse al servidor [INSTALL.md](INSTALL.md).

### Interacción con la Aplicación

#### Conectarse al Servidor

1. **Iniciar el Cliente**

   Ejecuta el cliente desde la línea de comandos. El cliente se conectará al servidor utilizando sockets TCP.

2. **Unirse a una Partida**

   Se ingresará los datos del usuario y la configuración con la que se desea iniciar junto a la ejecución dek cliente, si no está registrado aún debe escoger el nombre de usuario (username) y contraseña (password) con las que desea registrarse.

   ```bash
    python3 cliente.py -u <username> -p <password> -a <jugar>/<historial> -ip <ipv4>/<ipv6>
    
-u: Nombre de usuario (username) del usuario.

-p: Contraseña (password) del usuario.

-a: Acción que desea realizar el usuario, puede ser jugar para comenzar una partida o historial para ver partidas anteriores.

-ip: Dirección IP del servidor (puede ser ipv4 o ipv6)