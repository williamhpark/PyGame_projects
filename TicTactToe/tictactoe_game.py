import pygame
import time

# Size of grid
# sets minimum dimensions, so that the squares don't get too small
WINDOWMULTIPLIER = 5
WINDOWSIZE = 81
# should be a multiple of 27 ideally (3*3*3), to avoid rounding issues
WINDOWWIDTH = WINDOWSIZE * WINDOWMULTIPLIER
WINDOWHEIGHT = WINDOWSIZE * WINDOWMULTIPLIER
SQUARESIZE = int((WINDOWSIZE * WINDOWMULTIPLIER) / 3)

# Size of markers
MARKER_SIZE = 100

# Coordinates of squares (x range, y range)
COORD_RANGE = ((0,SQUARESIZE), (SQUARESIZE,2*SQUARESIZE), (2*SQUARESIZE,3*SQUARESIZE))

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# draws tic-tac-toe grid
def draw_grid():
    # horizontal
    for x in range(0, WINDOWWIDTH, SQUARESIZE):
        pygame.draw.line(SCREEN, BLACK, (x, 0), (x, WINDOWHEIGHT))
    # vertical
    for y in range(0, WINDOWHEIGHT, SQUARESIZE):
        pygame.draw.line(SCREEN, BLACK, (0, y), (WINDOWWIDTH, y))


# displays message passed in to user
def message_to_screen(msg, color, pos):
    screen_text = font.render(msg, True, color)

    # adjust for text length
    # win text position
    if pos == 'w':
        p = [WINDOWWIDTH/2 - 75, WINDOWHEIGHT/2 - 30]
    # tie text position
    elif pos == 't':
        p = [WINDOWWIDTH/2 - 10, WINDOWHEIGHT/2 - 30]
    # restart text position
    elif pos == 'r':
        p = [WINDOWWIDTH/2 - 150, WINDOWHEIGHT/2]

    SCREEN.blit(screen_text, p)


# finds box that mouse is clicked in
def find_box(position):
    x = position[0]
    y = position[1]

    for i in range(0,3):
        if x in range(COORD_RANGE[i][0], COORD_RANGE[i][1]):
            column = i + 1
        if y in range(COORD_RANGE[i][0], COORD_RANGE[i][1]):
            row = i + 1

    if row == 1:
        if column == 1:
            return 1
        elif column == 2:
            return 2
        elif column == 3:
            return 3
    if row == 2:
        if column == 1:
            return 4
        elif column == 2:
            return 5
        elif column == 3:
            return 6
    if row == 3:
        if column == 1:
            return 7
        elif column == 2:
            return 8
        elif column == 3:
            return 9


# draws marker into selected box
def draw_marker(marker, box):
    half = int(SQUARESIZE/2)

    if box in range(1,4):
        y = half
        if box == 1:
            x = half
        elif box == 2:
            x = SQUARESIZE + half
        elif box == 3:
            x = 2*SQUARESIZE + half
    elif box in range(4,7):
        y = SQUARESIZE + half
        if box == 4:
            x = half
        elif box == 5:
            x = SQUARESIZE + half
        elif box == 6:
            x = 2*SQUARESIZE + half
    elif box in range(7,10):
        y = 2*SQUARESIZE + half
        if box == 7:
            x = half
        elif box == 8:
            x = SQUARESIZE + half
        elif box == 9:
            x = 2*SQUARESIZE + half

    # player 1, rectangle marker
    if marker == 'r':
        pygame.draw.rect(SCREEN, RED, (x - 50, y - 50, MARKER_SIZE, MARKER_SIZE))
    # player 2, circle marker
    elif marker == 'c':
        pygame.draw.circle(SCREEN, BLUE, (x, y), int(MARKER_SIZE/2))


# checks if a player has won (True if there is a win, False otherwise)
def win_check(board, mark):
    # horizontal win
    h_win = (mark in board[1] and mark in board[2] and mark in board[3]) or (
            mark in board[4] and mark in board[5] and mark in board[6]) or (
                    mark in board[7] and mark in board[8] and mark in board[9])
    # vertical win
    v_win = (mark in board[1] and mark in board[4] and mark in board[7]) or (
            mark in board[2] and mark in board[5] and mark in board[8]) or (
                    mark in board[3] and mark in board[6] and mark in board[9])
    # diagonal win
    d_win = (mark in board[1] and mark in board[5] and mark in board[9]) or (
            mark in board[3] and mark in board[5] and mark in board[7])

    return h_win or v_win or d_win


# checks if the board is full (True if full, False otherwise)
def full_board_check(board):
    for i in range(1, 10):
        if board[i] == ' ':
            return False
    return True


def main():
    pygame.init()

    # defining font object to font variable
    global font
    font = pygame.font.SysFont('arial', 30)

    global SCREEN
    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Tic-Tac-Toe')

    SCREEN.fill(WHITE)

    # initializing board list
    board = ['#'] + [' ']*9

    running = True
    playing = True

    # keeps track of which player's turn it is
    turn = 1

    while running:
        pygame.time.delay(100)

        draw_grid()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if playing:

                if event.type == pygame.MOUSEBUTTONUP:
                    position = pygame.mouse.get_pos()
                    box = find_box(position)

                    # check if board square is empty
                    if board[box] == ' ':

                        # player 1's turn
                        if turn == 1:
                            board[box] = 'r'
                            draw_marker('r', box)
                            if win_check(board, 'r'):
                                message_to_screen("Player 1 Wins", BLACK, 'w')
                                message_to_screen("Press spacebar to restart", BLACK, 'r')
                                playing = False
                            elif full_board_check(board):
                                message_to_screen("Tie", BLACK, 't')
                                message_to_screen("Press spacebar to restart", BLACK, 'r')
                                playing = False
                            else:
                                turn += 1

                        # player 2's turn
                        else:
                            board[box] = 'c'
                            draw_marker('c', box)
                            if win_check(board, 'c'):
                                message_to_screen("Player 2 Wins", BLACK, 'w')
                                message_to_screen("Press spacebar to restart", BLACK, 'r')
                                playing = False
                            elif full_board_check(board):
                                message_to_screen("Tie", BLACK, 't')
                                message_to_screen("Press spacebar to restart", BLACK, 'r')
                                playing = False
                            else:
                                turn -= 1


            # when not playing
            else:
                # press spacebar to restart game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    playing = True
                    board = ['#'] + [' '] * 9
                    SCREEN.fill(WHITE)
                    draw_grid()
                    turn = 1

            pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

