import akhhhh_KInARow as my_agent

# cspell: ignore akhhhh

# Create an instance of OurAgent
agent = my_agent.OurAgent()

# Define a mock game type
class MockGameType:
    def __init__(self, k=3, n=3, m=3):
        self.k = k
        self.n = n
        self.m = m
        self.long_name = "Tic-Tac-Toe"

mock_game_type = MockGameType()
agent.prepare(mock_game_type, 'X', 'Opponent')  # ✅ Ensure the agent is initialized properly

# Define a MockState class to match what `OurAgent` expects
class MockState:
    def __init__(self, board, whose_move):
        self.board = board  # ✅ Matches `state.board`
        self.whose_move = whose_move  # ✅ Matches `state.whose_move`

def test():
    test_board = [
        ['X', 'O', 'X'],
        ['O', 'X', ' '],
        [' ', ' ', 'O']
    ]

    # Use MockState instead of a dictionary
    test_state = MockState(test_board, 'X')  # ✅ Matches what `OurAgent` expects

    print("Static eval result:", agent.static_eval(test_state, agent.current_game_type))  # ✅ Now works

test()
