import asyncio
import socket
import os
import configparser

from game import Connect_4

config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

config = configparser.ConfigParser()
config.read(config_path)

host = config['server']['HOST']
port = int(config['server']['PORT'])

waiting_players = []

class Player:
    def __init__(self, reader, writer, username, id):
        self.reader = reader
        self.writer = writer
        self.username = username
        self.id = id


async def handle_client(reader, writer, game_sender, game_receiver):
    addr = writer.get_extra_info('peername')
    print(f"Jugador conectado desde {addr}")

    credentials_data = await reader.read(1024)
    if not credentials_data:
        print(f"Jugador {addr} se desconectó antes de enviar credenciales.")
        writer.close()
        await writer.wait_closed()
        return
    
    credentials = credentials_data.decode().strip()
    username, password, action = credentials.split(',')
    print(f"Credenciales recibidas - Usuario: {username}, Acción: {action}")

    if action == 'jugar':
        register_request = {'action': 'login', 'data': {'username': username, 'password': password}}
        print(f"Enviando solicitud de autenticación a la base de datos: {register_request}")
        game_sender.send(register_request)
        print("Solicitud enviada al pipe")

        register_response = game_receiver.recv()
        print(f"Respuesta recibida: {register_response}")

        if register_response.get("message") == "ok":
            writer.write(f"Bienvenido {username}, autenticación exitosa!\n".encode())

            new_player = Player(reader, writer, username, register_response.get("id"))
            waiting_players.append(new_player)

        elif register_response.get("message") == "incorrect_password":
            writer.write("Contraseña incorrecta. Desconectando...\n".encode())

        elif register_response.get("message") == "user_not_found":
            writer.write("Usuario no encontrado. Desconectando...\n".encode())

    elif action == 'register':
        register_request = {'action': 'register', 'data': {'username': username, 'password': password}}
        print(f"Enviando solicitud de registro a la base de datos: {register_request}")
        game_sender.send(register_request)
        print("Solicitud enviada al pipe")
        
        register_response = game_receiver.recv()
        print(f"Respuesta recibida: {register_response}")

        if register_response.get("message") == "registered":
            writer.write(f"Registro exitoso, {username}! Ahora puedes jugar.\n".encode())

            new_player = Player(reader, writer, username, register_response.get("id"))
            waiting_players.append(new_player)

        elif register_response.get("message") == "duplicated_username":
            writer.write("Usuario ya existe. Desconectando...\n".encode())

    elif action == 'historial':
        history_request = {'action': 'history', 'data': {username}}
        game_sender.send(history_request)
        print("Solicitud enviada al pipe")
        
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

async def main(game_sender, game_receiver):
    addr = (host, port)

    if socket.has_dualstack_ipv6():
        s = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
    else:
        s = socket.create_server(addr)

    s.setblocking(False)

    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, game_sender, game_receiver),
        sock=s
    )

    addr = server.sockets[0].getsockname()
    print(f"Servidor escuchando en {addr}")

    async with server:
        await server.serve_forever()

def run_async_server(game_sender, game_receiver):
    asyncio.run(main(game_sender, game_receiver))