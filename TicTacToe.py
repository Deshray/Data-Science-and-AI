import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 10
LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
BOARD_COLOR = (200, 200, 200)
CELL_SIZE = WIDTH // 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

def draw_board():
    screen.fill(BACKGROUND_COLOR)
    for x in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT), LINE_WIDTH)
    for y in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE), LINE_WIDTH)

def get_board_pos(x, y):
    return y // CELL_SIZE, x // CELL_SIZE

def tic_tac_toe():
    board = [[" "]*3 for _ in range(3)]
    players = ["X", "O"]
    turn = 0
    last_move = None
    while True:
        draw_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if turn % 2 == 0:
                    player = "X"
                else:
                    player = "O"
                x, y = pygame.mouse.get_pos()
                row, col = get_board_pos(x, y)
                if board[row][col] == " ":
                    board[row][col] = player
                    last_move = (player, row, col)
                    turn += 1
                else:
                    print("That cell is already occupied. Try again.")
        
        for row in range(3):
            for col in range(3):
                if board[row][col] == "X":
                    pygame.draw.line(screen, (255, 0, 0), (col * CELL_SIZE + 30, row * CELL_SIZE + 30), 
                                     ((col + 1) * CELL_SIZE - 30, (row + 1) * CELL_SIZE - 30), 5)
                    pygame.draw.line(screen, (255, 0, 0), ((col + 1) * CELL_SIZE - 30, row * CELL_SIZE + 30), 
                                     (col * CELL_SIZE + 30, (row + 1) * CELL_SIZE - 30), 5)
                elif board[row][col] == "O":
                    pygame.draw.circle(screen, (0, 0, 255), (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 30, 3)
        
        if last_move:
            player, row, col = last_move
            if player == "X":
                pygame.draw.line(screen, (255, 0, 0), (col * CELL_SIZE + 30, row * CELL_SIZE + 30), 
                                 ((col + 1) * CELL_SIZE - 30, (row + 1) * CELL_SIZE - 30), 5)
                pygame.draw.line(screen, (255, 0, 0), ((col + 1) * CELL_SIZE - 30, row * CELL_SIZE + 30), 
                                 (col * CELL_SIZE + 30, (row + 1) * CELL_SIZE - 30), 5)
            elif player == "O":
                pygame.draw.circle(screen, (0, 0, 255), (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 30, 3)

        for player in players:
            if ((board[0][0] == player and board[0][1] == player and board[0][2] == player) or
                (board[1][0] == player and board[1][1] == player and board[1][2] == player) or
                (board[2][0] == player and board[2][1] == player and board[2][2] == player) or
                (board[0][0] == player and board[1][0] == player and board[2][0] == player) or
                (board[0][1] == player and board[1][1] == player and board[2][1] == player) or
                (board[0][2] == player and board[1][2] == player and board[2][2] == player) or
                (board[0][0] == player and board[1][1] == player and board[2][2] == player) or
                (board[0][2] == player and board[1][1] == player and board[2][0] == player)):
                draw_board()
                print(f"Player {player} wins!")
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()

        if turn == 9:
            draw_board()
            print("It's a draw!")
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        pygame.display.update()

tic_tac_toe()
