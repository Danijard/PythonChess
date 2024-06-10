import pygame

# Define constants
WINDOW_SIZE = 800
SQUARE_SIZE = WINDOW_SIZE // 8
SQUARE_AREA = (WINDOW_SIZE // 8, WINDOW_SIZE // 8)
WHITE_COLOR = (220, 220, 220)
BLACK_COLOR = (100, 60, 60)
GREEN_COLOR = (0, 255, 0)
RED_COLOR = (255, 0, 0)
BLUE_COLOR = (0, 0, 255)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Chess')


# Load pieces images
def load_image(name):
    image = pygame.transform.scale(pygame.image.load(name), SQUARE_AREA)
    return image


# Pieces images
pieces = {
    'r': load_image('figures/black_rook.png'),
    'n': load_image('figures/black_knight.png'),
    'b': load_image('figures/black_bishop.png'),
    'q': load_image('figures/black_queen.png'),
    'k': load_image('figures/black_king.png'),
    'p': load_image('figures/black_pawn.png'),
    'R': load_image('figures/white_rook.png'),
    'N': load_image('figures/white_knight.png'),
    'B': load_image('figures/white_bishop.png'),
    'Q': load_image('figures/white_queen.png'),
    'K': load_image('figures/white_king.png'),
    'P': load_image('figures/white_pawn.png'),
}


class Piece:
    def __init__(self, side, position, board):
        self.board = board
        self.side = side
        self.position = position
        self.image = None
        self.possible_moves = []
        self.is_hovered = False

    def try_move_piece(self):
        pass

    def all_possible_moves(self):
        pass

    def delete_possible_moves(self):
        self.possible_moves = []

class Pawn(Piece):
    def __init__(self, side, position, board):
        super().__init__(side, position, board)
        self.is_moved = False
        self.image = pieces['p' if side == 'black' else 'P']

    def all_possible_moves(self, check_check=True):
        direction = 1 if self.side == 'black' else -1
        opponent_color = 'white' if self.side == 'black' else 'black'

        # Temporary storage for valid moves
        valid_moves = []

        # Check forward moves
        if self.board.is_field_free(self.position[0] + direction, self.position[1]):
            valid_moves.append([self.position[0] + direction, self.position[1]])
            if not self.is_moved and self.board.is_field_free(self.position[0] + 2 * direction, self.position[1]):
                valid_moves.append([self.position[0] + 2 * direction, self.position[1]])

        # Check diagonal captures
        for d_col in [-1, 1]:
            try:
                if self.board.is_field_has_piece_with_color(self.position[0] + direction, self.position[1] + d_col,
                                                            opponent_color):
                    valid_moves.append([self.position[0] + direction, self.position[1] + d_col])
            except IndexError:
                pass

        # Filter valid moves to exclude those leading to check
        if check_check:
            self.possible_moves = [move for move in valid_moves if
                                   not self.board.would_move_cause_check(self.position, move)]

class Rook(Piece):
    def __init__(self, side, position, board):
        super().__init__(side, position, board)
        self.image = pieces['r' if side == 'black' else 'R']
        self.is_moved = False

    def all_possible_moves(self, check_check=True):
        directions = [
            (1, 0),  # UP
            (-1, 0),  # DOWN
            (0, 1),  # RIGHT
            (0, -1)  # LEFT
        ]

        valid_moves = []

        for direction in directions:
            for i in range(1, 8):
                new_row = self.position[0] + i * direction[0]
                new_col = self.position[1] + i * direction[1]

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board.is_field_free(new_row, new_col):
                        valid_moves.append([new_row, new_col])
                    elif self.board.is_field_has_piece_with_color(new_row, new_col,
                                                                  'white' if self.side == 'black' else 'black'):
                        valid_moves.append([new_row, new_col])
                        break
                    else:
                        break
                else:
                    break

        # Filter valid moves to exclude those leading to check
        if check_check:
            self.possible_moves = [move for move in valid_moves if
                                   not self.board.would_move_cause_check(self.position, move)]


class Knight(Piece):
    def __init__(self, side, position, board):
        super().__init__(side, position, board)
        self.image = pieces['n' if side == 'black' else 'N']

    def all_possible_moves(self, check_check=True):
        self.possible_moves = []  # Reset possible moves
        possible_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        valid_moves = []

        for move in possible_moves:
            new_row = self.position[0] + move[0]
            new_col = self.position[1] + move[1]

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                try:
                    if self.board.is_field_free(new_row, new_col):
                        valid_moves.append([new_row, new_col])
                    elif self.board.is_field_has_piece_with_color(new_row, new_col,
                                                                  'white' if self.side == 'black' else 'black'):
                        valid_moves.append([new_row, new_col])
                except IndexError:
                    continue

        # Filter valid moves to exclude those leading to check
        if check_check:
            self.possible_moves = [move for move in valid_moves if
                                   not self.board.would_move_cause_check(self.position, move)]


class Bishop(Piece):
    def __init__(self, side, position, board):
        super().__init__(side, position, board)
        self.image = pieces['b' if side == 'black' else 'B']

    def all_possible_moves(self, check_check=True):
        directions = [
            (1, 1),  # UP-RIGHT
            (-1, -1),  # DOWN-LEFT
            (-1, 1),  # UP-LEFT
            (1, -1)  # DOWN-RIGHT
        ]

        valid_moves = []

        for direction in directions:
            for i in range(1, 8):
                new_row = self.position[0] + i * direction[0]
                new_col = self.position[1] + i * direction[1]

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board.is_field_free(new_row, new_col):
                        valid_moves.append([new_row, new_col])
                    elif self.board.is_field_has_piece_with_color(new_row, new_col,
                                                                  'white' if self.side == 'black' else 'black'):
                        valid_moves.append([new_row, new_col])
                        break
                    else:
                        break
                else:
                    break

        # Filter valid moves to exclude those leading to check
        if check_check:
            self.possible_moves = [move for move in valid_moves if
                                   not self.board.would_move_cause_check(self.position, move)]


class Queen(Piece):
    def __init__(self, side, position, board):
        super().__init__(side, position, board)
        self.image = pieces['q' if side == 'black' else 'Q']

    def all_possible_moves(self, check_check=True):
        directions = [
            (1, 0),  # UP
            (-1, 0),  # DOWN
            (0, 1),  # RIGHT
            (0, -1),  # LEFT
            (1, 1),  # UP-RIGHT
            (-1, -1),  # DOWN-LEFT
            (-1, 1),  # UP-LEFT
            (1, -1)  # DOWN-RIGHT
        ]

        valid_moves = []

        for direction in directions:
            for i in range(1, 8):
                new_row = self.position[0] + i * direction[0]
                new_col = self.position[1] + i * direction[1]

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board.is_field_free(new_row, new_col):
                        valid_moves.append([new_row, new_col])
                    elif self.board.is_field_has_piece_with_color(new_row, new_col,
                                                                  'white' if self.side == 'black' else 'black'):
                        valid_moves.append([new_row, new_col])
                        break
                    else:
                        break
                else:
                    break

        # Filter valid moves to exclude those leading to check
        if check_check:
            self.possible_moves = [move for move in valid_moves if
                                   not self.board.would_move_cause_check(self.position, move)]


class King(Piece):
    def __init__(self, side, position, board):
        super().__init__(side, position, board)
        self.image = pieces['k' if side == 'black' else 'K']
        self.is_moved = False

    def all_possible_moves(self, check_check=True):
        directions = [
            (1, 0),  # UP
            (-1, 0),  # DOWN
            (0, 1),  # RIGHT
            (0, -1),  # LEFT
            (1, 1),  # UP-RIGHT
            (-1, -1),  # DOWN-LEFT
            (-1, 1),  # UP-LEFT
            (1, -1)  # DOWN-RIGHT
        ]

        valid_moves = []

        for direction in directions:
            new_row = self.position[0] + direction[0]
            new_col = self.position[1] + direction[1]

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board.is_field_free(new_row, new_col):
                    valid_moves.append([new_row, new_col])
                elif self.board.is_field_has_piece_with_color(new_row, new_col,
                                                              'white' if self.side == 'black' else 'black'):
                    valid_moves.append([new_row, new_col])

        # Filter valid moves to exclude those leading to check
        if check_check:
            self.possible_moves = [move for move in valid_moves if
                                   not self.board.would_move_cause_check(self.position, move, )]


class Board:
    def __init__(self):
        self.pieces = [
            #[Pawn('black', [1, i], self) for i in range(8)] +
            [
                Rook('black', [0, 0], self), Rook('black', [0, 7], self),
                Knight('black', [0, 1], self), Knight('black', [0, 6], self),
                Bishop('black', [0, 2], self), Bishop('black', [0, 5], self),
                Queen('black', [1, 4], self), King('black', [0, 4], self)
            ],

            #[Pawn('white', [6, i], self) for i in range(8)] +
            [
                Rook('white', [7, 0], self), Rook('white', [7, 7], self),
                Knight('white', [7, 1], self), Knight('white', [7, 6], self),
                Bishop('white', [7, 2], self), Bishop('white', [7, 5], self),
                Queen('white', [7, 3], self), King('white', [7, 4], self)
            ]
        ]

        self.board = [[None for _ in range(8)] for _ in range(8)]
        for piece_color in self.pieces:
            for piece in piece_color:
                self.board[piece.position[0]][piece.position[1]] = piece

        # Start king positions
        self.black_king = self.board[0][4]
        self.white_king = self.board[7][4]

        # All possible moves for black and white pieces in start position
        self.black_possible_moves = []
        self.white_possible_moves = []
        self.temp_black_possible_moves = []
        self.temp_white_possible_moves = []

        # Last moved piece for pawn en passant
        self.last_moved_piece = None

        # Whose turn is it
        self.turn = 'white'

        # Selected piece
        self.selected_field = None

        # Hovered piece
        self.hovered_field = None

    def calculate_possible_moves(self, check_check=True):
        if not check_check:
            self.black_possible_moves = []
            self.white_possible_moves = []
        else:
            self.temp_black_possible_moves = []
            self.temp_white_possible_moves = []
        for color in range(2):
            for piece in self.pieces[color]:
                piece.delete_possible_moves()
                piece.all_possible_moves(check_check)
                if not check_check:
                    if color == 0:
                        self.black_possible_moves += piece.possible_moves
                    else:
                        self.white_possible_moves += piece.possible_moves
                else:
                    if color == 0:
                        self.temp_black_possible_moves += piece.possible_moves
                    else:
                        self.temp_white_possible_moves += piece.possible_moves

    def get_piece(self, row, col):
        return self.board[row][col]

    def is_field_free(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col] is None
        return False

    def is_field_has_piece_with_color(self, row, col, color):
        if 0 <= row < 8 and 0 <= col < 8:
            if self.board[row][col] is not None and self.board[row][col].side == color:
                return True
        return False

    def is_field_under_attack(self, row, col, color_attacker, attacker_moves=None):
        if attacker_moves is None:
            possible_moves = self.white_possible_moves if color_attacker == 'white' else self.black_possible_moves
            for move in possible_moves:
                if move[0] == row and move[1] == col:
                    return True
        elif [row, col] in attacker_moves:
            return True
        return False

    def would_move_cause_check(self, start_pos, end_pos):
        # Save current state
        piece = self.board[start_pos[0]][start_pos[1]]
        target_piece = self.board[end_pos[0]][end_pos[1]]
        start_piece = self.board[start_pos[0]][start_pos[1]]
        if type(piece) == King:
            start_king_position = start_pos

        # Simulate move
        self.board[end_pos[0]][end_pos[1]] = piece
        self.board[start_pos[0]][start_pos[1]] = None
        if type(piece) == King and piece.side == 'black':
            self.black_king.position = end_pos
        elif type(piece) == King and piece.side == 'white':
            self.white_king.position = end_pos
        piece.position = end_pos
        self.calculate_possible_moves(check_check=False)

        # Check if king is in check
        king = self.black_king if piece.side == 'black' else self.white_king
        is_in_check = self.is_field_under_attack(king.position[0], king.position[1], 'white' if piece.side == 'black' else 'black', self.temp_black_possible_moves if piece.side == 'white' else self.temp_white_possible_moves)

        # Revert move
        self.board[start_pos[0]][start_pos[1]] = start_piece
        self.board[end_pos[0]][end_pos[1]] = target_piece
        piece.position = start_pos
        if type(piece) == King and piece.side == 'black':
            self.black_king.position = start_king_position
        elif type(piece) == King and piece.side == 'white':
            self.white_king.position = start_king_position

        return is_in_check


def draw_update(board):
    # Draw board
    for row in range(8):
        for col in range(8):
            color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Draw pieces
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece is not None and not piece.is_hovered:
                screen.blit(piece.image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Draw check highlight
    if board.is_field_under_attack(board.black_king.position[0], board.black_king.position[1], 'white'):
        row, col = board.black_king.position
        pygame.draw.rect(screen, RED_COLOR, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
    if board.is_field_under_attack(board.white_king.position[0], board.white_king.position[1], 'black'):
        row, col = board.white_king.position
        pygame.draw.rect(screen, RED_COLOR, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

    # Draw moves highlight
    if board.selected_field is not None:
        row, col = board.selected_field
        pygame.draw.rect(screen, BLUE_COLOR, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
        for possible_move in board.board[row][col].possible_moves:
            row, col = possible_move
            center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            if board.get_piece(row, col) is not None:
                pygame.draw.rect(screen, GREEN_COLOR, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
            else: pygame.draw.circle(screen, GREEN_COLOR, (center_x, center_y), 10)

    # Draw hovered piece
    if board.hovered_field is not None:
        row, col = board.hovered_field
        piece = board.get_piece(row, col)
        if piece is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Blit the piece image at the mouse position
            screen.blit(piece.image, (mouse_x - SQUARE_SIZE // 2, mouse_y - SQUARE_SIZE // 2))

    pygame.display.flip()


def mouse_hover(board, row, col):
    board.selected_field = [row, col]
    piece = board.get_piece(row, col)

    if piece is not None:
        board.hovered_field = [row, col]
        piece.is_hovered = True
    else:
        board.selected_field = None


def mouse_drop(board, row, col):
    if board.selected_field is not None:
        board.get_piece(board.hovered_field[0], board.hovered_field[1]).is_hovered = False
        board.hovered_field = None
        if board.selected_field != [row, col]:
            pass


def handle_mouse_click(event, board):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        row, col = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
        board.selected_field = [row, col]
        mouse_hover(board, row, col)
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        row, col = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
        if not (0 <= row < 8 and 0 <= col < 8):
            row, col = board.selected_field
        mouse_drop(board, row, col)


def main():
    board = Board()
    board.calculate_possible_moves()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                handle_mouse_click(event, board)
        draw_update(board)

    pygame.quit()


if __name__ == '__main__':
    main()
