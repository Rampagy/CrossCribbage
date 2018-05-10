import BoardGraphics as bg
import ComputeScore as cs
import numpy as np
import TensorAI as tai
import UserBot
import tflearn

'''
GraphicsOn = to display graphics
WriteToFile = to save game logs to a file
CompGraph = tf computational graph
session = tensorflow session
'''

def PlayGame(xc_model, GraphicsOn=False, WriteToFile=False, Test=False):
    # initialize the game
    board = bg.CribbageBoard(np.random.randint(0, 2))
    card = board.PickCardFromDeck()
    turn_count = 0

    p0_log = []
    p1_log = []

    # put the initial card in the middle of the board
    board.AddMoveToBoard('C3')

    winner = -1

    # a 'game' has 25 turns - 1 for the initial middle card
    while not (board.IsGameOver()):
        turn_count += 1
        if GraphicsOn:
            print('\n'*20)
            print('\nType "Crib" to put the card in the Crib\n')
            print('Players Turn: ' + str(board.GetPlayersTurn()))
            print('Player ' + str(board.crib_owner) + "'s crib.\n")
            print('Player 0 has ' + str(board.GetCardsInCrib(0)) + ' cards in the crib')
            print('Player 1 has ' + str(board.GetCardsInCrib(1)) + ' cards in the crib')
            print('')
            print('Player 0 ->->->->->->\n')
            board.DisplayGame()

        card = board.PickCardFromDeck()

        invalid_count = 0
        valid_input = False

        while (not valid_input):
            if (board.GetPlayersTurn() == 0):
                # call AI bot as player 0
                obs, move, enc_move = tai.TensorAI(board_state=board.GetBoardState(), card=card,
                            cards_in_crib=board.GetCardsInCrib(0), player=0,
                            crib_owner=int(board.crib_owner==0), predict_model=xc_model)
                p0_log += [[obs, move]]

            else:
                if not Test:
                    # call AI bot as player 1 (normalize board to always be the same direction)
                    obs, move, enc_move = tai.TensorAI(board_state=board.GetBoardState().transpose(),
                                card=card, cards_in_crib=board.GetCardsInCrib(1),
                                player=1, crib_owner=int(board.crib_owner==1), predict_model=xc_model)
                else:
                    # call the user interface bot
                    enc_move = UserBot.GetMove(card)

                p1_log += [[obs, move]]

            if GraphicsOn:
                print(enc_move)

            valid_input = board.AddMoveToBoard(enc_move)

            # increment count if invalid guess
            if not valid_input:
                invalid_count += 1

            if invalid_count >= 1:
                break

        if invalid_count >= 1:
            winner = int(not board.GetPlayersTurn())
            break

    # if a winner has not already been set
    if winner < 0:
        scores = cs.ScoreGame(board.GetBoardState())
        crib_score = cs.ScoreCrib(board.GetCribRow())
        player0_score, player1_score = scores[0], scores[1]

        if (board.GetCribOwner() == 0):
            player0_score += crib_score
        else:
            player1_score += crib_score

        # the player with more points wins (player0 wins in a tie)
        if (player0_score >= player1_score):
            winner = 0
        else:
            winner = 1

        if GraphicsOn:
            print('\n\nCrib:')
            board.DisplayCrib()
            print('\n')
            print('Player 0 Score: ' + str(player0_score))
            print('Player 1 Score: ' + str(player1_score))
            print('Crib Score: ' + str(crib_score))


    win_log = []
    lose_log = []
    if winner == 0:
        win_log = p0_log
        lose_log = p1_log
    else:
        win_log = p1_log
        lose_log = p0_log

    if GraphicsOn:
        print('Player {} wins!'.format(winner))

    if WriteToFile:
        board.SaveGameHistory(player0_score, player1_score)

    return win_log, lose_log # winners moves and losers moves
