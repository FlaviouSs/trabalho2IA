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

    game.print_board()


    moves = game.available_moves()

    for move in moves:
        print(move)

    print(len(moves))