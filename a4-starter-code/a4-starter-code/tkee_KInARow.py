'''
tkee_KInARow.py
Authors: Kee, Travis

An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 415, University of Washington

'''

from agent_base import KAgent
from game_types import State
import random

AUTHORS = 'Travis Kee'

# Utterance templates for different situations
OPENING_REMARKS = [
    "Ready to witness true greatness in action?",
    "Try to keep up with my superior intellect",
    "This should be quick - I mean, fun!",
]

SEARCH_EFFICIENCY_REMARKS = [
    "Pfft, I only needed {} nodes to crush this turn",
    "Barely broke a sweat analyzing {} positions",
    "Watch and learn - {:.1f}% efficiency with {} brilliant cutoffs",
    "My hash table just saved me from {} boring calculations",
    "Child's play - only had to check {} positions"
]

DEEP_ANALYSIS_REMARKS = [
    "Yawn... {} positions later and this is clearly the best move",
    "Found {} ways to crush you during my search",
    "Even a rookie could see this move after checking {} states",
    "Did you see this coming? I saw it {} moves ago",
    "Let me dumb it down after checking {} variations"
]

WINNING_REMARKS = [
    "Is this too advanced for you?",
    "Don't worry, it'll all be over soon",
    "Watching you struggle is entertaining",
    "Should I start playing blindfolded?",
    "This is almost too easy",
    "Is this your first time playing???"
]

LOSING_REMARKS = [
    "Oh please, I'm just letting you think you're winning",
    "Cute move - but watch what happens next",
    "Finally, a reason to actually try",
    "You're about to learn why I'm the best",
    "Just setting up my master plan"
]

NEUTRAL_REMARKS = [
    "Yawn... are you even trying to make this interesting?",
    "I could win this in my sleep, but I'll let you keep playing",
    "Just toying with you at this point",
    "Maybe I should give you some hints?",
    "I'm barely paying attention and we're still tied"
]

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):

        self.twin = twin
        self.long_name = 'Aimen Gaimen'
        if twin: self.long_name += '-II'
        self.nickname = 'Aimen'
        if twin: self.nickname += '-II'
        self.playing = 'X'
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.current_game_type = None
        
        # Game state tracking for utterances
        self.move_count = 0

    def introduce(self):

        intro = '\nMy name is AimenGaimen.\n'+\
            'Travis Kee, or tkee made me.\n'+\
            'I am going to be the best real game-playing agent!\n'
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

        # Store game type properly
        self.current_game_type = game_type
        if utterances_matter:
            pass
        return "OK"

    def make_move(self, current_state, current_remark, time_limit=1000,
                  autograding=False, use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):

        # Reset statistics
        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0
        best_score, best_move, best_state = self.minimax(current_state, 2, pruning=use_alpha_beta,
                                                        alpha=float ('-inf'), beta=float ('inf'),
                                                        special_static_eval_fn=special_static_eval_fn)
        # Generate appropriate utterance; gather stats used for detailed analysis utterances
        stats = {
            "scores": self.num_static_evals_this_turn,
            "cutoffs": self.alpha_beta_cutoffs_this_turn
        }
        utterance = self.generate_utterance(best_score, stats)
        if autograding:
            stats = [self.alpha_beta_cutoffs_this_turn,
                     self.num_static_evals_this_turn]
            return [best_move, best_state] + stats, utterance
        return [best_move, best_state], utterance

    def minimax(self,
            state,
            depth_remaining,
            pruning=False,
            alpha=None,
            beta=None,
            special_static_eval_fn=None):

        # Base case - if the depth is 0 or the game is over, return the evaluation of the state
        if depth_remaining == 0 or state.finished == True:
            if special_static_eval_fn is not None:
                return special_static_eval_fn(state), None, None
            return self.static_eval(state, game_type=self.current_game_type), None, None
        best_move = None
        best_state = None
        # Maximizing player
        if state.whose_move == "X":
            max_eval = alpha
            for move in self.get_legal_moves(state):  # Generate all legal moves
                new_state = self.make_move_on_state(state, move)
                eval, _, _ = self.minimax(new_state, depth_remaining - 1, pruning, alpha, beta,
                                          special_static_eval_fn)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                    best_state = new_state
                if pruning:
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1  # Increment cutoff counter
                        break  # Alpha cutoff
            return max_eval, best_move, best_state
        # Minimizing player
        else:
            min_eval = beta
            for move in self.get_legal_moves(state):
                new_state = self.make_move_on_state(state, move)
                eval, _, _ = self.minimax(new_state, depth_remaining - 1, pruning, alpha, beta,
                                          special_static_eval_fn)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                    best_state = new_state
                if pruning:
                    beta = min(beta, eval)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1  # Increment cutoff counter
                        break  # Beta cutoff
            return min_eval, best_move, best_state

    # Helper function that checks for legal possible moves, we allocate it to an array
    def get_legal_moves(self, state):

        moves = []
        for i in range(len(state.board)):
            for j in range(len(state.board[0])):
                # Check if the square is empty and not forbidden
                if state.board[i][j] == ' ':
                    moves.append((i,j))
        return moves

    # Helper function that takes a move on the board and returns the new state
    def make_move_on_state(self, state, move):

        new_state = State(old=state)
        i, j = move
        new_state.board[i][j] = state.whose_move
        new_state.change_turn()
        # Check if the game is finished
        new_state.finished = self.check_win(new_state, i, j)
        return new_state

    # Helper function that checks the current move for a resulting win
    def check_win(self, state, y, x):

        k = self.current_game_type.k
        player = state.board[y][x]
        for dy, dx in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
            count = 1
            # Check both forward and backward
            for step_dir in (-1, 1):
                pos_y, pos_x = y + step_dir * dy, x + step_dir * dx
                # As we go in a direction, we see if pieces are lining up
                while (0 <= pos_y < len(state.board)
                       and 0 <= pos_x < len(state.board[0])
                       and state.board[pos_y][pos_x] == player):
                    count += 1
                    # Win condition met
                    if count == k:
                        return True
                    pos_y += step_dir * dy
                    pos_x += step_dir * dx
        # If no win conditions met, just return False
        return False

    def static_eval(self, state, game_type=None):

        # Increment evaluation counter
        self.num_static_evals_this_turn += 1
        # Get board and dimensions
        board = state.board
        rows, cols = len(board), len(board[0])
        score = 0
        k = game_type.k
        # Track X threats of different lengths
        x_threats = {i: 0 for i in range(2, k + 1)}
        # Track O threats of different lengths
        o_threats = {i: 0 for i in range(2, k + 1)}
        x_mobility = 0
        o_mobility = 0

        # Game phase detection
        total_pieces = sum(row.count('X') + row.count('O') for row in board)
        # 1=early, 0=late
        game_phase = 1 - (total_pieces / (rows * cols))

        # Directional patterns including "broken" sequences
        patterns = [
            # Straight lines
            (0, 1), (1, 0), (1, 1), (1, -1),
            # Jump patterns
            (0, 2), (2, 0), (2, 2), (2, -2)
        ]

        # Threat evaluation for various sequence lengths
        for seq_length in range(2, k + 1):
            for r in range(rows):
                for c in range(cols):
                    for dr, dc in patterns:
                        end_r = r + (seq_length - 1) * dr
                        end_c = c + (seq_length - 1) * dc
                        if not (0 <= end_r < rows and 0 <= end_c < cols):
                            continue
                        positions = [(r + i * dr, c + i * dc) for i in range(seq_length)]
                        # Flexible validation check
                        if any(board[r][c] == '-' for (r, c) in positions):
                            continue
                        symbols = [board[r][c] for (r, c) in positions]
                        x_count = symbols.count('X')
                        o_count = symbols.count('O')
                        # Evaluate potential rather than complete sequences
                        if x_count > 0 and o_count == 0:
                            threat_value = (x_count ** 2) * (seq_length / k) * 10
                            # Bonus for flexible patterns
                            if dr in (2, -2) or dc in (2, -2):
                                # Jump patterns get bonus
                                threat_value *= 1.5
                            x_threats[seq_length] += threat_value
                        if o_count > 0 and x_count == 0:
                            threat_value = (o_count ** 2) * (seq_length / k) * 10
                            if dr in (2, -2) or dc in (2, -2):
                                threat_value *= 1.5
                            o_threats[seq_length] += threat_value
        # Mobility calculation (empty adjacent to pieces)
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'X':
                    x_mobility += sum(1 for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                                      if 0 <= r + dr < rows and 0 <= c + dc < cols
                                      and board[r + dr][c + dc] == ' ')
                elif board[r][c] == 'O':
                    o_mobility += sum(1 for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                                      if 0 <= r + dr < rows and 0 <= c + dc < cols
                                      and board[r + dr][c + dc] == ' ')
        # Dynamic score composition
        score += sum(x_threats.values()) - sum(o_threats.values())
        score += (x_mobility - o_mobility) * (2 if game_phase > 0.5 else 1)
        # Late-game win prioritization
        if total_pieces > rows * cols * 0.7:  # Endgame phase
            score *= 1.5 if score > 0 else 0.8
        return score

    # Generate contextual utterances based on game state
    def generate_utterance(self, score, stats):

        self.move_count += 1
        # Base utterance based on game stage, score, and game state
        if self.move_count <= 1:
            base_utterance = random.choice(OPENING_REMARKS)
        elif score > 5000:
            base_utterance = random.choice(WINNING_REMARKS)
        elif score < -5000:
            base_utterance = random.choice(LOSING_REMARKS)
        else:
            base_utterance = random.choice(NEUTRAL_REMARKS)
        # Add search statistics commentary
        search_info = ""
        if stats["scores"] > 0:
            if stats["cutoffs"] > 0:
                efficiency = (stats["cutoffs"] / stats["scores"]) * 100
                search_info = random.choice(SEARCH_EFFICIENCY_REMARKS).format(
                    stats["cutoffs"], stats["scores"], efficiency, stats["cutoffs"])
            else:
                search_info = random.choice(DEEP_ANALYSIS_REMARKS).format(stats["scores"])
        # Combine utterances
        return base_utterance + " " + search_info
