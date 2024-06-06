import pygame

# Определяем размеры окна и цвета
WINDOW_SIZE = 800
SQUARE_SIZE = WINDOW_SIZE // 8
BLACK_COLOR = (220, 220, 220)
WHITE_COLOR = (100, 60, 60)
HIGHLIGHT_COLOR = (0, 255, 0)
CHECK_COLOR = (255, 0, 0)
DRAW_COLOR = (0, 0, 255)
GAME_OVER_COLOR = (255, 0, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Chess')

# Загрузка изображений фигур
pieces = {
    'r': pygame.transform.scale(pygame.image.load('figures/black_rook.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'n': pygame.transform.scale(pygame.image.load('figures/black_knight.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'b': pygame.transform.scale(pygame.image.load('figures/black_bishop.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'q': pygame.transform.scale(pygame.image.load('figures/black_queen.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'k': pygame.transform.scale(pygame.image.load('figures/black_king.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'p': pygame.transform.scale(pygame.image.load('figures/black_pawn.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'R': pygame.transform.scale(pygame.image.load('figures/white_rook.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'N': pygame.transform.scale(pygame.image.load('figures/white_knight.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'B': pygame.transform.scale(pygame.image.load('figures/white_bishop.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'Q': pygame.transform.scale(pygame.image.load('figures/white_queen.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'K': pygame.transform.scale(pygame.image.load('figures/white_king.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'P': pygame.transform.scale(pygame.image.load('figures/white_pawn.png'), (SQUARE_SIZE, SQUARE_SIZE)),
}

class ChessBoard:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['' for _ in range(8)],
            ['' for _ in range(8)],
            ['' for _ in range(8)],
            ['' for _ in range(8)],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.selected_piece = None
        self.selected_pos = None
        self.possible_moves = []
        self.en_passant_target = None
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.check = False
        self.checkmate = False
        self.current_player = 'white'  # 'white' or 'black'

    def draw_check_indicator(self):
        if self.check:
            king_pos = self.find_king(self.selected_piece.isupper())
            pygame.draw.rect(screen, CHECK_COLOR, pygame.Rect(king_pos[1] * SQUARE_SIZE, king_pos[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
                pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = self.board[row][col]
                if piece:
                    screen.blit(pieces[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
        if self.check:
            king_pos = self.find_king(self.selected_piece.isupper())
            pygame.draw.rect(screen, CHECK_COLOR, pygame.Rect(king_pos[1] * SQUARE_SIZE, king_pos[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

    def draw_highlights(self):
        if self.selected_piece:
            row, col = self.selected_pos
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
            for move in self.possible_moves:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, pygame.Rect(move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

    def draw_game_over(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, GAME_OVER_COLOR)
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        screen.blit(text, text_rect)



    def draw_game_draw(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Draw", True, DRAW_COLOR)
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        screen.blit(text, text_rect)

    def get_piece_moves(self, piece, row, col):
        moves = []
        direction = -1 if piece.isupper() else 1
        if piece.lower() == 'p':
            # Ходы вперед
            if 0 <= row + direction < 8 and not self.board[row + direction][col]:
                moves.append((row + direction, col))
                # Двойной ход вперед с начальной позиции
                if piece.isupper() and row == 6 and not self.board[row - 1][col] and not self.board[row - 2][col]:
                    moves.append((row - 2, col))
                if piece.islower() and row == 1 and not self.board[row + 1][col] and not self.board[row + 2][col]:
                    moves.append((row + 2, col))
            # Взятие по диагонали
            if col - 1 >= 0 and 0 <= row + direction < 8 and self.board[row + direction][col - 1] and self.board[row + direction][col - 1].isupper() != piece.isupper():
                moves.append((row + direction, col - 1))
            if col + 1 < 8 and 0 <= row + direction < 8 and self.board[row + direction][col + 1] and self.board[row + direction][col + 1].isupper() != piece.isupper():
                moves.append((row + direction, col + 1))
            # Взятие на проходе
            if self.en_passant_target:
                target_row, target_col = self.en_passant_target
                if abs(target_col - col) == 1 and target_row == row:
                    moves.append((target_row + direction, target_col))
        elif piece.lower() == 'r':
            # Ходы ладьи
            moves.extend(self.get_linear_moves(row, col, [(1, 0), (-1, 0), (0, 1), (0, -1)]))
        elif piece.lower() == 'n':
            # Ходы коня
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dr, dc in knight_moves:
                if 0 <= row + dr < 8 and 0 <= col + dc < 8 and (not self.board[row + dr][col + dc] or self.board[row + dr][col + dc].isupper() != piece.isupper()):
                    moves.append((row + dr, col + dc))
        elif piece.lower() == 'b':
            # Ходы слона
            moves.extend(self.get_linear_moves(row, col, [(1, 1), (-1, 1), (1, -1), (-1, -1)]))
        elif piece.lower() == 'q':
            # Ходы ферзя
            moves.extend(self.get_linear_moves(row, col, [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]))
        elif piece.lower() == 'k':
            # Ходы короля
            king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            for dr, dc in king_moves:
                if 0 <= row + dr < 8 and 0 <= col + dc < 8 and (not self.board[row + dr][col + dc] or self.board[row + dr][col + dc].isupper() != piece.isupper()):
                    moves.append((row + dr, col + dc))
            # Рокировка
            if (piece.isupper() and self.castling_rights['K']) or (piece.islower() and self.castling_rights['k']):
                if all(self.board[row][col + i] == '' for i in range(1, 3)):
                    moves.append((row, col + 2))
            if (piece.isupper() and self.castling_rights['Q']) or (piece.islower() and self.castling_rights['q']):
                if all(self.board[row][col - i] == '' for i in range(1, 4)):
                    moves.append((row, col - 2))
        return moves

    def get_linear_moves(self, row, col, directions):
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c]:
                    if self.board[r][c].isupper() != self.board[row][col].isupper():
                        moves.append((r, c))
                    break
                moves.append((r, c))
                r += dr
                c += dc
        return moves

    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos[0]][start_pos[1]]
        target = self.board[end_pos[0]][end_pos[1]]
        if piece.lower() == 'k' and abs(start_pos[1] - end_pos[1]) == 2:
            # Рокировка
            if end_pos[1] == 6:
                self.board[start_pos[0]][7] = ''
                self.board[start_pos[0]][5] = 'R' if piece.isupper() else 'r'
            elif end_pos[1] == 2:
                self.board[start_pos[0]][0] = ''
                self.board[start_pos[0]][3] = 'R' if piece.isupper() else 'r'
            self.castling_rights['K' if piece.isupper() else 'k'] = False
            self.castling_rights['Q' if piece.isupper() else 'q'] = False
        elif piece.lower() == 'p' and end_pos == self.en_passant_target:
            # Взятие на проходе
            self.board[start_pos[0]][end_pos[1]] = ''
        elif piece.lower() == 'p' and (end_pos[0] == 0 or end_pos[0] == 7):
            # Превращение пешки
            self.board[end_pos[0]][end_pos[1]] = 'Q' if piece.isupper() else 'q'
        else:
            self.board[end_pos[0]][end_pos[1]] = piece
        self.board[start_pos[0]][start_pos[1]] = ''
        if piece.lower() == 'k':
            self.castling_rights['K' if piece.isupper() else 'k'] = False
            self.castling_rights['Q' if piece.isupper() else 'q'] = False
        elif piece.lower() == 'r':
            if start_pos == (7, 0):
                self.castling_rights['Q'] = False
            elif start_pos == (7, 7):
                self.castling_rights['K'] = False
            elif start_pos == (0, 0):
                self.castling_rights['q'] = False
            elif start_pos == (0, 7):
                self.castling_rights['k'] = False
        self.en_passant_target = None
        if piece.lower() == 'p' and abs(start_pos[0] - end_pos[0]) == 2:
            self.en_passant_target = (start_pos[0] + end_pos[0]) // 2, start_pos[1]

        self.check = self.is_in_check(not piece.isupper())
        self.checkmate = self.is_checkmate(not piece.isupper())
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def find_king(self, white):
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == ('K' if white else 'k'):
                    return row, col
        return None

    def is_in_check(self, white):
        king_pos = self.find_king(white)
        if not king_pos:
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.isupper() != white:
                    if king_pos in self.get_piece_moves(piece, row, col):
                        return True
        return False

    def is_checkmate(self, white):
        if not self.is_in_check(white):
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.isupper() == white:
                    moves = self.get_piece_moves(piece, row, col)
                    for move in moves:
                        board_copy = [row.copy() for row in self.board]
                        self.move_piece((row, col), move)
                        if not self.is_in_check(white):
                            self.board = board_copy
                            return False
                        self.board = board_copy
        return True

    def handle_click(self, pos):
        col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
        piece = self.board[row][col]
        if self.selected_piece and (row, col) in self.possible_moves:
            self.move_piece(self.selected_pos, (row, col))
            self.selected_piece = None
            self.selected_pos = None
            self.possible_moves = []
            return True  # Возвращаем True, если ход был сделан
        elif piece and ((self.current_player == 'white' and piece.isupper()) or (self.current_player == 'black' and piece.islower())):
            self.selected_piece = piece
            self.selected_pos = (row, col)
            self.possible_moves = self.get_piece_moves(piece, row, col)
        else:
            self.selected_piece = None
            self.selected_pos = None
            self.possible_moves = []
        return False  # Возвращаем False, если ход не был сделан

    def count_opponent_moves(self):
        opponent_moves = 0
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.isupper() != (self.current_player == 'white'):
                    opponent_moves += len(self.get_piece_moves(piece, row, col))
                if opponent_moves > 0:
                    break
        return opponent_moves

    def check_game_state(self):
        opponent_moves = self.count_opponent_moves()
        if opponent_moves == 0:
            print("Пат!")
            return False
        return True

# Главный цикл игры
board = ChessBoard()
running = True
game_over = False
draw = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if board.handle_click(pygame.mouse.get_pos()):
                if not ChessBoard.check_game_state(board):
                    draw = True
                if board.checkmate:
                    game_over = True

    board.draw_board()
    board.draw_highlights()
    board.draw_check_indicator()
    
    if game_over:
        board.draw_game_over()
    if draw:
        board.draw_game_draw()
    pygame.display.flip()

pygame.quit()
