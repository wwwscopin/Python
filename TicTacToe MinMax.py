"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

DRAW = provided.DRAW
PLAYERX = provided.PLAYERX
PLAYERO = provided.PLAYERO
EMPTY = provided.EMPTY


def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if board.check_win() != None:
        return (SCORES.get(board.check_win()), (-1, -1))
    else:
        score = None
        move = None
        for cell in board.get_empty_squares():
            boardc = board.clone()
            boardc.move(cell[0], cell[1], player)
            val,_ = mm_move(boardc, provided.switch_player(player))
            if val*SCORES.get(player) == 1: 
                return (val,cell)
            else:	
                if score == None or score*SCORES.get(player) < val*SCORES.get(player):
                    score = val
                    move = cell   
        return (score, move)

#TTTBoard = provided.TTTBoard 
#print mm_move(TTTBoard(3, False, [[PLAYERX, EMPTY, EMPTY], [PLAYERO, PLAYERO, EMPTY], [EMPTY, PLAYERX, EMPTY]]), PLAYERX)
#print mm_move(TTTBoard(3, False, [[EMPTY, EMPTY, PLAYERX], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]), PLAYERO)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """

    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]


# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
