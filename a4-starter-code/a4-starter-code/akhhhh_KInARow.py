'''
akhhhh_KInARow.py
Author: Husin, Aaron Kwan
  Example:  
    Authors: Smith, Jane; Lee, Laura

An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

from agent_base import KAgent
from game_types import State, Game_Type
import math
import copy
import random

AUTHORS = 'Aaron Kwan' 

# cspell: ignore evals zobrist autograding akhhhh Husin Kwantum

import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'Kwantum'
        if twin: self.nickname += '2'
        self.long_name = 'Templatus Skeletus' # cspell: ignore Templatus Skeletus
        if twin: self.long_name += ' II'
        self.persona = 'persistent'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet" # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None

    def introduce(self):
        intro = '\nMy name is Templatus Skeletus.\n'+\
            '"An instructor" made me.\n'+\
            'Somebody please turn me into a real game-playing agent!\n'
        if self.twin: intro += "By the way, I'm the TWIN.\n"
        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(
        self,
        game_type,
        what_side_to_play,
        opponent_nickname,
        expected_time_per_move = 0.1, # Time limits can be
                                      # changed mid-game by the game master.

        utterances_matter=True):      # If False, just return 'OK' for each utterance,
                                      # or something simple and quick to compute
                                      # and do not import any LLM or special APIs.
                                      # During the tournament, this will be False..
       if utterances_matter:
           pass
           # Optionally, import your LLM API here.
           # Then you can use it to help create utterances.

           # Aaron's remarks: No LLM API being used here; instead a function that 
           # just chooses random responses based on how good the move is
           
       # Write code to save the relevant information in variables
       # local to this instance of the agent.
       # Game-type info can be in global variables.

       # Store game parameters
       self.long_name = game_type.long_name
       self.playing = what_side_to_play  # 'X' or 'O'
       self.current_game_type = game_type
       self.k = game_type.k  # Win condition (K-in-a-row)
       self.board_size = (game_type.n, game_type.m)  # Board dimensions
       self.expected_time_per_move = expected_time_per_move  # Time constraint

       print("Change this to return 'OK' when ready to test the method.")
       return "OK"
    


   
    # The core of your agent's ability should be implemented here:             
    def make_move(self, current_state, current_remark, time_limit=10,
                  autograding=True, use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        print("make_move has been called")

        # Get legal moves
        legal_moves = self.get_valid_moves(current_state)
    
        if not legal_moves:
            return [[None, current_state], "I can't move anywhere. I'm sorry. Very sorry."]
        
        best_score = -math.inf
        best_move = None
        # alpha, beta = -math.inf, math.inf

        current_player = current_state.whose_move

        # Reset stats
        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0

        # Iterate through possible moves and evaluate using Minimax
        for move in legal_moves:
            new_state = self.make_move_state(current_state, move)
            score, _ = self.minimax(new_state, depth_remaining=3, special_static_eval_fn=special_static_eval_fn)  # Adjust depth as needed

            print(f"Evaluating move {move}: Score = {score}")

            # Maximize for X, minimize for O
            if (current_player == 'X' and score > best_score) or (current_player == 'O' and score < best_score):
                best_score = score
                best_move = move

        chosen_move = best_move if best_move else legal_moves[0] # Choose first move for failsafe

        # TODO: add stats summary to this array
        stats_summary = {
            "evals": self.num_static_evals_this_turn,
            "ab_cutoffs": self.alpha_beta_cutoffs_this_turn,
            "zobrist_entries": self.zobrist_table_num_entries_this_turn,
            "zobrist_hits": self.zobrist_table_num_hits_this_turn
        }
    
        # Generate an utterance for this move
        new_remark = self.utterance_system(best_move, new_state, True, self.k)

        print("Returning from make_move")
        return [[chosen_move, new_state, stats_summary['ab_cutoffs'], stats_summary['evals'], stats_summary['zobrist_entries'], stats_summary['zobrist_hits']], new_remark] if autograding else [[chosen_move, new_state], new_remark]
    


    
    # Organizing the new move state
    def make_move_state(self, state, move):

        new_state = copy.deepcopy(state)
        r,c = move

        new_state.board[r][c] = state.whose_move

        new_state.whose_move = 'O' if state.whose_move == 'X' else 'X'

        return new_state
    



    # Compiling valid moves into one structure
    def get_valid_moves(self, state):
        
        board = state.board
        rows, cols = len(board), len(board[0])
        valid_moves = []
        # directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)] # left, right, up, down, down-right, up-right, down-left, up-left

        # Check all directions for open squares
        
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == ' ':
                    valid_moves.append((r, c))

        print(f"Valid moves generated: {valid_moves}")  # 🔹 Debugging statement

        return valid_moves




    # The main adversarial search function:
    def minimax(self, state, depth_remaining, pruning=False, alpha=None, beta=None, special_static_eval_fn=None):
        print(f"Minimax called with depth: {depth_remaining}, player: {state.whose_move}")
        gtype = self.current_game_type

        # Check terminal state or depth limit
        if depth_remaining == 0 or self.is_terminal(state, gtype):
            self.num_static_evals_this_turn += 1
            if special_static_eval_fn:
                return special_static_eval_fn(state), None
            eval_score = self.static_eval(state, gtype)
            print(f"Leaf node reached: Static evaluation = {eval_score}")
            return eval_score, None  # Return board evaluation and no move

        current_player = state.whose_move
        is_maximizing = (current_player == 'X')

        best_score = -float('inf') if is_maximizing else float('inf')
        best_move = None

        successors = self.generate_successors(state)  # Pre-generate all valid moves
        print(f"Successors at depth {depth_remaining}: {len(successors)}")

        if not successors:  # Handle case where no valid moves exist
            eval_score = self.static_eval(state)
            print(f"Leaf node (no successors) reached: Static evaluation = {eval_score}")
            return eval_score, None

        for move, new_state in successors:
            score, _ = self.minimax(new_state, depth_remaining - 1, pruning, alpha, beta)
            print(f"Evaluating move {move} at depth {depth_remaining}: Score = {score}")

            if is_maximizing:
                if score > best_score:
                    best_score, best_move = score, move  # Ensure best_move is updated
                    print(f"New best move for X at depth {depth_remaining}: {best_move} with score {best_score}")
                if pruning:
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        print("Pruning branch (Alpha-Beta)")
                        break  # Alpha-beta pruning

            else:  # Minimizing player
                if score < best_score:
                    best_score, best_move = score, move  # Ensure best_move is updated
                    print(f"New best move for O at depth {depth_remaining}: {best_move} with score {best_score}")
                if pruning:
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        print("Pruning branch (Alpha-Beta)")
                        break  # Alpha-beta pruning

        print(f"Returning from depth {depth_remaining}: Best move = {best_move}, Best score = {best_score}")
        return best_score, best_move





        #default_score = 0 # Value of the passed-in state. Needs to be computed.
    
        #return [default_score, "my own optional stuff", "more of my stuff"]
        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc. 
 
    def static_eval(self, state, game_type=None):
        print("Currently evaluating static value. Please wait.")
        board = state.board
        rows = len(board)
        cols = len(board[0])
        k = game_type.k if game_type is not None else 3
    
        f_values_x = [0] * k
        f_values_o = [0] * k

        # Formula: f1 + 10f2 + 100f3 + ... + (10^(n-1))fn, where n is k in this case
        # Check all directions
        for r in range(rows):
            for c in range(cols):
                if board[r][c] in ['X', 'O']:
                    player = board[r][c]

                    # Check all directions
                    for i in range(1, k + 1):
                        f_x, f_o = self.count_n_in_a_row(board, r, c, player, i, k, require_open=True)
                        f_values_x[i-1] += f_x
                        f_values_o[i-1] += f_o

        evaluation_score = 0
        for i in range(k):
            evaluation_score += (10**(i)) * (f_values_x[i] - f_values_o[i])

        # returns the value of the function that is used in class for Tic-Tac-Toe
        return evaluation_score
    



    def generate_successors(self, state):
        """
        Generates all possible successor states from the given state.
        """
        successors = []
        valid_moves = self.get_valid_moves(state)  # Get all legal moves

        for move in valid_moves:
            new_state = self.make_move_state(state, move)  # Create a new game state
            successors.append((move, new_state))

        print(f"Generated {len(successors)} successor states.")
        return successors  # Return a list of (move, state) pairs




    def count_n_in_a_row(self, board, r, c, player, n, k, require_open):
        """
        Counts instances of `n` in a row that are unblocked.

        Parameters:
        - board: The game board.
        - r, c: Current position on the board.
        - player: 'X' or 'O'.
        - n: Number of pieces in a row to check.
        - k: The win condition (e.g., 3, 4, 5 in a row).
        - require_open: If true, only count unblocked sequences

        Returns:
        - (x_count, o_count): The count of N-in-a-row sequences for X and O.
        """

        rows, cols = len(board), len(board[0])
        count_x, count_o = 0, 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Down, Right, Diagonal Right, Diagonal Left

        for dr, dc in directions:
            # Build potential N-in-a-row sequence
            sequence = []
            for i in range(n):
                nr, nc = r + i * dr, c + i * dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    sequence.append(board[nr][nc])
                else:
                    break

            # Ensure exactly N pieces of the same player in the sequence
            if len(sequence) == n and all(cell == player for cell in sequence):
                if require_open:
                    # Check if the sequence is unblocked (can be extended)
                    before_r, before_c = r - dr, c - dc
                    after_r, after_c = r + n * dr, c + n * dc

                    before_open = 0 <= before_r < rows and 0 <= before_c < cols and board[before_r][before_c] == ' '
                    after_open = 0 <= after_r < rows and 0 <= after_c < cols and board[after_r][after_c] == ' '

                    if before_open or after_open:  # If at least one side is open
                        if player == 'X':
                            count_x += 1
                        else:
                            count_o += 1
                
                else:
                    # Always count regardless of blockage
                    if player == 'X':
                        count_x += 1
                    else:
                        count_o += 1


        return count_x, count_o
    



    def is_terminal(self, state, game_type):
        """
        Checks if the given game state is a terminal state (win or draw).

        Parameters:
        - state: The current game state (dictionary).

        Returns:
        - True if the game is over (win or draw), False otherwise.
        """
        board = state.board
        k = game_type.k # Number of marks in a row needed to win

        # Check if either player has won
        if self.check_winner(board, 'X', k) or self.check_winner(board, 'O', k):
            return True

        # Check if the board is full (draw)
        if all(cell != ' ' for row in board for cell in row):
            return True  # No empty spaces left → Draw

        return False  # The game is still ongoing




    # Helper for checking terminal state
    def check_winner(self, board, who, k):

        rows, cols = len(board), len(board[0])
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Down, Right, Diagonal Right, Diagonal Left

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == who:
                    for dr, dc in directions:
                        if self.count_n_in_a_row(board, r, c, who, k, k, require_open=False)[0] > 0:
                            return True
        
        return False
    



    def utterance_system(self, move, state, k, is_my_turn):
        """
        Generates an utterance based on the game state.
    
        - `move`: The last move played (row, col).
        - `state`: The current game state after the move.
        - `is_my_turn`: True if it's the agent's turn after the move, False if the opponent just played.
        """
        board = state.board
        last_move_row, last_move_col = move if move is not None else (0,0)
        last_player = 'X' if state.whose_move == 'O' else 'O'  # Who played the last move?
        gtype = self.current_game_type
    
        # Check current evaluation
        eval_score = self.static_eval(state, gtype)

        # TODO: adjust score threshold according to game type (i.e. check if eval_score > 50 or < -50 for TTT)
        # Categorize game state
        if eval_score > (10**k)/2:  # Winning significantly
            game_status = "winning"
        elif eval_score < -(10**k)/2:  # Losing significantly
            game_status = "losing"
        else:
            game_status = "neutral"

        # Define utterances based on context
        my_move_responses = {
            "winning": [
                "I'm in control now!", "This is looking good for me!", "Try to stop me!"
            ],
            "losing": [
                "I need to turn this around.", "This is getting tough!", "You're ahead... for now."
            ],
            "neutral": [
                "Let's see where this leads.", "A solid choice.", "That should work well."
            ]
        }

        opponent_move_responses = {
            "winning": [
                "You're making this too easy!", "I saw that coming!", "A desperate move!"
            ],
            "losing": [
                "Uh-oh, I need a new strategy!", "Nice move, I must admit.", "You're playing well!"
            ],
            "neutral": [
                "Interesting move.", "I see what you're doing.", "Let's see how this plays out."
            ]
        }

        # Choose an utterance based on game status and whether it's the agent's move
        if is_my_turn:
            utterance = random.choice(my_move_responses[game_status])
        else:
            utterance = random.choice(opponent_move_responses[game_status])

        print(f"Utterance after move {move} by {last_player}: {utterance}")
        return utterance
    



    def update_opponent_move(self, last_move, state):
        """
        Generates an utterance based on the opponent's last move.
        """
        if last_move is None:
            return "Let's get started!"

        return self.utterance_system(last_move, state, is_my_turn=False)
    




 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

STATE_A = [' ', ' ', ' ',
           ' ', ' ', ' ',
           ' ', ' ', ' '] # Just starting

def test():
    test_board = [
    ['X', 'O', 'X'],
    ['O', 'X', ' '],
    [' ', ' ', 'O']
    ]

    test_state = State(old=None, initial_state_data=(test_board, 'X'))  # X's turn
    print("Initial Test Board:")
    for row in test_state.board:
        print(row)
    print("Current Player:", test_state.whose_move)

    agent = OurAgent()
    agent.prepare(
        Game_Type(
            long_name="Tic Tac Toe",
            short_name="TTT",
            k=3,
            n=3,
            m=3,
            initial_state_data=(test_board, 'X'),
            turn_limit=10,
            default_time_per_move=5
        ),
        'X',
        'Opponent'
    )
    valid_moves = agent.get_valid_moves(test_state)
    print("Valid moves: ", valid_moves)

    successors = agent.generate_successors(test_state)
    print(f"Generated {len(successors)} successor states.")
    for move, new_state in successors:
        print(f"Move: {move}")
        for row in new_state.board:
            print(row)
        print("Next Player:", new_state.whose_move)
        print("------")

    print("Is terminal state:", agent.is_terminal(test_state, agent.current_game_type))

    eval_score = agent.static_eval(test_state)
    print("Static Evaluation Score:", eval_score)

    best_score, best_move = agent.minimax(test_state, 3)
    print(f"Minimax (Depth 1) - Best Move: {best_move}, Score: {best_score}")  

test()