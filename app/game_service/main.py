import asyncio
import socket

from game import Connect_4

waiting_players = []

class Player:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Jugador conectado desde {addr}")

    new_player = Player(reader, writer)

    waiting_players.append(new_player)

    if len(waiting_players) >= 2:
        player1 = waiting_players.pop(0)
        player2 = waiting_players.pop(0)
        print("Partida iniciada entre dos jugadores")
        await start_game(player1, player2)
    
def format_board_for_display(board):
    header = " ".join([f"({i+1}) " for i in range(8)])
    rows = []
    for row in board:
        rows.append("    |".join(row))
    board_display = "\n".join(rows)
    return f" {header}\n{board_display}\n"

async def start_game(player1, player2):
    game = Connect_4()
    players = [player1, player2]
    turn = 0

    while True:
        current_player = players[turn]
        opponent_player = players[1 - turn]

        # Formatear el tablero para mostrarlo en Telnet
        board_display = format_board_for_display(game.board)
        current_player.writer.write(f"Tablero actual:\n{board_display}\nTu turno, Jugador {game.player_turn()}! Selecciona una columna (1-8) o 'exit' para salir:".encode())
        await current_player.writer.drain()

        data = await current_player.reader.read(100)
        if not data:
            raise ConnectionError("Jugador desconectado")

        user_move = data.decode().strip()

        try:
            valid_move = game.put_token(int(user_move))
            if not valid_move:
                current_player.writer.write(f"Movimiento inválido. Inténtalo nuevamente.\n".encode())
                await current_player.writer.drain()
                continue
        except ValueError:
            current_player.writer.write(f"Entrada inválida. Elige un número entre 1 y 8.\n".encode())
            await current_player.writer.drain()
            continue

        game_status = game.winner()
        if game_status != True:
            board_display = format_board_for_display(game.board)
            current_player.writer.write(f"Tablero final:\n{board_display}\n{game_status}\n".encode())
            opponent_player.writer.write(f"Tablero final:\n{board_display}\n{game_status}\n".encode())
            await current_player.writer.drain()
            await opponent_player.writer.drain()
            break

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
