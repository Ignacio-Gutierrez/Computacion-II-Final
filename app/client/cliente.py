import asyncio
import argparse
import socket

HOST = 'localhost'    
PORT = 8888

async def connect_to_server(username, password, action, ip_version):
    if ip_version == 'ipv6':
        reader, writer = await asyncio.open_connection(HOST, PORT, family=socket.AF_INET6)
    else:
        reader, writer = await asyncio.open_connection(HOST, PORT, family=socket.AF_INET)
    
    print(f"Conectado al servidor {HOST} en el puerto {PORT} usando {ip_version.upper()}.")

    while True:
        data = await reader.read(500)
        if not data:
            break
        print(f"Recibido: {data.decode()}")

    print("Conexión cerrada")
    writer.close()
    await writer.wait_closed()

def parse_args():
    parser = argparse.ArgumentParser(description="Cliente Telnet para conectarse al servidor de juego")
    parser.add_argument('-u','--username', type=str, required=True, help='Tu nombre de usuario')
    parser.add_argument('-p','--password', type=str, required=True, help='Tu contraseña')
    parser.add_argument('-a','--action', type=str, choices=['jugar', 'historial'], default='jugar', help='Acción: jugar o ver historial')
    parser.add_argument('-ip','--ip_version', type=str, choices=['ipv4', 'ipv6'], default='ipv4', help='Especifica si usar IPv4 o IPv6 (por defecto IPv4)')
    
    return parser.parse_args()

async def main():
    args = parse_args()
    await connect_to_server(args.username, args.password, args.action, args.ip_version)

if __name__ == '__main__':
    asyncio.run(main())
