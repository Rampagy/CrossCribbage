import BoardGraphics as bg
import ComputeScore as cs
import UserBot as ub
import AIBot as aib

# initialize the game
board = bg.CribbageBoard()
card = board.PickCardFromDeck()
turn_count = 0

# put the initial card in the middle of the board
board.AddMoveToBoard('C3')

# a 'game' has 25 turns - 1 for the initial middle card
while not (board.IsGameOver()):
    turn_count += 1
    print('\n'*50)
    print('\nType "Crib" to put the card in the Crib\n')
    print('Players Turn: ' + str(board.GetPlayersTurn()))
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
            move = aib.AIBot(board.GetBoardState(), card, board.GetCardsInCrib(0))
        else:
            # only print the card if it is the user's board
            print(board.DecipherCard(card))
            move = ub.UserBot(board.GetBoardState(), card, board.GetCardsInCrib(1))

        valid_input = board.AddMoveToBoard(move)


scores = cs.ScoreGame(board.GetBoardState())
crib_score = cs.ScoreCrib(board.GetCribRow())
board.SaveGameHistory(scores[0], scores[1], crib_score)

print('\n\nCrib:')
board.DisplayCrib()
print('\n')
print('Player 0 Score: ' + str(scores[0]))
print('Player 1 Score: ' + str(scores[1]))
print('Crib Score: ' + str(crib_score))
