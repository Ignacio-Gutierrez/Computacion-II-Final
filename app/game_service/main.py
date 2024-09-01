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
    addr = ("", 8888)

    if socket.has_dualstack_ipv6():
        s = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
    else:
        s = socket.create_server(addr)

    s.setblocking(False)

    server = await asyncio.start_server(
        handle_client,
        sock=s
    )

    addr = server.sockets[0].getsockname()
    print(f"Servidor escuchando en {addr}")

    async with server:
        await server.serve_forever()
        
if __name__ == '__main__':
    asyncio.run(main())
