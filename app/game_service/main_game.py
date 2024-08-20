from game import Connect_4

def play():

    game = Connect_4()
    game_running = True

    while game_running:
        game.show_board()

        valid_move = False

        while not valid_move:
            user_move = input(f'Turno del Jugador {game.player_turn()}, Seleccione una columna entre 1 y 8: ')
            try:
                valid_move = game.put_token(int(user_move))
            except:
                print(f'Elija un numero entre 1 y 8')

        game_running = game.winner()

        if game_running != True:
            game.show_board()
            print(game.winner())

if __name__ == '__main__':

    play()