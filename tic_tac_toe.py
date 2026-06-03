import pygame
import sys

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

        if self.display_mode == "graphic": #graphicモードの時pygameを初期化
            pygame.init()
            self.screen_size = 300
            self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
            pygame.display.set_caption("TicTacToe")

            self.board_size = 200
            #ボードの座標
            self.board_x = 50
            self.board_y = 50
            self.board_surface = pygame.Surface((self.board_size, self.board_size)) #ボードを独立したサーフェスに

            self.cell_size = self.board_size // 3

            self.TEXT_COLOR = (0, 255, 0)
            self.font = pygame.font.Font(None, 25)
            
            self.text_x = 0
            self.text_y = 0

            self.BG_COLOR = (255, 255, 255)
            self.BOARD_COLOR = (230,230,150)
            self.LINE_COLOR = (0, 0, 0)
            self.O_COLOR = (0, 0, 255)
            self.X_COLOR = (255, 0, 0)
            



    def display(self):
        #コマンド表示
        if self.display_mode == "console":
            print("  0 1 2 ")
            for i, row in enumerate(self.tictactoe.board):
                print(f"{i} " + "|".join(row))
                if i < 2:
                    print("  -------")
        elif self.display_mode == "graphic":
            self._draw_graphic_board()


    def _draw_graphic_board(self): #pygameでの表示を行う
        self.screen.fill(self.BG_COLOR)
        self.board_surface.fill(self.BOARD_COLOR)

        #ボードの格子を引く
        for i in range(1, 3):
            pos = i * (self.cell_size)
            pygame.draw.line(self.board_surface, self.LINE_COLOR, (0, pos), (self.board_size, pos), 2)
            pygame.draw.line(self.board_surface, self.LINE_COLOR, (pos, 0), (pos, self.board_size), 2)

        #マルバツの表示
        for row in range(len(self.tictactoe.board)):
            for col in range(len(self.tictactoe.board[row])):
                cell = self.tictactoe.board[row][col]
                cell_left = self.cell_size * row
                cell_top = self.cell_size * col
                center_x = cell_left + self.cell_size // 2
                center_y = cell_top + self.cell_size // 2
                margine = self.board_size // 30

                if cell == self.tictactoe.PLAYER_O:
                    pygame.draw.circle(self.board_surface, self.O_COLOR, (center_x, center_y), self.cell_size // 2 - margine, 4)
                if cell == self.tictactoe.PLAYER_X:
                    pygame.draw.line(self.board_surface, self.X_COLOR, (cell_left + margine, cell_top + margine), (cell_left + self.cell_size - margine, cell_top + self.cell_size - margine), 4)
                    pygame.draw.line(self.board_surface, self.X_COLOR, (cell_left + self.cell_size - margine, cell_top + margine), (cell_left + margine, cell_top + self.cell_size - margine), 4)

        #テキストの表示
        winner = self.tictactoe.check_winner()
        if winner == None:
            text = f"Current player is {self.tictactoe.current_player}"
        elif winner == self.tictactoe.PLAYER_O:
            text = "O wins!!"
        elif winner == self.tictactoe.PLAYER_X:
            text = "X wins!!"

        text_surface = self.font.render(text, True, self.TEXT_COLOR)
        
        self.screen.blit(text_surface, (self.text_x, self.text_y))
        self.screen.blit(self.board_surface, (self.board_x, self.board_y))
        pygame.display.update()
        

    def console_get_action(self):
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

    def graphic_get_action(self, mouse_pos):
        mx, my = mouse_pos

        local_x = mx - self.board_x
        local_y = my - self.board_y

        if 0 <= local_x < self.board_size and 0 <= local_y < self.board_size:
            row = local_x // self.cell_size
            col = local_y // self.cell_size

            action = (row, col)
            return action
        return None


    def play_game(self):
        if self.display_mode == "console":
            self._play_console()
        elif self.display_mode == "graphic":
            self._play_graphic()


    def _play_console(self): #コンソールモードのゲームループ
        print("===Game start!!===")

        turn = 0
        while turn < 9:
            self.display()
            row, col = self.console_get_action()
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

    def _play_graphic(self):
        running = True

        while running:
            self.display()
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = event.pos
                        action = self.graphic_get_action(mouse_pos)
                        if action is not None:
                            self.tictactoe.make_move(action[0], action[1])

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    gm = GameController(display_mode="graphic")
    gm.play_game()
