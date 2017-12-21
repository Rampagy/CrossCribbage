import numpy as np
import random
import time
import ComputeScore as cs
import os

class CribbageBoard:
    def __init__ (self, crib_owner_in):
        self.playing_cards = {# no card
                            0: ' X ',
                            # spades
                            1:' A\u2660',
                            2:' 2\u2660',
                            3:' 3\u2660',
                            4:' 4\u2660',
                            5:' 5\u2660',
                            6:' 6\u2660',
                            7:' 7\u2660',
                            8:' 8\u2660',
                            9:' 9\u2660',
                            10:'10\u2660',
                            11:' J\u2660',
                            12:' Q\u2660',
                            13:' K\u2660',
                            # clubs
                            14:' A\u2663',
                            15:' 2\u2663',
                            16:' 3\u2663',
                            17:' 4\u2663',
                            18:' 5\u2663',
                            19:' 6\u2663',
                            20:' 7\u2663',
                            21:' 8\u2663',
                            22:' 9\u2663',
                            23:'10\u2663',
                            24:' J\u2663',
                            25:' Q\u2663',
                            26:' K\u2663',
                            # hearts
                            27:' A\u2665',
                            28:' 2\u2665',
                            29:' 3\u2665',
                            30:' 4\u2665',
                            31:' 5\u2665',
                            32:' 6\u2665',
                            33:' 7\u2665',
                            34:' 8\u2665',
                            35:' 9\u2665',
                            36:'10\u2665',
                            37:' J\u2665',
                            38:' Q\u2665',
                            39:' K\u2665',
                            # diamonds
                            40:' A\u2666',
                            41:' 2\u2666',
                            42:' 3\u2666',
                            43:' 4\u2666',
                            44:' 5\u2666',
                            45:' 6\u2666',
                            46:' 7\u2666',
                            47:' 8\u2666',
                            48:' 9\u2666',
                            49:'10\u2666',
                            50:' J\u2666',
                            51:' Q\u2666',
                            52:' K\u2666'
                            }
        
        self.cribbage_board = np.matrix([[0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0]])

        self.crib = np.array([])
        self.card_deck = random.sample(range(1, len(self.playing_cards)), len(self.playing_cards)-1)
        self.picked_card = 0

        # 0 is player 0 and 1 is player 1
        self.players_turn = 1
        self.player0_cards_in_crib = 0
        self.crib_owner = crib_owner_in
        
        self.game_history = []

    def DisplayGame(self):
        print('   1  2  3  4  5\n', end='')
        
        count = 0
        letter_inc = 65
    
        for row_idx in range(0, len(self.cribbage_board)):
            for col_idx in range(0, len(self.cribbage_board)):
                if (count%5 == 0):
                    print(chr(letter_inc) + ' ', end='')
                    letter_inc += 1
                    count = 0

                print(self.playing_cards[self.cribbage_board[row_idx, col_idx]], end='')

                if (count >= 4):
                    print('\n')
            
                count += 1


    def DisplayCrib(self):
        crib_disp = np.append(self.crib, self.cribbage_board[2, 2])

        for val in crib_disp:
            print(self.playing_cards[val], end=' ')

    
    def PickCardFromDeck(self):
        self.picked_card = self.card_deck[0]
        self.card_deck = self.card_deck[1:len(self.card_deck)]
        return self.picked_card


    def IsGameOver(self):
        if (len(self.crib) < 4):
            return False
        else:
            for i in range(0, len(self.cribbage_board)):
                for j in range(0, len(self.cribbage_board)):
                    if (self.cribbage_board[i, j] == 0):
                        return False

        return True
    
    def AddMoveToBoard(self, move):
        valid_move_found = False
        
        if (self.GetCardsInCrib(self.players_turn) >= 2):
            for i in range(0, len(self.cribbage_board)):
                for j in range(0, len(self.cribbage_board)):
                    if (self.cribbage_board[i, j] == 0):
                        valid_move_found = True
                        break
                if (valid_move_found):
                    break
        else:
            valid_move_found = True


        if (valid_move_found == False):
            self.players_turn ^= 1
            return True

        
        if move.upper() == 'CRIB':
            if ((self.crib.size < 4) and
                (((self.players_turn == 0) and (self.player0_cards_in_crib <= 1)) or
                ((self.players_turn != 0) and (self.crib.size-self.player0_cards_in_crib <= 1)))):
                
                self.crib = np.append(self.crib, np.array([self.picked_card]))
                if (self.players_turn == 0):
                    self.player0_cards_in_crib += 1
                self.RecordMove(self.players_turn, self.cribbage_board, self.picked_card, move.upper())
                return True
            else:
                return False

        if (len(move) != 2):
            return False
            
        row = ord(move[0].upper())-65
        column = ord(move[1])-49

        if ((column <= 4) and (column >= 0) and (row <= 4) and (row >= 0) and
            (self.cribbage_board[row, column] == 0)):

            self.RecordMove(self.players_turn, self.cribbage_board, self.picked_card, move)
            self.cribbage_board[row, column] = self.picked_card
            self.players_turn ^= 1
            return True
        else:
            return False
            

    def DecipherCard(self, card):
        return self.playing_cards[card]


    def GetPlayersTurn(self):
        return self.players_turn


    def RecordMove(self, player, game_state, card, move):
        card = str(card)
        player = str(player)
        rec_game_state = ','.join(str(i) for i in np.squeeze(np.asarray(self.cribbage_board.flatten())).tolist())
        
        rec_move = ''
        if (move != 'CRIB'):
            rec_move = str(5*(ord(move[0])-65) + ord(move[1])-49)
        else:
            rec_move = '25'
        
        recorded_move = player + ":" + rec_game_state + ":" + card + ":" + rec_move
        self.game_history.append(recorded_move)


    def SaveGameHistory(self, player0_score, player1_score):
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(file_path, 'Replays')
        
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
        file_path = os.path.join(file_path, 'replay')
        opt = ''
        if os.path.exists(file_path + '.csv'):
            opt = 'a'
        else:
            opt = 'w'
        
        save_file = open(file_path + '.csv', opt)
        #if new file write a header at the top
        if (opt == 'w'):
            save_file.write('in0,in1,in2,in3,in4,in5,in6,in7,in8,in9,in10,in11,in12,in13,in14,in15,in16,in17,in18,in19,in20,in21,in22,in23,in24,CardToBePlaced,WinningPlayersCrib,' + \
                            'out0,out1,out2,out3,out4,out5,out6,out7,out8,out9,out10,out11,out12,out13,out14,out15,out16,out17,out18,out19,out20,out21,out22,out23,out24,PlaceInCrib\n')

        for turn in self.game_history:
            player, game_state, card, move = turn.split(':')
            
            #produce the truth game state to generate an error in the neural network
            correct_game_state = np.zeros(26)
            if move == 'CRIB':
                correct_game_state[25] = 1
            else:
                correct_game_state[int(move)] = 1
                
            rec_correct_game_state = ','.join(str(int(i)) for i in correct_game_state.tolist())
            
            # only write the winning players moves
            if((player0_score > player1_score) and (player == '0')):
                save_file.write("{0},{1},{2},{3}\n".format(game_state, card, str(int(self.crib_owner==0)), rec_correct_game_state))

            if((player1_score > player0_score) and (player == '1')):
                save_file.write("{0},{1},{2},{3}\n".format(game_state, card, str(int(self.crib_owner==1)), rec_correct_game_state))
                

    def GetCardsInCrib(self, player):
        if (player == 0):
            return self.player0_cards_in_crib
        elif (player == 1):
            return self.crib.size - self.player0_cards_in_crib
        else:
            return 0


    def GetBoardState(self):
        return self.cribbage_board


    def GetCribRow(self):
        return np.append(self.crib, self.cribbage_board[2, 2])


    def GetCribOwner(self):
        return self.crib_owner
























