from board_game import BoardGame

class BreakThrough(BoardGame):
    def __init__(self):
        super().__init__(8, 8)
        
        self.board = [
            ['O'] * self.cols if i < 2
            else [self.current] * self.cols if i >= self.rows - 2
            else [' '] * self.cols
            for i in range(self.rows)
        ]


    def available_moves(self):

        moves = []
        delta_row = 1

        # 'X' starts at the bottom and advances upward (-1); 'O' starts at the top and advances downward (+1)
        if self.current == 'X':
            delta_row = -1

        for r in range(self.rows):
            for c in range(self.cols):

                # Locate a piece belonging to the current player
                if self.board[r][c] == self.current:
                    next_row = r + delta_row

                    # Ensure the destination row is within board boundaries
                    if next_row >= 0 and next_row < self.rows:

                        # Straight forward move
                        if self.board[next_row][c] == ' ':
                            moves.append(((r, c), (next_row, c)))

                        # Diagonal left move
                        if (c - 1) >= 0 and self.board[next_row][c - 1] != self.current:
                            moves.append(((r, c), (next_row, c - 1)))

                        # Diagonal right move
                        if (c + 1) < self.cols and self.board[next_row][c + 1] != self.current:
                            moves.append(((r, c), (next_row, c + 1)))

        return moves


    def make_move(self, move):

        ((r_org, c_org), (r_dest, c_dest)) = move

        # Make the move
        self.board[r_dest][c_dest] = self.board[r_org][c_org]
        self.board[r_org][c_org] = ' '

        # Changes current
        self.current = 'O' if self.current == 'X' else 'X'


    def winner(self):

        if 'X' in self.board[0]:
            return 'X'
        
        if 'O' in self.board[self.rows - 1]:
            return 'O'

        if not self.available_moves():
            return 'O' if self.current == 'X' else 'X'

        return None

    def game_over(self):
        return self.winner() is not None

    def print_board(self):
        # Print column numbers at the top
        print('   ' + ' '.join(map(str, range(self.cols))))

        # Print row letters on both sides of the board
        for i, row in enumerate(self.board):
            letter = chr(ord('a') + i)
            print(letter + ' |' + '|'.join(row) + '| ' + letter)

        # Print column numbers at the bottom
        print('   ' + ' '.join(map(str, range(self.cols))))

if __name__ == "__main__":
    game = BreakThrough()

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

    print("=" * 45)
    print("      BREAKTHROUGH - Interactive Test")
    print("=" * 45)
    print("Commands:")
    print("  • Type move as 'origin destination' (e.g. 'g0 f0' or 'g0->f0')")
    print("  • Type 'moves' to see all legal moves for current player")
    print("  • Type 'quit' to exit\n")

    # Game loop
    while game.winner() is None:
        game.print_board()
        valid_moves = game.available_moves()

        print(
            f"\nTurn: Player [{game.current}] "
            f"({len(valid_moves)} legal moves available)"
        )

        user_input = input("Enter move: ").strip()

        if user_input.lower() in ['quit', 'exit']:
            print("\nGame exited by user.")
            break

        if user_input.lower() in ['moves', 'help', 'list']:
            print("Legal moves:")
            formatted = [format_move(m) for m in valid_moves]

            # Print in columns for readability
            for i in range(0, len(formatted), 4):
                print("  " + "   ".join(formatted[i:i + 4]))

            print()
            continue

        move = parse_move(user_input)

        if move is not None and move in valid_moves:
            game.make_move(move)
            print(f"Executed: {format_move(move)}\n" + "-" * 35)
        else:
            print(
                "\n❌ Invalid move! The move must follow Breakthrough "
                "rules and be in legal moves."
            )
            print("Tip: Type 'moves' to view all possible moves for your turn.\n")

    # Winner announced
    winner = game.winner()

    if winner:
        print("\n" + "=" * 45)
        print(f"🎉 GAME OVER! Winner: Player [{winner}] 🎉")
        print("=" * 45)
        game.print_board()