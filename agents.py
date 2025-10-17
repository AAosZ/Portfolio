from connect_four import State, Game, Player
from copy import deepcopy
from random import randint

DIRECTIONS = {
    "N": (0, 1),
    # "S": (0, -1),
    # "W": (-1, 0),
    "E": (1, 0),
    # "NW": (-1, 1),
    "NE": (1, 1),
    # "SW": (-1, -1),
    "SE": (1, -1)
}

class MinimaxNode:
    """
    One node in the Minimax search tree.

    """
    def __init__(self, state: State, alpha=-1000000, beta=1000000):
        """
        Stores the node's state, (heuristic) value, alpha-beta values, Minimax selection status
        (pruned nodes are not selected), and a dictionary of successor nodes,
        where the keys are possible moves and the values are the successor nodes resulting from those moves

        :param  state: The state associated with this node
        :type state: State
        :param  alpha: Minimax alpha value
        :type state: float
        :param  beta: Minimax beta value
        :type state: float
        """
        self.state = state
        self.was_selected = False
        self.alpha = alpha
        self.beta = beta
        self.value = 0
        self.heur = 0
        self.successors = []

    def __eq__(self, other):
        """
        Recursively compares two MinimaxNodes, producing true if all have the same heuristic value,
        state, and successors. Used by the == operator.

        :param  other: The other MinimaxNode
        :type other: MinimaxNode
        :return: True if the nodes are equal, False otherwise
        :rtype: bool
        """
        return self.state == other.state and self.value == other.value and self.successors == other.successors and \
            self.alpha == other.alpha and self.beta == other.beta



def minimax(node: MinimaxNode, depth: int, max_role: str, heuristic_fn):
    """
    Performs minimax search from the given node out to a maximum depth, when heuristic evaluation is performed.
    Uses alpha-beta pruning. Move ordering is determined by heuristic values.
    Generates a tree of MinimaxNodes rooted at node, with correct state, value, and successors attributes

    :param node: The node that will be the root of this search. After running this function, node will be
    :            modified such that it represents the root of a full Minimax search.
    :type node: MinimaxNode
    :param depth: The search depth. When depth is 0, perform a heuristic evaluation.
    :type depth: int
    :param max_role: The maximizing player
    :type max_role: str (one of 'x' or 'o')
    :param heuristic_fn: The heuristic evaluation function to be used at the max search depth
    :type heuristic_fn: Function (State str -> float), which consumes the state to be evaluated and
    :                   the maximizing player's role (either 'x' or 'o')
    :return: The Minimax value of the given node
    :rtype: float
    """
    state = node.state
    # does this move order in order???

    if node.state.is_terminal or depth == 0:
        node.heur = heuristic_fn(state, max_role)
        node.value = node.heur
        return node.value

    ismax = True if node.state.turn == max_role else False

    moves = node.state.get_legal_moves()
    successors = []

    for move in moves:
        nextboard = state.peek_next_board(move)
        nextturn = 'o' if state.turn == 'x' else 'x'
        nextstate = State(state.num_cols, state.num_rows, nextturn, nextboard)
        succ = MinimaxNode(nextstate, node.alpha, node.beta)
        succ.heur = heuristic_fn(nextstate, max_role)
        successors.append((move, succ))

    # "How do I sort my successors in order?" prompt. ChatGPT, ChatGPT 5 version, OpenAI, 9 Oct. 2025, chat.openai.com/chat.
    if ismax:
        successors.sort(key=lambda x: (-x[1].heur, x[0]))
    else:
        successors.sort(key=lambda x: (x[1].heur, x[0]))
    node.successors = successors
    # END AI CITATION

    # now use lecture pseudocode
    if ismax:
        node.value = float('-inf')
        for (move, succ) in successors:
            succ.alpha = node.alpha
            succ.beta = node.beta

            v = minimax(succ, depth - 1, max_role, heuristic_fn)
            node.value = max(node.value, v)
            node.alpha = max(node.alpha, v)
            if node.alpha >= node.beta:
                break

    else:
        node.value = float('inf')
        for (move, succ) in successors:
            succ.alpha = node.alpha
            succ.beta = node.beta

            v = minimax(succ, depth - 1, max_role, heuristic_fn)
            node.value = min(node.value, v)
            node.beta = min(node.beta, v)
            if node.alpha >= node.beta:
                break

    for (move, succ) in successors:
        if succ.value == node.value:
            succ.was_selected = True

    return node.value

def three_line_heur(state: State, max_role: str):
    """
    Performs a heuristic evaluation of the given state, equal to the number of three-in-a-rows for the
    maximizing player minus the number of three-in-a-rows for the minimizing player.
    If the state is terminal, gives the true evaluation instead (100 if the maximizer has won,
    0 for a draw, or -100 if the minimizer has won)

    :param state: The state to evaluate
    :type state: State
    :param max_role: The role of the maximizing player
    :type max_role: str (one of 'x' or 'o')
    :return: The evaluation of the given state
    :rtype: float
    """
    if max_role == 'x':
        min_role = 'o'
    else:
        min_role = 'x'

    if state.is_terminal:
        return zero_heur(state, max_role)
    else:
        return find_three(state, max_role) - find_three(state, min_role)


def zero_heur(state: State, max_role: str):
    """
    Produces 0 for any non-terminal state.
    If the state is terminal, gives the true evaluation instead (100 if the maximizer has won,
    0 for a draw, or -100 if the minimizer has won)

    :param state: The state to evaluate
    :type state: State
    :param max_role: The role of the maximizing player
    :type max_role: str (one of 'x' or 'o')
    :return: The evaluation of the given state
    :rtype: int
    """

    #If the state is terminal, give the true evaluation
    if state.is_terminal:
        if state.winner == '':
            return 0
        elif state.winner == max_role:
            return 100
        else:
            return -100

    #If the state is not terminal, produce 0
    return 0



def my_heuristic(state: State, max_role: str):
    """
    Performs a heuristic evaluation of the given state.
    If the state is terminal, gives the true evaluation instead (100 if the maximizer has won,
    0 for a draw, or -100 if the minimizer has won)

    :param state: The state to evaluate
    :type state: State
    :param max_role: The role of the maximizing player
    :type max_role: str (one of 'x' or 'o')
    :return: The evaluation of the given state
    :rtype: float
    """
    if state.is_terminal:
        return zero_heur(state, max_role)

    min_role = 'o' if max_role == 'x' else 'x'

    score = 0.0

    for col in range(state.num_cols):
        for row in range(state.num_rows):
            for (dx, dy) in DIRECTIONS.values():
                end_col = col + 3 * dx
                end_row = row + 3 * dy
                if state.coords_legal(end_col, end_row):
                    score += eval(state, col, row, dy, dx, max_role, min_role)

    # "How could I make my heuristic stronger?" prompt. ChatGPT, ChatGPT 5 version, OpenAI, 11 Oct. 2025, chat.openai.com/chat.
    center_col = state.num_cols // 2
    center_bonus = 0
    for r in range(state.num_rows):
        if state.board[center_col][r] == max_role:
            center_bonus += 1
        elif state.board[center_col][r] == min_role:
            center_bonus -= 1
    score += center_bonus * 3.0

    # why do you randomly timeout???
    max_pieces = sum(1 for c in range(state.num_cols) for r in range(state.num_rows) if state.board[c][r] == max_role)
    min_pieces = sum(1 for c in range(state.num_cols) for r in range(state.num_rows) if state.board[c][r] == min_role)
    score += (max_pieces - min_pieces) * 0.5
    # END AT CITATION

    return float(score)


# Helper Functions
# Helper Functions

def find_three(state, role):
    count = 0

    for col in range(state.num_cols):
        for row in range(state.num_rows):
            if state.board[col][row] == role:
                for direction_name, (dx, dy) in DIRECTIONS.items():
                    if (state.coords_legal(col + dx, row + dy) and
                            state.coords_legal(col + 2*dx, row + 2*dy) and
                            state.board[col + dx][row + dy] == role and
                            state.board[col + 2*dx][row + 2*dy] == role):
                        count += 1

    return count

def eval(state, y, x, dy, dx, max_role, min_role):
    max = 0
    min = 0
    empty = 0

    for i in range(4):
        cy = y + i * dy
        cx = x + i * dx

        if state.coords_legal(cy, cx):

            if state.board[cy][cx] == max_role:
                max += 1
            elif state.board[cy][cx] == min_role:
                min += 1
            else:
                empty += 1

    if max > 0 and min > 0:
        return 0

    if max == 4:
        return 100
    elif max == 3 and empty == 1:
        return 20
    elif max == 2 and empty == 2:
        return 10
    elif max == 1 and empty == 3:
        return 1

    if min == 4:
        return -100
    elif min == 3 and empty == 1:
        return -20
    elif min == 2 and empty == 2:
        return -10
    elif min == 1 and empty == 3:
        return -1

    return 0





def print_tree(root: MinimaxNode):
    """
    Prints out a Minimax tree in a human-readable format. Used for debugging.
    Note that IDs are just for readability, and are not part of the actual tree.

    :param root: The root of the Minimax tree to print
    :type root: MinimaxNode
    """
    nextID = 0
    stack = []
    stack.append((nextID, root))
    nextID += 1
    while len(stack) > 0:
        currID, currNode = stack.pop()
        print("Node ID: " + str(currID))
        print("Selected?: " + str(currNode.was_selected))
        print("Minimax Value: " + str(currNode.value))
        print("Heuristic Value: " + str(currNode.heur))
        print("Alpha: " + str(currNode.alpha))
        print("Beta: " + str(currNode.beta))
        succ = []
        temp_list = []
        for (move, s) in currNode.successors:
            succ.append((move, "ID: " + str(nextID)))
            temp_list.append((nextID, s))
            nextID += 1
        for (nodeID, s) in reversed(temp_list):
            stack.append((nodeID, s))

        print("Successors: " + str(succ))
        print("Board:")
        currNode.state.display()
        print()


# def print_tree(root: MinimaxNode):
#     """
#     Prints out a Minimax tree in a human-readable format and returns the string representation.
#     Used for debugging.
#     Note that IDs are just for readability, and are not part of the actual tree.
#
#     :param root: The root of the Minimax tree to print
#     :type root: MinimaxNode
#     :return: String representation of the tree
#     :rtype: str
#     """
#     output = ""
#     nextID = 0
#     stack = []
#     stack.append((nextID, root))
#     nextID += 1
#     while len(stack) > 0:
#         currID, currNode = stack.pop()
#         output += "Node ID: " + str(currID) + "\n"
#         output += "Selected?: " + str(currNode.was_selected) + "\n"
#         output += "Minimax Value: " + str(currNode.value) + "\n"
#         output += "Heuristic Value: " + str(currNode.heur) + "\n"
#         output += "Alpha: " + str(currNode.alpha) + "\n"
#         output += "Beta: " + str(currNode.beta) + "\n"
#         succ = []
#         temp_list = []
#         for (move, s) in currNode.successors:
#             succ.append((move, "ID: " + str(nextID)))
#             temp_list.append((nextID, s))
#             nextID += 1
#         for (nodeID, s) in reversed(temp_list):
#             stack.append((nodeID, s))
#
#         output += "Successors: " + str(succ) + "\n"
#         output += "Board:\n"
#         # Capture the board display as string
#         import io
#         import sys
#         old_stdout = sys.stdout
#         new_stdout = io.StringIO()
#         sys.stdout = new_stdout
#         currNode.state.display()
#         output += new_stdout.getvalue()
#         sys.stdout = old_stdout
#         output += "\n\n"
#
#     return output
























































class MinimaxPlayer(Player):
    """
    An agent that uses minimax to select moves.

    """

    def __init__(self, depth: int, heuristic_fn, display=True):
        """
        Stores minimax parameters

        :param depth: The depth at which search is terminated and a heuristic evaluation is performed
        :type depth: int
        :param heuristic_fn: The heuristic evaluation function to be used at the max search depth
        :type heuristic_fn: Function (State str -> float), which consumes the state to be evaluated and
        :           the maximizing player's role (either 'x' or 'o')
        :param display: If true, print board every play
        :type display: bool
        """
        self.role = ''
        self.depth = depth
        self.heuristic_fn = heuristic_fn
        self.display = display

    def initialize(self, role: str):
        """
        This function is called once for each agent at the beginning of a game, before any moves are made

        :param role: The role of the player
        :type role: str (one of 'x' or 'o')
        """
        self.role = role

    def play(self, state: State):
        """
        This function is called every time it is the player's turn. It produces the column number that a
        piece should be dropped into

        :param state: the game's current State
        :type state: State
        :return: A column number representing a valid move to be played
        :rtype: int
        """
        if self.display:
            state.display()
        root = MinimaxNode(state)
        minimax(root, self.depth, self.role, self.heuristic_fn)
        best_move = -1
        best_value = 0
        for (move, succ) in root.successors:
            if succ.was_selected:
                if best_move == -1 or succ.value > best_value:
                    best_move = move
                    best_value = succ.value
        return best_move



class FirstMovePlayer(Player):
    """
    An agent that always plays the first legal move.

    """

    def initialize(self, role: str):
        pass

    def play(self, state: State):
        state.display()
        return state.get_legal_moves()[0]



class RandomPlayer(Player):
    """
    An agent that always plays a random move.

    """

    def initialize(self, role: str):
        pass

    def play(self, state: State):
        state.display()
        moves = state.get_legal_moves()
        return moves[randint(0,len(moves)-1)]


class HumanPlayer(Player):
    """
    An agent that allows you to play by keyboard input!

    """

    def initialize(self, role: str):
        pass

    def play(self, state: State):
        state.display()
        moves = state.get_legal_moves()
        valid = False
        col = -1
        while not valid:
            str = input("Enter a column number in the range [0,6]: ")
            try:
                col = int(str)
                if col in moves:
                    valid = True
                else:
                    print("Selected column is not valid.")
            except ValueError:
                print("Unable to parse input.")
        return col



if __name__ == "__main__":

    # This is the code that gets run when you run this file. You can set up games to be played here.

    # Here are some more examples of game initialization:
    # game = Game(MinimaxPlayer(4, three_line_heur), MinimaxPlayer(4, zero_heur))
    # game = Game(RandomPlayer(), FirstMovePlayer())

    # Notice that "o" is MAX, even though it is "x"'s turn.
    # Also, the board appears sideways because of the [col][row] indexing
    test_state = State(7, 6, 'o', [['x', 'x', 'x', 'o', 'x', 'o'],
                                   ['x', 'x', 'o', 'x', 'x', 'o'],
                                   ['o', 'x', 'x', 'x', 'o', 'o'],
                                   ['x', 'o', 'x', 'o', 'x', 'x'],
                                   ['o', 'o', 'x', 'o', '.', '.'],
                                   ['o', 'x', 'o', 'o', 'x', '.'],
                                   ['o', 'o', '.', '.', '.', '.']])

    root = MinimaxNode(deepcopy(test_state))
    result = minimax(root, 3, 'x', three_line_heur)

    print("Result of minimax: " + str(result))
    print()
    print("Resulting tree:")
    print_tree(root)
    game = Game(HumanPlayer(), RandomPlayer())
    winner = game.play_game()
    game.display()

# root = MinimaxNode(deepcopy(test_state))
# result = minimax(root, 3, 'x', three_line_heur)
#
# print("Result of minimax: " + str(result))
# print()
# print("Resulting tree:")
# tree_output = print_tree(root)
# with open("file_results.txt", "w") as file:
#     file.write(tree_output)
