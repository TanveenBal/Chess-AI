# Chess AI with Alpha-Beta Minimax

This project is a Chess game implemented using Pygame, with a built-in AI. The algorithm used by the AI is Minimax algorithm with Alpha-Beta pruning. Players can play against an AI opponent capable of evaluating board states and making optimal moves. The AI supports dynamic depth evaluation and efficient decision-making.

## Features
- Full implementation of chess rules and mechanics (including moves like castling and en passant).
- Interactive GUI using Pygame.
- AI opponent using the Alpha-Beta Minimax algorithm for decision-making.
- Undo and restart functionality.
- Customizable chess themes and board resets.

## How the AI Works

The Chess AI employs the Alpha-Beta Pruning optimization for the Minimax algorithm, making it an efficient decision-making engine for complex chess positions.

### What is Minimax?

The Minimax algorithm is used in two-player games to determine the best move by simulating all possible moves until a certain depth. It assumes:

- The maximizing player (AI in this case) tries to maximize its advantage.
- The minimizing player (the opponent) tries to minimize the AI’s advantage.

<div style="text-align: center;">
    <img src="src/minimax example.png" alt="Example of the Minimax Algorithm">
    <p style="font-style: italic; margin-top: 8px;">
        Image Source: <a href="https://library.fiveable.me/intermediate-microeconomic-theory/unit-11/sequential-games-subgame-perfect-equilibrium/study-guide/NVlcz0HIm50QivsF" target="_blank">Sequential games and subgame perfect equilibrium</a>
    </p>
</div>

#### At each level of the game tree:

- The maximizing player chooses the move with the highest possible evaluation.
- The minimizing player chooses the move with the lowest possible evaluation.

#### What is Alpha-Beta Pruning?

Alpha-Beta Pruning improves the Minimax algorithm by "pruning" (ignoring) branches of the game tree that do not need to be explored. It tracks two parameters:

- `Alpha`: The best score achievable by the maximizing player (initially set to -∞).
- `Beta`: The best score achievable by the minimizing player (initially set to +∞).

#### Pruning occurs when:

- A branch cannot provide a better outcome than an already evaluated move.
- This reduces the number of evaluations, making the AI faster and able to search deeper into the game tree.

<div style="text-align: center;">
    <img src="src/pruning example.jpeg" alt="Example of the Minimax Algorithm">
    <p style="font-style: italic; margin-top: 8px;">
        Image Source: <a href="A step-by-step guide to building a simple chess AI" target="_blank">A step-by-step guide to building a simple chess AI</a>
    </p>
</div>


## Installation

### Prerequisites

`Python 3.x`

`Pygame`


### Clone the Repository

`git clone https://github.com/TanveenBal/Chess-AI.git`

`cd chess-ai`

### Install Dependencies

`pip install pygame`

### Run the Program

`python main.py`

### Usage

- Use the mouse to select and move pieces.
- Press U to undo a move.
- Press R to reset the board.
- Press T to toggle the chess theme.

AI will automatically play as the opposing side (black team).

## File Structure

```python
├── ai.py            # Chess AI powered by Alpha-Beta Minimax.
├── board.py         # Holds data for state of current board.
├── color.py         # Object to hold colors light and dark.
├── config.py        # Configures the themes, fonts, and sounds.
├── const.py         # Game constants (e.g., board size, colors).
├── dragger.py       # Handles dynamic image movement when dragging pieces.
├── gui.py           # GUI handling for rendering and updates.
├── main.py          # Main game loop and event handling.
├── move.py          # Move mechanics and validations.
├── piece.py         # Chess piece implementation and behavior.
├── sound.py         # Plays and holds the sound of pieces.
├── square.py        # Defines the chessboard squares and state logic.
└── theme.py         # Theme/color of board including movements being made.
```

## Alpha-Beta Minimax AI Code

```python
def minimax(self, board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.game_over():
        return None, self.evaluate(board, "white" if maximizing_player else "black")
    
    best_move = None
    if maximizing_player:
        max_eval = -math.inf
        for move in board.get_moves(self.max_color):
            board.move(move.initial.piece, move)
            current_eval = self.minimax(board, depth - 1, alpha, beta, False)[1]
            board.undo_move()
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = math.inf
        for move in board.get_moves(self.min_color):
            board.move(move.initial.piece, move)
            current_eval = self.minimax(board, depth - 1, alpha, beta, True)[1]
            board.undo_move()
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        return best_move, min_eval
```

Found something wrong in my code or have questions? Feel free to contact me:
- Email: [tanveenbal@gmail.com](tanveenbal@gmail.com)
- LinkedIn: [tanveenbal](https://www.linkedin.com/in/tanveenbal/)