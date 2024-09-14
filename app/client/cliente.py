import argparse
import socket

import os
import configparser

import re
import colorama
colorama.init(autoreset=True)

config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

config = configparser.ConfigParser()
config.read(config_path)

host = config['server']['host']
port = int(config['server']['port'])

def telnet_client(username, password, action, ip_version):

    while True:
        register_status = input("¿Estás registrado? (s/n): ").lower()
        if register_status == 'n':
            action = 'register'
            break
        elif register_status == 's':
            break
        else:
            print("Entrada no válida. Por favor, ingresa 's' para sí o 'n' para no.")
            continue
        
    try:
        if ip_version == 'ipv4':
            family = socket.AF_INET
        else:
            family = socket.AF_INET6

        with socket.socket(family, socket.SOCK_STREAM) as c_s:

            if action == 'jugar':
                c_s.connect((host, port))
                print(f"Conectado a {host}:{port} usando {ip_version.upper()}")

                credentials = f"{username},{password},{action}"
                c_s.send(credentials.encode())
                
                response = c_s.recv(1024).decode()
                print(f"{response}")

                while True:
                    response = c_s.recv(1024).decode()
                    response = response.replace('X', f"{colorama.Fore.CYAN + colorama.Style.BRIGHT}X{colorama.Style.RESET_ALL}")
                    response = response.replace('O', f"{colorama.Fore.MAGENTA + colorama.Style.BRIGHT}O{colorama.Style.RESET_ALL}")
                    print(f"{response}")

                    comando = input("=>  ")
                    if comando.lower() == 'exit':
                        break

                    if comando not in [str(i) for i in range(1, 9)]:
                        print("Comando inválido, por favor ingresa un número entre 1 y 8")
                        continue

                    c_s.send(comando.encode())

                print("Desconectando...")
                c_s.send("exit".encode())

            elif action == 'historial':
                c_s.connect((host, port))
                print(f"Conectado a {host}:{port} usando {ip_version.upper()}")

                credentials = f"{username},{password},{action}"
                c_s.send(credentials.encode())
                
                response = c_s.recv(2048).decode()
                pattern = rf'\b{re.escape(username)}\b'
                colored_response = re.sub(pattern, f"{colorama.Fore.CYAN}{username}{colorama.Style.RESET_ALL}", response)

                print(f"{colored_response}")

                while True:
                    comando = input("Para salir escriba 'exit': ")
                    if comando.lower() == 'exit':
                        c_s.send("exit".encode())
                        break
                
                print("Desconectando...")

            else:
                print("Acción no válida. Por favor, ingresa 'jugar' o 'historial'")
                return

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. Verifica que esté en ejecución.")
    except socket.error as e:
        print(f"Error de socket: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description="Cliente Telnet para conectarse al servidor de juego")
    parser.add_argument('-u','--username', type=str, required=True, help='Tu nombre de usuario')
    parser.add_argument('-p','--password', type=str, required=True, help='Tu contraseña')
    parser.add_argument('-a','--action', type=str, choices=['jugar', 'historial'], default='jugar', help='Acción: jugar o ver historial')
    parser.add_argument('-ip','--ip_version', type=str, choices=['ipv4', 'ipv6'], default='ipv4', help='Especifica si usar IPv4 o IPv6 (por defecto IPv4)')
    
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    telnet_client(args.username, args.password, args.action, args.ip_version)

# python3 cliente.py -u testuser -p testpassword

# python3 cliente.py -u testuser0 -p testpassword -ip ipv6