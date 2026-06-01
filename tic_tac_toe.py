

class TicTacToe:
    #クラス変数として定義
    EMPTY_CELL = " "
    PLAYER_O = "o"
    PLAYER_X = "x"

    def __init__(self):
        self.board = [[self.EMPTY_CELL for _ in range(3)] for _ in range(3)] #空っぽのボードを作成
        self.current_player = self.PLAYER_O #最初のプレイヤーはo

    #プレーヤーの行動を起こす。入力された行動が可能ならボードにo,xを置き、Trueを返す。不可能ならFalse
    def make_move(self, row, col):
        if not (0<=row<=2 and 0<=col<=2):
            return False
        if self.board[row][col] == self.EMPTY_CELL:
            self.board[row][col] = self.current_player

            if self.current_player == self.PLAYER_O:
                self.current_player = self.PLAYER_X
            else:
                self.current_player = self.PLAYER_O
            return True
        else:
            return False
        
    #勝者を返す。
    def check_winner(self):
        # 勝利条件をチェックするヘルパー関数
        def check_line(line):
            if all(cell == self.PLAYER_O for cell in line):
                return self.PLAYER_O
            if all(cell == self.PLAYER_X for cell in line):
                return self.PLAYER_X
            return None

        # 横軸の判定
        for row in self.board:
            winner = check_line(row)
            if winner:
                return winner
        
        # 縦軸の判定
        for col_idx in range(3):
            column = [self.board[row_idx][col_idx] for row_idx in range(3)] #内包表記
            winner = check_line(column)
            if winner:
                return winner
            
        # 斜めの判定
        diagonal1 = [self.board[i][i] for i in range(3)]
        winner = check_line(diagonal1)
        if winner:
            return winner
        
        diagonal2 = [self.board[i][2-i] for i in range(3)]
        winner = check_line(diagonal2)
        if winner:
            return winner
        
        return None
    

class GameController:
    def __init__(self, display_mode=None):
        self.tictactoe = TicTacToe()
        self.display_mode = display_mode #コマンドに表示するかpygameでグラフィックを表示するか、表示なしか

    def display(self):
        #コマンド表示
        if self.display_mode == "console":
            print("  0 1 2 ")
            for i, row in enumerate(self.tictactoe.board):
                print(f"{i} " + "|".join(row))
                if i < 2:
                    print("  -------")

    def get_action(self):
        while True:
            try:
                print(f"Current player is {self.tictactoe.current_player}")
                user_input = input("Enter the row and column value (e.g., '0 1'): ")

                row_str, col_str = user_input.split( )
                row = int(row_str)
                col = int(col_str)

                return row, col

            except ValueError:
                print("ValueError")

    def play_game(self):
        print("===Game start!!===")

        turn = 0
        while turn < 9:
            self.display()
            row, col = self.get_action()
            if self.tictactoe.make_move(row, col):
                turn += 1
            
            winner = self.tictactoe.check_winner()
            if winner == self.tictactoe.PLAYER_O:
                self.display()
                print("o wins!!")
                break
            elif winner == self.tictactoe.PLAYER_X:
                self.display()
                print("x wins!!")
                break

        if turn == 9:
            print("Draw!!")

        print("===Game end===")

if __name__ == "__main__":
    gm = GameController(display_mode="console")
    gm.play_game()
