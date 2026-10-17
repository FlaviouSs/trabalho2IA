from board_breakthrough import BreakThrough
from minimax import minimax_with_hef

def parse_coordinate(coord_str):
    """Converts notation like 'g0' to board indices (6, 0)."""
    coord_str = coord_str.strip().lower()

    if (
        len(coord_str) == 2
        and 'a' <= coord_str[0] <= 'h'
        and '0' <= coord_str[1] <= '7'
    ):
        row = ord(coord_str[0]) - ord('a')
        col = int(coord_str[1])
        return (row, col)

    return None

def parse_move(input_str):
    """Parses user input into a move tuple ((r_org, c_org), (r_dest, c_dest))."""
    # Clean common delimiters: '->', 'to', ',', '-'
    cleaned = (
        input_str.lower()
        .replace('->', ' ')
        .replace('to', ' ')
        .replace('-', ' ')
        .replace(',', ' ')
    )

    parts = cleaned.split()

    if len(parts) == 2:
        src = parse_coordinate(parts[0])
        dst = parse_coordinate(parts[1])

        if src and dst:
            return (src, dst)

    return None

def format_move(move):
    """Formats a move tuple ((6, 0), (5, 0)) into readable chess notation 'g0 -> f0'."""
    (r_org, c_org), (r_dest, c_dest) = move

    return (
        f"{chr(ord('a') + r_org)}{c_org} -> "
        f"{chr(ord('a') + r_dest)}{c_dest}"
    )

def evaluate_breakthrough(board, player):
    rows = len(board)
    cols = len(board[0])

    def closestPieceToWin():
        pieces = []
        # Iterate through rows and columns
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == player:
                    pieces.append((r, c))

        # If the player has no pieces left, return the maximum distance
        if not pieces:
            return rows

        # 'X' wants the smallest row (reaching row 0)
        # 'O' wants the largest row (reaching row 7)
        pieces.sort(key=lambda piece: piece[0], reverse=(player == 'O'))
        best_piece = pieces[0]

        # Calculate remaining distance in rows to reach the winning rank
        distance = best_piece[0] if player == 'X' else (rows - 1 - best_piece[0])
        return distance

    def pieces_alive():
        count = 0
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == player:
                    count += 1
        return count

    # Weights configuration
    PIECE_WEIGHT = 1.0
    DISTANCE_WEIGHT = 100.0 

    min_dist = closestPieceToWin()

    # (min_dist + 1) prevents ZeroDivisionError when a piece reaches distance 0
    proximity_score = DISTANCE_WEIGHT / (min_dist + 1)
    material_score = pieces_alive() * PIECE_WEIGHT

    return material_score + proximity_score


def best_move_minimax(game, depth=3):

    player = game.current
    best_score = float('-inf')
    best_action = None

    for move in game.available_moves():
        new_game = game.copy()
        new_game.make_move(move)

        score = minimax_with_hef(
            game=new_game,
            depth=depth - 1,
            maximizing=False,
            player=player,
            evaluate_fn=evaluate_breakthrough
        )

        if score > best_score:
            best_score = score
            best_action = move

    return best_action



def minimax_agent():
    game = BreakThrough()

    while game.winner() is None:
        game.print_board()

        if game.current == 'X':
            user_input = input("\n[X] Move: ").strip()

            if user_input.lower() in ['quit', 'exit']:
                break

            if user_input.lower() in ['moves', 'help']:
                valid_moves = [format_move(m) for m in game.available_moves()]
                for i in range(0, len(valid_moves), 4):
                    print("  " + "   ".join(valid_moves[i:i + 4]))
                continue

            move = parse_move(user_input)
            if move and move in game.available_moves():
                game.make_move(move)
            else:
                print("Invalid move.\n")

        else:
            print("\n[O] Thinking...")
            ai_move = best_move_minimax(game, depth=3)
            if ai_move:
                game.make_move(ai_move)
                print(f"[O] Played: {format_move(ai_move)}\n")

    winner = game.winner()
    if winner:
        game.print_board()
        print(f"\nGame Over. Winner: [{winner}]")

def main():
    minimax_agent()

if __name__ == "__main__":

    main()