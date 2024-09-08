import asyncio
import socket
from game import Connect_4

waiting_players = []

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Jugador conectado desde {addr}")

    waiting_players.append((reader, writer))
    
    if len(waiting_players) >= 2:
        player1_reader, player1_writer = waiting_players.pop(0)
        player2_reader, player2_writer = waiting_players.pop(0)
        print("Partida iniciada entre dos jugadores")
        await start_game(player1_reader, player1_writer, player2_reader, player2_writer)

def format_board_for_display(board):
    header = "  ".join([f"({i+1})" for i in range(8)])  # Números de columna
    rows = []
    for row in board:
        rows.append(" | ".join(row))
    board_display = "\n".join(rows)
    return f"  {header}\n{board_display}\n"

async def start_game(player1_reader, player1_writer, player2_reader, player2_writer):
    game = Connect_4()
    players = [(player1_reader, player1_writer), (player2_reader, player2_writer)]
    turn = 0

    while True:
        current_reader, current_writer = players[turn]
        opponent_reader, opponent_writer = players[1 - turn]

        # Formatear el tablero para mostrarlo en Telnet
        board_display = format_board_for_display(game.board)
        current_writer.write(f"Tablero actual:\n{board_display}\n".encode())
        current_writer.write(f"Tu turno, Jugador {game.player_turn()}! Selecciona una columna (1-8): ".encode())
        await current_writer.drain()

        data = await current_reader.read(100)
        if not data:
            raise ConnectionError("Jugador desconectado")

        user_move = data.decode().strip()

        try:
            valid_move = game.put_token(int(user_move))
            if not valid_move:
                current_writer.write(f"Movimiento inválido. Inténtalo nuevamente.\n".encode())
                await current_writer.drain()
                continue
        except ValueError:
            current_writer.write(f"Entrada inválida. Elige un número entre 1 y 8.\n".encode())
            await current_writer.drain()
            continue

        game_status = game.winner()
        if game_status != True:
            board_display = format_board_for_display(game.board)
            current_writer.write(f"Tablero final:\n{board_display}\n{game_status}\n".encode())
            opponent_writer.write(f"Tablero final:\n{board_display}\n{game_status}\n".encode())
            await current_writer.drain()
            await opponent_writer.drain()
            break

        # Enviar el tablero actualizado al oponente
        board_display = format_board_for_display(game.board)
        opponent_writer.write(f"Tablero actualizado:\n{board_display}\nEs tu turno, Jugador {game.player_turn()}.\n".encode())
        await opponent_writer.drain()

        # Cambiar el turno al otro jugador
        turn = 1 - turn

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