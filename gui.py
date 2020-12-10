import pygame
import time
import sys

arg_count = len(sys.argv)
if (arg_count != 3) and sys.argv[1] != "-dim":
    print("""
          # usage
          python gui.py [-dim <board_dimension>]

          @flag
          -dim : sets dimension of board
          """)
    sys.exit()

elif sys.argv[1] == "-dim":
    board_dim = int(sys.argv[2])


# init pygame
pygame.init()

# Constants
display_width = 684
display_height = 784
board_width = display_width
board_height = display_height - 100
square_size = board_width / board_dim

game_quit = False

# Colors
white = (255, 255, 255)
black = (8, 28, 21)
red = (255, 0, 0)
green = (51	, 100,	51)
blue = (100, 100, 100)
yellow = (255, 213, 0)
background = (241, 250, 238)
button = (29, 53, 87)
wood_light = (151, 157, 172)
wood_dark = (4, 102, 200)

gameDisplay = pygame.display.set_mode((display_width, display_height))
gameDisplay.fill(white, rect=(0, 0, display_width, display_height))
board = pygame.Surface((board_width, board_height))

pygame.display.set_caption('GhostBuster')
clock = pygame.time.Clock()


def show_text(msg, x, y, size, color, font=pygame.font.get_default_font(), sysfont=True):
    if sysfont:
        font = pygame.font.SysFont(font, size)
    else:
        font = pygame.font.Font(font, size)
    TextSurf = font.render(msg, True, color)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((x), (y))
    gameDisplay.blit(TextSurf, TextRect)


def draw_board():
    w = (board_width / board_dim)
    h = (board_height / board_dim)
    inner = 3
    for x in range(0, board_dim):
        for y in range(0, board_dim):
            # color = wood_light if (x+y) % 2 == 0 else wood_dark
            pygame.draw.rect(board, wood_light, (y * w, x * w, w-2, h-2))
            pygame.draw.rect(board, wood_dark, (y * w + inner, x * w + inner,
                                                w - 2*inner, h-2*inner))

    gameDisplay.blit(board, (0, 100))


def change_color(x, y, color):
    w = board_width / board_dim
    h = board_height / board_dim
    inner = 3

    # color = wood_light if (x+y) % 2 == 0 else wood_dark
    pygame.draw.rect(board, color, (y * w + inner, x * w + inner,
                                    w - 2 * inner, h - 2 * inner))
    gameDisplay.blit(board, (0, 100))


def show_probability(bust_X=-1, bust_Y=-1):
    for i in range(board_dim):
        for j in range(board_dim):
            if i == bust_X and j == bust_Y:
                centerY = 100 + (i * square_size)+0.5*square_size
                centerX = (j * square_size)+0.5*square_size
                show_text("",centerX, centerY, 20, black, "magneto")

            else:
                centerY = 100 + (i * square_size)+0.5*square_size
                centerX = (j * square_size)+0.5*square_size
                show_text(str(round(probability[i][j], 2)),
                          centerX, centerY, 20, black, "magneto")
            

button_width, button_height, time_x, bust_x, button_y = 140, 50, 180, 380, 25
pygame.draw.rect(gameDisplay, black,
                 (0, 0, display_width, 100))
pygame.draw.rect(gameDisplay, button,
                 (time_x, button_y, button_width, button_height))
pygame.draw.rect(gameDisplay, button,
                 (bust_x, button_y, button_width, button_height))
show_text("TIME+1", 250, 50, 25, white)
show_text("BUST", 450, 50, 25, white)
pygame.display.flip()

init_prob = (1 / (board_dim * board_dim))
probability = [[init_prob for i in range(board_dim)] for j in range(board_dim)]

draw_board()
show_probability()
last_X, last_Y = 0, 0
bust_clicked = False
pygame.display.flip()

while not game_quit:
    draw_board()
    if bust_clicked:
        centerX = (last_Y * square_size)+0.5*square_size
        centerY = 100 + (last_X * square_size) + 0.5 * square_size
        show_probability(last_X,last_Y)
        show_text(bust_text, centerX, centerY, 18, black, "magneto")
        pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and not bust_clicked:
            posX, posY = pygame.mouse.get_pos()

            if posY < 100:
                if posX >= time_x and posX <= (time_x + button_width) and posY >= button_y and posY <= (button_y + button_height):
                    probability[last_X][last_Y] = (last_X+last_Y)/100
                elif posX >= bust_x and posX <= (bust_x + button_width) and posY >= button_y and posY <= (button_y + button_height):
                    change_color(last_X, last_Y, blue)
                    bust_clicked = True
                    bust_text = "HIT"
                
                show_probability()
                pygame.display.flip()

            else:
                posY = posY - 100
                p_j = int((posX - 0.001)) // square_size
                p_i = int((posY - 0.001)) // square_size
                last_X,last_Y = int(p_i),int(p_j)
                change_color(p_i, p_j, red)
                show_probability()
                pygame.display.flip()

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    
    clock.tick(60)
