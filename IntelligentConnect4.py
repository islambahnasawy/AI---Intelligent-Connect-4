import pygame
import time
import random
import numpy as np
import sys
import math



##//////////////////////////////////////////////////////////////
## declaring some constants to be used
##//////////////////////////////////////////////////////////////
## used colors

BLUE = (30, 141, 255)
Dark_blue = (17,34,51)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

red = (200, 0, 0)
light_red = (255, 0, 0)

yellow = (200, 200, 0)
light_yellow = (255, 255, 0)

green = (34, 177, 76)
light_green = (0, 255, 0)

c4 = pygame.image.load('C4_rr.jpg')

## rows & columns
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

SQUARESIZE = 100
# display_width = 800
# display_height = 600
display_width = COLUMN_COUNT * SQUARESIZE
display_height = (ROW_COUNT + 1) * SQUARESIZE
size = (display_width, display_height)
RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

# def score(score):
#     text = smallfont.render("Score: " + str(score), True, black)
#     gameDisplay.blit(text, [0, 0])

##//////////////////////////////////////////////////////////////
## create and display text or message
def free_text(text, color, size="small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()

def display_message(msg, color, y_displace=0, size="small"):
    textSurf, textRect = free_text(msg, color, size)
    textRect.center = (int(display_width / 2), int(display_height / 2) + y_displace)
    gameDisplay.blit(textSurf, textRect)

##//////////////////////////////////////////////////////////////
## create buttom

def text_to_button(msg, color, buttonx, buttony, buttondisplay_width, buttondisplay_height, size="small"):
    textSurf, textRect = free_text(msg, color, size)
    textRect.center = ((buttonx + (buttondisplay_width / 2)), buttony + (buttondisplay_height / 2))
    gameDisplay.blit(textSurf, textRect)

def button(text, x, y, display_width, display_height, inactive_color, active_color, action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x + display_width > cur[0] > x and y + display_height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, display_width, display_height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()

            if action == "info":
                game_info()

            if action == 'back':
                game_intro()

            if action == "select":
                game_select()

            if action == "play":
                Connect4Loop()

            if action == "AIplay":
                AIConnect4()

    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, display_width, display_height))

    text_to_button(text, black, x, y, display_width, display_height)


def image_display():
    gameDisplay.blit(c4, (0,display_height * 0.17))

##//////////////////////////////////////////////////////////////
## create matrix represents the board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

##//////////////////////////////////////////////////////////////
## give matrix element a number (1 or 2) to represent dropping piece to the board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

##//////////////////////////////////////////////////////////////
## check if it's a valid location to drop a piece or not
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

##//////////////////////////////////////////////////////////////
## this fn takes the current column and the board then returns the next open row in this column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

##//////////////////////////////////////////////////////////////
##Printing the matrix to represent the board
def print_board(board):
    print(np.flip(board, 0))

##//////////////////////////////////////////////////////////////
## check if the last move was a winning move
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


##//////////////////////////////////////////////////////////////
## this fn draws the board on GUI
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, Dark_blue, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, white, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 0:
                pygame.draw.circle(screen, white, (
                int(c * SQUARESIZE + SQUARESIZE / 2), display_height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), display_height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), display_height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

##//////////////////////////////////////////////////////////////
## this fn clears the board for the next game
def clear_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            board[r][c] == 0
    pygame.display.update()
    pygame.time.wait(100)

##//////////////////////////////////////////////////////////////
## this fn evaluates the window (board) and returns score value that represent the situation
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

##//////////////////////////////////////////////////////////////
## check the stoping state, if it's a terminal node
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

##//////////////////////////////////////////////////////////////
## the minimax utility fanction
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


##//////////////////////////////////////////////////////////////
## gets all valid locations in an array
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def Connect4Loop():
    board = create_board()
    clear_board(board)
    draw_board(board)
    pygame.display.update()
    game_over = False
    turn = 0
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, white, (0, 0, display_width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, white, (0, 0, display_width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = myfont.render("Player 1 wins!", 1, red)
                            screen.blit(label, (40, 10))
                            game_over = True


                # # Ask for Player 2 Input
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins!", 1, yellow)
                            screen.blit(label, (40, 10))
                            game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)

def AIConnect4():
    board = create_board()
    clear_board(board)
    draw_board(board)
    pygame.display.update()
    game_over = False
    turn = random.randint(PLAYER, AI)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, white, (0, 0, display_width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, white, (0, 0, display_width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Player 1 wins!!", 1, red)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        # # Ask for Player 2 Input
        if turn == AI and not game_over:

            # col = random.randint(0, COLUMN_COUNT-1)
            # col = pick_best_move(board, AI_PIECE)
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                # pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Game Over!!", 1, BLACK)
                    screen.blit(label, (100, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)




def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:

                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        image_display()
        display_message("Welcome to our Connect 4!", green, -280, size="large")
        display_message("Click play to start game.", black, 200)
        # display_message("Press C to play, P to pause or Q to quit",black,180)

        button("play", 80, 600, 100, 50, green, light_green, action="select")
        #button("1 player", 150, 600, 100, 50, green, light_green, action="AIplay")
        button("info", 300, 600, 100, 50, yellow, light_yellow, action="info")
        button("quit", 520, 600, 100, 50, red, light_red, action="quit")

        pygame.display.update()

        clock.tick(15)

def game_info():
    info = True

    while info:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    info = False
                elif event.key == pygame.K_q:

                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        display_message("Intelligent Connect 4!", green, -120, size="large")
        display_message("This game has been developed by a CSE student at the faculty", black, -50)
        display_message("of Engineering, Ain Shams Uni. 2019/2018 as a bonus project", black, -10)
        display_message("in AI course, introduced by Dr. Manal Mourad and with", black, 30)
        display_message("the aid of our teaching assistants:", black, 70)
        display_message("Eng. Youmna Hesham and Eng. Ahmed Fathy.", black, 110)

        # display_message("Press C to play, P to pause or Q to quit",black,180)

        button("back", 550, 530, 100, 50, Dark_blue, BLUE, action="back")

        pygame.display.update()

        clock.tick(15)

def game_select():
    select = True

    while select:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    select = False
                elif event.key == pygame.K_q:

                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        display_message("Intelligent Connect 4!", green, -180, size="large")
        display_message("Please, select 1 player or 2 players", black, -90)

        button("1 player", 200, 320, 100, 50, yellow, light_yellow, action="AIplay")
        button("2 players", 390, 320, 100, 50, red, light_red, action="play")
        button("back", 550, 530, 100, 50, Dark_blue, BLUE, action="back")

        pygame.display.update()

        clock.tick(15)

pygame.init()

smallfont = pygame.font.SysFont("comicsansms", 20)
medfont = pygame.font.SysFont("comicsansms", 40)
largefont = pygame.font.SysFont("comicsansms", 50)
myfont = pygame.font.SysFont("monospace", 75)
pygame.display.set_caption('Intelligent Connect 4')

game_intro()
