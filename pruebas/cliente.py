import asyncio
import argparse

async def handle_server(reader):
    try:
        while True:
            data = await reader.read(100)
            if not data:
                print("Conexión cerrada por el servidor.")
                break
            message = data.decode()
            print(message, end='')  # Mostrar el mensaje en la terminal
    except asyncio.CancelledError:
        pass
    finally:
        print("Finalizando la recepción de mensajes del servidor.")

async def main(host, port):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        print(f"Conectado al servidor {host}:{port}")

        # Crear una tarea para manejar los mensajes del servidor
        server_task = asyncio.create_task(handle_server(reader))

        while True:
            message = input()  # Leer entrada del usuario
            if message.lower() == 'salir':
                break
            writer.write(message.encode() + b'\n')
            await writer.drain()  # Asegurarse de que el mensaje se envíe

        # Finalizar la tarea de manejo del servidor
        server_task.cancel()
        await server_task
    except ConnectionRefusedError:
        print(f"No se pudo conectar al servidor en {host}:{port}. Asegúrate de que el servidor esté en ejecución.")
    except asyncio.CancelledError:
        print("Cliente terminado.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print("Desconectado del servidor.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cliente para conectarse al servidor de juego.')
    parser.add_argument('-H', '--host', required=True, help='Dirección IP del servidor.')
    parser.add_argument('-p', '--port', type=int, required=True, help='Puerto del servidor.')

    args = parser.parse_args()
    asyncio.run(main(args.host, args.port))
    