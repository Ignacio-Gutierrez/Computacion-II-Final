import asyncio
import socket
import os
import configparser

from datetime import datetime

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
            await writer.drain()

            new_player = Player(reader, writer, username, register_response.get("user_id"))
            waiting_players.append(new_player)

        elif register_response.get("message") == "incorrect_password":
            writer.write("Contraseña incorrecta. Desconectando...\n".encode())
            await writer.drain()

        elif register_response.get("message") == "user_not_found":
            writer.write("Usuario no encontrado. Desconectando...\n".encode())
            await writer.drain()

    elif action == 'register':
        register_request = {'action': 'register', 'data': {'username': username, 'password': password}}
        print(f"Enviando solicitud de registro a la base de datos: {register_request}")
        game_sender.send(register_request)
        print("Solicitud enviada al pipe")
        
        register_response = game_receiver.recv()
        print(f"Respuesta recibida: {register_response}")

        if register_response.get("message") == "registered":
            writer.write(f"Registro exitoso, {username}! Ahora puedes jugar.\n".encode())
            await writer.drain()

            new_player = Player(reader, writer, username, register_response.get("user_id"))
            waiting_players.append(new_player)

        elif register_response.get("message") == "duplicated_username":
            writer.write("Usuario ya existe. Desconectando...\n".encode())
            await writer.drain()

    elif action == 'historial':
        page = 1
        history_request = {'action': 'history', 'data': {'username': username, 'page': page}}
        game_sender.send(history_request)
        print("Solicitud enviada al pipe")

        history_recv = game_receiver.recv()
        pages = history_recv.get("pages")

        history = format_history_for_display(history_recv.get("matches"))
        print(f"Historial de partidas de {username}:\n{history}")
        writer.write(f"Historial de partidas de {username}:\n{history}\n\n- Página {page} de [{pages}].".encode())
        await writer.drain()
        
        while True:

            page_request = await reader.read(100)

            if page_request.lower() == 'exit':
                break

            if page_request.isdigit() and 1 <= int(page_request) <= pages:
                page = int(page_request)

                history_request = {'action': 'history', 'data': {'username': username, 'page': page}}
                game_sender.send(history_request)
                history_recv = game_receiver.recv()
                pages = history_recv.get("pages")
                
                history = format_history_for_display(history_recv.get("matches"))
                print(f"Historial de partidas de {username}:\n{history}")
                writer.write(f"Historial de partidas de {username}:\n{history}\n\n- Página {page} de [{pages}].".encode())
                await writer.drain()
            else:
                writer.write(f"Número de página inválido. Por favor, introduce un número entre 1 y {pages}.\n".encode())
                await writer.drain()
        
    if len(waiting_players) >= 2:
        player1 = waiting_players.pop(0)
        player2 = waiting_players.pop(0)
        print("Partida iniciada entre dos jugadores")
        await start_game(player1, player2, game_sender, game_receiver)
    
def format_board_for_display(board):
    header = "|".join([f"[{i+1}]".center(5) for i in range(8)])

    formatted_board_display = [header]

    for row in board:
        formatted_row = "" + "|".join([cell.center(5) for cell in row])
        formatted_board_display.append(formatted_row)
    
    return "\n".join(formatted_board_display)

def format_history_for_display(history):
    header = f"{'N°'.ljust(5)} | {'Fecha'.ljust(25)} | {'Jugador 1'.ljust(20)} | {'Jugador 2'.ljust(20)} | {'Ganador'.ljust(20)}"
    separator = "-" * len(header)

    formatted_history = [header, separator]

    for index, game in enumerate(history, start=1):
        row = (
            f"{index}".ljust(5) + " | " +
            f"{game.get('game_date')}".ljust(25) + " | " +
            f"{game.get('player1_name')}".ljust(20) + " | " +
            f"{game.get('player2_name')}".ljust(20) + " | " +
            f"{game.get('winner_name')}".ljust(20)
        )
        formatted_history.append(row)

    return "\n".join(formatted_history)

async def start_game(player1, player2, game_sender, game_receiver):
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
            opponent_player.writer.write(f"El jugador {current_player.name} se ha desconectado. Fin del juego.\n".encode())
            await opponent_player.writer.drain()
            break

        user_move = data.decode().strip()

        if user_move.lower() == "exit":
                current_player.writer.write(f"Te has retirado del juego.\n".encode())
                opponent_player.writer.write(f"El jugador {current_player.name} se ha retirado del juego.\n".encode())
                await current_player.writer.drain()
                await opponent_player.writer.drain()
                break
    
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

            if "El Jugador X ganó" in game_status:
                winner_id = current_player.id
                loser_id = opponent_player.id
            else:
                winner_id = opponent_player.id
                loser_id = current_player.id
            
            finished_game = {
                'action': 'save_match',
                'data': {
                    "player1_id": current_player.id,
                    "player2_id": opponent_player.id,
                    "game_date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    "winner_id": winner_id,
                    "loser_id": loser_id
                }
            }
            game_sender.send(finished_game)
            saved_game = game_receiver.recv()
            
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