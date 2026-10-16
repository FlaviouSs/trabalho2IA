from minimax import minimax_with_hef

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
