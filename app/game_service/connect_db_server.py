import requests
import os
import configparser

config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

host = config['api']['HOST']
port = int(config['api']['PORT'])

def connect_to_db(db_sender, db_receiver):
    while True:
        if db_receiver.poll():
            message = db_receiver.recv()
            print(f"Solicitud recibida en connect_to_db: {message}")
            action = message['action']
            data = message['data']

            try:
                if action == 'login':
                    response = requests.post(f'http://{host}:{port}/auth/login', json=data)
                    response.raise_for_status()
                    response_data = response.json()
                    print(f"Respuesta de autenticación: {response_data}")

                elif action == 'register':
                    response = requests.post(f'http://{host}:{port}/auth/register', json=data)
                    response.raise_for_status()
                    response_data = response.json()
                    print(f"Respuesta de registro: {response_data}")

                elif action == 'save_match':
                    response = requests.post(f'http://{host}:{port}/matches', json=data)
                    response.raise_for_status()
                    response_data = response.json()
                    print(f"Respuesta de guardado de partida: {response_data}")

                elif action == 'history':
                    player = data['username']
                    page = data['page']
                    response = requests.get(f'http://{host}:{port}/matches?page={page}&player={player}')
                    response.raise_for_status()
                    response_data = response.json()
                    print(f"Respuesta de historial de partidas: {response_data}")

            except requests.RequestException as e:
                print(f"Error en la autenticación: {e}")
                response_data = {"message": "error", "details": str(e)}

            db_sender.send(response_data)
            print(f"Respuesta enviada a async_game_server: {response_data}")
        else:
            continue