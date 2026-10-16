from board_game import BoardGame

class BreakThrough(BoardGame):
    def __init__(self):
        super().__init__(8, 8)
        
        self.board = [
            ['O'] * self.cols if i < 2
            else ['X'] * self.cols if i >= self.rows - 2
            else [' '] * self.cols
            for i in range(self.rows)
        ]


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
