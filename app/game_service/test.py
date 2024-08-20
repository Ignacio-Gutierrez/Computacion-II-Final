from game import Connect_4
from unittest.mock import patch

import unittest

class test_game_Connect_4(unittest.TestCase):

    def test_matriz_8x8(self):
        en_linea = Connect_4()
        self.assertEqual(en_linea.board, [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']])

    @patch("builtins.print")
    def test_showboard(self, mockpatched):
        en_linea =  Connect_4()
        en_linea.show_board()
        self.assertEqual(mockpatched.call_count, 90)

    def test_agregar_ficha(self):
        en_linea = Connect_4()
        en_linea.put_token(1)
        self.assertEqual(en_linea.board, [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ']])
    
    def test_agregar_turno_J1(self):
        en_linea = Connect_4()
        self.assertEqual(en_linea.turns, 0)
        self.assertEqual(en_linea.player_turn(), '1')

    def test_agregar_turno_J2_manual(self):
        en_linea = Connect_4()
        en_linea.turns = 1
        self.assertEqual(en_linea.turns, 1)
        self.assertEqual(en_linea.player_turn(), '2')

    def test_agregar_turno_J2_auto(self):
        en_linea = Connect_4()
        en_linea.put_token(1)
        self.assertEqual(en_linea.turns, 1)
        self.assertEqual(en_linea.player_turn(), '2')

    def test_agregar_turno_J1_Turno3(self):
        en_linea = Connect_4()
        en_linea.put_token(1)
        en_linea.put_token(1)
        self.assertEqual(en_linea.turns, 2)
        self.assertEqual(en_linea.player_turn(), '1')
    
    def test_turnos(self):
        en_linea = Connect_4()
        self.assertEqual(en_linea.player_turn(), '1')
        en_linea.put_token(1) #1
        self.assertEqual(en_linea.player_turn(), '2')
        
    def test_agregar_fichas_1a8(self):
        en_linea = Connect_4()
        en_linea.put_token(1) #1
        en_linea.put_token(2) #2
        en_linea.put_token(3) #1
        en_linea.put_token(4) #2
        en_linea.put_token(5) #1
        en_linea.put_token(6) #2
        en_linea.put_token(7) #1
        en_linea.put_token(8) #2
        self.assertEqual(en_linea.board, [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          ['1', '2', '1', '2', '1', '2', '1', '2']])

    def test_gandor_horizontal_player2(self):
        en_linea = Connect_4()
        en_linea.put_token(1) #1
        en_linea.put_token(2) #2
        en_linea.put_token(2) #1
        en_linea.put_token(2) #2
        en_linea.put_token(3) #1
        en_linea.put_token(5) #2
        en_linea.put_token(1) #1
        en_linea.put_token(2) #2
        en_linea.put_token(4) #1
        en_linea.put_token(2) #2
        en_linea.put_token(2) #1
        en_linea.put_token(4) #2
        en_linea.put_token(1) #1
        en_linea.put_token(1) #2
        en_linea.put_token(6) #1
        en_linea.put_token(5) #2
        en_linea.put_token(6) #1
        en_linea.put_token(3) #2
        en_linea.put_token(3) #1
        en_linea.put_token(3) #2
        en_linea.put_token(4) #1
        en_linea.put_token(4) #2
        self.assertEqual(en_linea.board, [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', '1', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', '2', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          ['2', '2', '2', '2', ' ', ' ', ' ', ' '], 
                                          ['1', '2', '1', '1', ' ', ' ', ' ', ' '], 
                                          ['1', '1', '2', '2', '2', '1', ' ', ' '], 
                                          ['1', '2', '1', '1', '2', '1', ' ', ' ']])
        self.assertEqual(en_linea.winner(), 'El Jugador 2 ganó con 4 en Horizontal')

    def test_gandor_horizontal_player1(self):
        en_linea = Connect_4()
        en_linea.put_token(1) #1
        en_linea.put_token(1) #2
        en_linea.put_token(2) #1
        en_linea.put_token(2) #2
        en_linea.put_token(3) #1
        en_linea.put_token(3) #2
        en_linea.put_token(4) #1
        self.assertEqual(en_linea.board, [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          ['2', '2', '2', ' ', ' ', ' ', ' ', ' '], 
                                          ['1', '1', '1', '1', ' ', ' ', ' ', ' ']])
        self.assertEqual(en_linea.winner(), 'El Jugador 1 ganó con 4 en Horizontal')

    def test_gandor_horizontal(self):
        en_linea = Connect_4()
        en_linea.put_token(1) #1
        en_linea.put_token(2) #2
        en_linea.put_token(1) #1
        en_linea.put_token(2) #2
        en_linea.put_token(1) #1
        en_linea.put_token(2) #2
        en_linea.put_token(1) #1
        self.assertEqual(en_linea.board, [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          ['1', '2', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          ['1', '2', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          ['1', '2', ' ', ' ', ' ', ' ', ' ', ' ']])
        self.assertEqual(en_linea.winner(), 'El Jugador 1 ganó con 4 en Vertical')

    def test_gandor_diagonal_n(self):
        en_linea = Connect_4()
        en_linea.put_token(1) #1
        en_linea.put_token(2) #2
        en_linea.put_token(2) #1
        en_linea.put_token(2) #2
        en_linea.put_token(3) #1
        en_linea.put_token(5) #2
        en_linea.put_token(1) #1
        en_linea.put_token(2) #2
        en_linea.put_token(4) #1
        en_linea.put_token(2) #2
        en_linea.put_token(2) #1
        en_linea.put_token(4) #2
        en_linea.put_token(1) #1
        en_linea.put_token(1) #2
        en_linea.put_token(6) #1
        en_linea.put_token(5) #2
        en_linea.put_token(6) #1
        en_linea.put_token(3) #2
        en_linea.put_token(3) #1
        en_linea.put_token(3) #2
        en_linea.put_token(8) #1
        en_linea.put_token(4) #2
        self.assertEqual(en_linea.board, [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', '1', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', '2', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          ['2', '2', '2', ' ', ' ', ' ', ' ', ' '], 
                                          ['1', '2', '1', '2', ' ', ' ', ' ', ' '], 
                                          ['1', '1', '2', '2', '2', '1', ' ', ' '], 
                                          ['1', '2', '1', '1', '2', '1', ' ', '1']])
        self.assertEqual(en_linea.winner(), 'El Jugador 2 ganó con 4 en Diagonal Negativa')

    def test_gandor_diagonal_n2(self):
        en_linea = Connect_4()
        en_linea.board = [['2', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', '2', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', '2', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', '2', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(en_linea.winner(), 'El Jugador 2 ganó con 4 en Diagonal Negativa')

    def test_gandor_diagonal_n3(self):
        en_linea = Connect_4()
        en_linea.board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', '1', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', '1', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', '1', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', '1']]
        self.assertEqual(en_linea.winner(), 'El Jugador 1 ganó con 4 en Diagonal Negativa')

    def test_gandor_diagonal_p(self):
        en_linea = Connect_4()
        en_linea.put_token(4) #1
        en_linea.put_token(5) #2
        en_linea.put_token(2) #1
        en_linea.put_token(3) #2
        en_linea.put_token(3) #1
        en_linea.put_token(4) #2
        en_linea.put_token(4) #1
        en_linea.put_token(5) #2
        en_linea.put_token(3) #1
        en_linea.put_token(6) #2
        en_linea.put_token(2) #1
        en_linea.put_token(6) #2
        en_linea.put_token(6) #1
        en_linea.put_token(5) #2
        en_linea.put_token(5) #1
        self.assertEqual(en_linea.board, [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                          [' ', ' ', ' ', ' ', '1', ' ', ' ', ' '], 
                                          [' ', ' ', '1', '1', '2', '1', ' ', ' '], 
                                          [' ', '1', '1', '2', '2', '2', ' ', ' '], 
                                          [' ', '1', '2', '1', '2', '2', ' ', ' ']])
        self.assertEqual(en_linea.winner(), 'El Jugador 1 ganó con 4 en Diagonal Positiva')

    def test_gandor_diagonal_p2(self):
        en_linea = Connect_4()
        en_linea.board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', '2'], 
                          [' ', ' ', ' ', ' ', ' ', ' ', '2', ' '], 
                          [' ', ' ', ' ', ' ', ' ', '2', ' ', ' '], 
                          [' ', ' ', ' ', ' ', '2', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(en_linea.winner(), 'El Jugador 2 ganó con 4 en Diagonal Positiva')

    def test_gandor_diagonal_p3(self):
        en_linea = Connect_4()
        en_linea.board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                          [' ', ' ', ' ', '1', ' ', ' ', ' ', ' '], 
                          [' ', ' ', '1', ' ', ' ', ' ', ' ', ' '], 
                          [' ', '1', ' ', ' ', ' ', ' ', ' ', ' '], 
                          ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(en_linea.winner(), 'El Jugador 1 ganó con 4 en Diagonal Positiva')

    def test_empate(self):
        en_linea = Connect_4()
        en_linea.board = [['2', '2', '2', '1', '2', '2', '1', '2'], 
                          ['1', '1', '1', '2', '1', '1', '2', '1'], 
                          ['2', '2', '2', '1', '2', '2', '1', '2'], 
                          ['1', '1', '1', '2', '1', '1', '2', '1'], 
                          ['2', '2', '2', '1', '2', '2', '1', '2'], 
                          ['1', '1', '1', '2', '1', '1', '2', '1'], 
                          ['2', '2', '2', '1', '2', '2', '1', '2'], 
                          ['1', '1', '1', '2', '1', '1', '2', '1']]
        self.assertEqual(en_linea.winner(), 'Empate')

    def test_gandor_nowinner_noempate(self):
        en_linea = Connect_4()
        self.assertEqual(en_linea.winner(), True)

if __name__ == '__main__':
    unittest.main()