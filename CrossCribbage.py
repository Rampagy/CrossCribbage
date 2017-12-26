import BoardGraphics as bg
import ComputeScore as cs
import UserBot as ub
import AIBot as aib
import numpy as np
import TensorAI as tai

def PlayGame(GraphicsOn=True, WriteToFile=True):
    # initialize the game
    board = bg.CribbageBoard(np.random.randint(0, 2))
    card = board.PickCardFromDeck()
    turn_count = 0

    # put the initial card in the middle of the board
    board.AddMoveToBoard('C3')

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

        valid_input = False
        while (not valid_input):
            if (board.GetPlayersTurn() == 0):
                # call AI bot
                move = aib.AIBot(board.GetBoardState(), card, board.GetCardsInCrib(0), 0)
            else:
                # call AI bot
                move = aib.AIBot(board.GetBoardState().transpose(), card, board.GetCardsInCrib(1), 1)
                # only print the card if it is the user's board
                #tai.TensorAI(board.GetBoardState().transpose(), card, board.GetCardsInCrib(1), 1, int(board.crib_owner==1))

                #print(board.DecipherCard(card))
                #move = ub.UserBot(board.GetBoardState().transpose(), card, board.GetCardsInCrib(1))

            if GraphicsOn:
                print(move)

            valid_input = board.AddMoveToBoard(move)

    scores = cs.ScoreGame(board.GetBoardState())
    crib_score = cs.ScoreCrib(board.GetCribRow())
    player0_score, player1_score = scores[0], scores[1]

    if (board.GetCribOwner() == 0):
        player0_score += crib_score
    else:
        player1_score += crib_score

    if WriteToFile:
        board.SaveGameHistory(player0_score, player1_score)

    if GraphicsOn:
        print('\n\nCrib:')
        board.DisplayCrib()
        print('\n')
        print('Player 0 Score: ' + str(player0_score))
        print('Player 1 Score: ' + str(player1_score))
        print('Crib Score: ' + str(crib_score))
