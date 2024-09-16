import argparse
import socket

import os
import configparser

import sys
import termios

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
            
            if action in ['jugar', 'historial', 'register']:

                c_s.connect((host, port))
                print(f"Conectado a {host}:{port} usando {ip_version.upper()}")

                credentials = f"{username},{password},{action}"
                c_s.send(credentials.encode())
            
                response = c_s.recv(1024).decode()
                print(f"{response}")
                
                if action == 'jugar':
                    print("Esperando a otro jugador...\n")

                    while True:
                        response = c_s.recv(1024).decode()
                        response = response.replace('X', f"{colorama.Fore.CYAN + colorama.Style.BRIGHT}X{colorama.Style.RESET_ALL}")
                        response = response.replace('O', f"{colorama.Fore.MAGENTA + colorama.Style.BRIGHT}O{colorama.Style.RESET_ALL}")
                        print(f"{response}")

                        clear_input_buffer()

                        if 'ganó' in response or 'Te has retirado del juego' in response:
                            break

                        while True:
                            comando = input("--->  ")
                            if comando.lower() == 'exit':
                                break

                            if comando in [str(i) for i in range(1, 9)]:
                                break
                            else:
                                print("Comando inválido, por favor ingresa un número entre 1 y 8")
                                continue

                        c_s.send(comando.encode())

                    print("Desconectando...")

                    c_s.send("exit".encode())

                elif action == 'register':
                    
                    response = c_s.recv(1024).decode()
                    print(f"{response}")

                    if "Usuario ya existe." in response:
                        c_s.send("exit".encode())

                    print("Esperando a otro jugador...\n")

                    while True:
                        response = c_s.recv(1024).decode()
                        response = response.replace('X', f"{colorama.Fore.CYAN + colorama.Style.BRIGHT}X{colorama.Style.RESET_ALL}")
                        response = response.replace('O', f"{colorama.Fore.MAGENTA + colorama.Style.BRIGHT}O{colorama.Style.RESET_ALL}")
                        print(f"{response}")

                        clear_input_buffer()

                        if 'ganó' or 'Te has retirado del juego' in response:
                            break
                        
                        while True:
                            comando = input("--->  ")
                            if comando.lower() == 'exit':
                                break

                            if comando in [str(i) for i in range(1, 9)]:
                                break
                            else:
                                print("Comando inválido, por favor ingresa un número entre 1 y 8")
                                continue
                                
                        c_s.send(comando.encode())

                    print("Desconectando...")


                elif action == 'historial':
                    
                    while True:
                        response = c_s.recv(2048).decode()
                        pattern = rf'\b{re.escape(username)}\b'
                        colored_response = re.sub(pattern, f"{colorama.Fore.CYAN}{username}{colorama.Style.RESET_ALL}", response)

                        print(f"{colored_response}")

                        while True:
                            print("\nPara salir escriba 'exit'")
                            comando = input("Para cambiar de página, ingresa número de página: ")
                            if comando.lower() == 'exit':
                                c_s.send("exit".encode())
                                break
                            elif comando.isdigit():
                                c_s.send(comando.encode())
                                break                                       
                        
                        if comando.lower() == 'exit':
                            break
                    print("Desconectando...")

            else:
                print("Acción no válida. Por favor, ingresa 'jugar' o 'historial'")

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. Verifica que esté en ejecución.")
    except socket.error as e:
        print(f"Error de socket: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        if c_s:
            c_s.close()
            
def clear_input_buffer():
    termios.tcflush(sys.stdin, termios.TCIFLUSH)

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