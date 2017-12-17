import numpy as np
import random
import datetime
import time
import ComputeScore as cs

class CribbageBoard:
    def __init__ (self):
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
                self.RecordMove(move, self.picked_card, self.players_turn)
                return True
            else:
                return False
        
        row = ord(move[0].upper())-65
        column = ord(move[1])-49

        if ((column <= 4) and (column >= 0) and (row <= 4) and (row >= 0) and
            (self.cribbage_board[row, column] == 0)):
            
            self.cribbage_board[row, column] = self.picked_card
            self.RecordMove(move, self.picked_card, self.players_turn)
            self.players_turn ^= 1
            return True
        else:
            return False
            

    def DecipherCard(self, card):
        return self.playing_cards[card]


    def GetPlayersTurn(self):
        return self.players_turn


    def RecordMove(self, move, card, player):
        turn = str(len(self.game_history)+1)
        card = str(card)
        player = str(player)
        recorded_move = turn + ":" + player + ":" + card + ":" + move + "\n"
        
        self.game_history.append(recorded_move)


    def SaveGameHistory(self, player0_score, player1_score, crib_score):
        now = time.strftime("%Y_%b_%d_%H_%M_%S", datetime.datetime.now().timetuple())
        
        save_file = open('replay_' + now +'.xcb', 'w')
        for turn in self.game_history:
          save_file.write("%s" % turn)
        save_file.write("\n\nPlayer0Score: " + str(player0_score))
        save_file.write("\nPlayer1Score: " + str(player1_score))
        save_file.write("\nCribScore: "+ str(crib_score))


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



























