import asyncio
import socket

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Conexión desde {addr}")

    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        print(f"Recibido: {message}")
        
        print("Enviando mensaje de vuelta")
        writer.write(data)
        await writer.drain()

    print("Cierre de la conexión")
    writer.close()
    await writer.wait_closed()

async def main():
    server_ipv4 = await asyncio.start_server(
        handle_client,
        '0.0.0.0',
        8888,
        family=socket.AF_INET
    )
    
    server_ipv6 = await asyncio.start_server(
        handle_client,
        '::',
        8888,
        family=socket.AF_INET6
    )
    
    addr_ipv4 = server_ipv4.sockets[0].getsockname()
    addr_ipv6 = server_ipv6.sockets[0].getsockname()
    print(f"Servidor escuchando en IPv4: {addr_ipv4}")
    print(f"Servidor escuchando en IPv6: {addr_ipv6}")

    async with server_ipv4, server_ipv6:
        await asyncio.gather(
            server_ipv4.serve_forever(),
            server_ipv6.serve_forever()
        )

if __name__ == '__main__':
    asyncio.run(main())
