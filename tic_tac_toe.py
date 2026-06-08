import pygame
import sys
from enum import Enum, auto #列挙型

class GameState(Enum):
    PLAYING = auto()
    DRAW = auto()
    WIN_O = auto()
    WIN_X = auto()

class DisplayMode(Enum):
    CONSOLE = auto()
    GRAPHIC = auto()

class Player(Enum):
    O = "O"
    X = "X"
    EMPTY = " "

    #相手プレーヤーを返す。
    @property
    def opponent(self):
        return Player.X if self == Player.O else Player.O

class TicTacToe:
    def __init__(self):
        self.board = [[Player.EMPTY for _ in range(3)] for _ in range(3)] #空っぽのボードを作成
        self.current_player = Player.O #最初のプレイヤーはo
        self.turn = 0
        self.state = GameState.PLAYING

    #プレーヤーの行動を起こす。入力された行動が可能ならボードにo,xを置き、Trueを返す。不可能ならFalse
    def make_move(self, row, col):
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        if self.board[row][col] == Player.EMPTY:
            self.board[row][col] = self.current_player
            self.turn += 1

            self._update_status()
            if self.state == GameState.PLAYING: # 決着がついていなければ交代
                self.current_player = self.current_player.opponent
            return True
        return False
        
    def _update_status(self):
        lines = (
            *self.board, #横すべて
            *zip(*self.board), #縦すべて
            [self.board[i][i] for i in range(3)], #斜め
            [self.board[i][2-i] for i in range(3)] #斜め
        )

        for line in lines:
            if line[0] != Player.EMPTY and all(cell == line[0] for cell in line):
                self.state = GameState.WIN_O if line[0] == Player.O else GameState.WIN_X
                return

        if self.turn == 9:
            self.state = GameState.DRAW

    @property
    def is_over(self):
        return self.state != GameState.PLAYING

class GameController:
    # 定数を整理
    BG_COLOR = (255, 255, 255)
    BOARD_COLOR = (230, 230, 150)
    LINE_COLOR = (0, 0, 0)
    O_COLOR = (0, 0, 255)
    X_COLOR = (255, 0, 0)
    TEXT_COLOR = (0, 255, 0)

    def __init__(self, display_mode=DisplayMode.GRAPHIC):
        self.tictactoe = TicTacToe()
        self.display_mode = display_mode

        if self.display_mode == DisplayMode.GRAPHIC:
            if not pygame.get_init(): pygame.init()
            self.screen_size = 300
            self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
            pygame.display.set_caption("Tic Tac Toe")

            self.board_size = 200
            #ボードの座標
            self.board_x = 50
            self.board_y = 50
            self.board_surface = pygame.Surface((self.board_size, self.board_size)) #ボードを独立したサーフェスに

            self.cell_size = self.board_size // 3
            self.font = pygame.font.Font(None, 25)
            
            #リセットボタン
            self.new_game_button = self.font.render("New game", True, self.TEXT_COLOR)
            self.new_game_rect = self.new_game_button.get_rect()
            self.new_game_rect.center = (self.screen_size // 2, 270)

    def display(self):
        if self.display_mode == DisplayMode.CONSOLE:
            self._draw_console_board()
        elif self.display_mode == DisplayMode.GRAPHIC:
            self._draw_graphic_board()

    def _draw_console_board(self):
            print("  0 1 2 ")
            for i, row in enumerate(self.tictactoe.board):
                print(f"{i} " + "|".join(cell.value for cell in row))
                if i < 2:
                    print("  -------")

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
                cell_left = self.cell_size * col
                cell_top = self.cell_size * row
                center_x = cell_left + self.cell_size // 2
                center_y = cell_top + self.cell_size // 2
                margine = self.board_size // 30

                if cell == Player.O:
                    pygame.draw.circle(self.board_surface, self.O_COLOR, (center_x, center_y), self.cell_size // 2 - margine, 4)
                elif cell == Player.X:
                    pygame.draw.line(self.board_surface, self.X_COLOR, (cell_left + margine, cell_top + margine), (cell_left + self.cell_size - margine, cell_top + self.cell_size - margine), 4)
                    pygame.draw.line(self.board_surface, self.X_COLOR, (cell_left + self.cell_size - margine, cell_top + margine), (cell_left + margine, cell_top + self.cell_size - margine), 4)

        #テキストの表示
        status_messages = {
            GameState.PLAYING: f"Player {self.tictactoe.current_player.value}'s Turn",
            GameState.WIN_O: "O Wins!!",
            GameState.WIN_X: "X Wins!!",
            GameState.DRAW: "It's a Draw!!"
        }
        text = status_messages.get(self.tictactoe.state, "Unknown State")

        text_surface = self.font.render(text, True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.screen_size // 2, 30)



        self.screen.blit(text_surface, text_rect)
        self.screen.blit(self.new_game_button, self.new_game_rect)
        self.screen.blit(self.board_surface, (self.board_x, self.board_y))
        pygame.display.update()

    def reset(self):
        self.tictactoe = TicTacToe()
        

    def console_get_action(self):
        while True:
            try:
                print(f"Current player is {self.tictactoe.current_player.value}")
                user_input = input("Enter the row and column value (e.g., '0 1'): ")

                row, col = map(int, user_input.split( ))

                return row, col

            except ValueError:
                print("Invalid input. Please enter tow numbers (0 2).")

    def graphic_get_action(self, mouse_pos):
        #マウス位置からアクションを返す。ニューゲームボタンクリック時はリセットを実行
        mx, my = mouse_pos
        if self.tictactoe.state == GameState.PLAYING:
            local_x = mx - self.board_x
            local_y = my - self.board_y

            if 0 <= local_x < self.board_size and 0 <= local_y < self.board_size:
                row = local_y // self.cell_size
                col = local_x // self.cell_size

                action = (row, col)
                return action
        
        if self.new_game_rect.collidepoint(mouse_pos):
            self.reset()
        
        return None


    def play_game(self):
        if self.display_mode == DisplayMode.CONSOLE:
            self._play_console()
        elif self.display_mode == DisplayMode.GRAPHIC:
            self._play_graphic()


    def _play_console(self): #コンソールモードのゲームループ
        print("===Game start!!===")

        
        while not self.tictactoe.is_over:
            self.display()
            row, col = self.console_get_action()
            self.tictactoe.make_move(row,col)

        self.display()
        print(f"Result: {self.tictactoe.state.name}")
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
    gm = GameController(display_mode=DisplayMode.GRAPHIC)
    gm.play_game()
