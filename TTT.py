"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 1    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
DRAW = provided.DRAW
PLAYERX = provided.PLAYERX
PLAYERO = provided.PLAYERO
EMPTY = provided.EMPTY
 
# Add your functions here.
def mc_trial(board, player):
    """
     This function takes a current board and the next player to move. 
     The function should play a game starting with the given player 
     by making random moves, alternating between players. 
     The function should return when the game is over.
    """
    while board.check_win() == None:
        empties = board.get_empty_squares()
        if len(empties) > 0:
            empty = random.choice(empties)
            board.move(empty[0], empty[1], player)
            player = provided.switch_player(player)
    
def mc_update_scores(scores, board, player): 
    """
    This function takes a grid of scores (a list of lists) with the same
    dimensions as the Tic-Tac-Toe board, a board from a completed game,
    and which player the machine player is. The function should score 
    the completed board and update the scores grid.  No return!       
    """
    state = board.check_win()
    if state != None and state != DRAW:
        dim = board.get_dim()
        for row in range(dim):
            for col in range(dim):
                status = board.square(row,col)
                if status !=EMPTY:
                    if state == player and status == player and player == PLAYERX \
                    or state != player and status != player and player == PLAYERO:
                        scores[row][col] += MCMATCH
                    elif state == player and status == player and player == PLAYERO \
                    or state != player and status != player and player == PLAYERX:
                        scores[row][col] += MCOTHER
                    elif state != player and status == player and player == PLAYERX \
                    or state == player and status != player and player == PLAYERO:
                        scores[row][col] -= MCMATCH
                    elif state != player and status == player and player == PLAYERO \
                    or state == player and status != player and player == PLAYERX:
                        scores[row][col] -= MCOTHER

def get_best_move(board, scores): 
    """
    This function takes a current board and a grid of scores. The function 
    should find all of the empty squares with the maximum score and randomly 
    return one of them as a (row, column) tuple. 
    """
    empties = board.get_empty_squares()
    if len(empties) > 0:
        temp = [scores[empty[0]][empty[1]] for empty in empties]         
        index = [ ind for ind in range(len(temp)) if temp[ind] == max(temp)]
        return empties[random.choice(index)]

def mc_move(board, player, trials): 
    """
    This function takes a current board, which player the machine player 
    is, and the number of trials to run. The function should use the 
    Monte Carlo simulation to return a move for the machine player
    in the form of a (row, column) tuple. 
    """
    dim = board.get_dim()
    scores =[[0 for dummy_row in range(dim)] for dummy_col in range(dim)] 
            
    for dummy in range(trials):
        board_mc = board.clone()
        mc_trial(board_mc, player)
        mc_update_scores(scores, board_mc, player)

    return get_best_move(board, scores) 

#board=provided.TTTBoard(3, False, [[PLAYERX, EMPTY, EMPTY], [PLAYERO, PLAYERO, EMPTY], [EMPTY, PLAYERX, EMPTY]])
#print mc_move(board, PLAYERX, NTRIALS)

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
