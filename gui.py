import pygame
import time
import sys
import numpy as np
import random

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


ghost_lottery = ["" for i in range(25)]
for i in range(5):
    ghost_lottery[4 * i] = "UP"
    ghost_lottery[4 * i+1] = "DOWN"
    ghost_lottery[4 * i+2] = "LEFT"
    ghost_lottery[4 * i+3] = "RIGHT"
ghost_lottery[20] = "TOP_LEFT"
ghost_lottery[21] = "TOP_RIGHT"
ghost_lottery[22] = "BOTTOM_LEFT"
ghost_lottery[23] = "BOTTOM_RIGHT"
ghost_lottery[24] = "STAY"
random.shuffle(ghost_lottery)


total_color = 3
red_distance = int(board_dim / 3)
yellow_distace = int(board_dim * .67)
green_distance = board_dim
color_to_distace = [red_distance, yellow_distace, green_distance]

#initialize values
init_prob = (1 / (board_dim * board_dim))
probability = np.full((1,board_dim*board_dim), init_prob)



def get_transitional_probability(indexA, indexB):
    transition_distribution = {"STRAIGHT": 0.2,
                               "DIAGONAL": 0.04, "STAY": 0.04}
    indexA_col = indexA % board_dim
    indexA_row = (indexA - indexA_col) // board_dim

    indexB_col = indexB % board_dim
    indexB_row = (indexB - indexB_col) // board_dim

    if indexA == indexB:
        return transition_distribution["STAY"]
    elif abs(indexA_row - indexB_row)== 1 and (indexA_col == indexB_col):
        return transition_distribution["STRAIGHT"]
    elif abs(indexA_col - indexB_col)== 1 and (indexA_row == indexB_row):
        return transition_distribution["STRAIGHT"]
    elif abs(indexA_row - indexB_row) == 1 and abs(indexA_col - indexB_col) == 1:
        return transition_distribution["DIAGONAL"]
    else:
        return 0

def show_probability(bust_X=-1, bust_Y=-1):
    for i in range(board_dim):
        for j in range(board_dim):
            if i == bust_X and j == bust_Y:
                centerY = 100 + (i * square_size)+0.5*square_size
                centerX = (j * square_size)+0.5*square_size
                show_text("", centerX, centerY, 20, black, "magneto")

            else:
                centerY = 100 + (i * square_size)+0.5*square_size
                centerX = (j * square_size)+0.5*square_size
                show_text(str(np.round(probability[0, i*board_dim+j],2)),
                          centerX, centerY, 20, black, "magneto")


def move_ghost(prev_x, prev_y):
    move_taken = False
    
    while not move_taken:
        move = random.randint(0, 24)
        move = ghost_lottery[move]
        # print(f"cur_x: {prev_x} cur_y: {prev_y} move: {move}")
        if move == "STAY":
            cur_x = prev_x
            cur_y = prev_y
            move_taken = True
        elif move == "UP":
            cur_x = prev_x - 1
            cur_y = prev_y
            move_taken = True if cur_x >= 0 else False
        elif move == "DOWN":
            cur_x = prev_x + 1
            cur_y = prev_y
            move_taken = True if cur_x < board_dim else False
        elif move == "LEFT":
            cur_x = prev_x
            cur_y = prev_y - 1
            move_taken = True if cur_y >= 0 else False
        elif move == "RIGHT":
            cur_x = prev_x
            cur_y = prev_y + 1
            move_taken = True if cur_y < board_dim else False
        elif move == "TOP_LEFT":
            cur_x = prev_x - 1
            cur_y = prev_y - 1
            move_taken = True if (cur_x >= 0 and cur_y >= 0) else False
        elif move == "TOP_RIGHT":
            cur_x = prev_x - 1
            cur_y = prev_y + 1
            move_taken = True if (cur_x >= 0 and cur_y < board_dim) else False
        elif move == "BOTTOM_LEFT":
            cur_x = prev_x + 1
            cur_y = prev_y - 1
            move_taken = True if (cur_x < board_dim and cur_y >= 0) else False
        elif move == "BOTTOM_RIGHT":
            cur_x = prev_x + 1
            cur_y = prev_y + 1
            move_taken = True if (cur_x < board_dim and cur_y < board_dim) else False
    return (cur_x,cur_y)

def get_emission_probability(indexA, indexB):
    indexA_col = indexA % board_dim
    indexA_row = (indexA - indexA_col) // board_dim

    color = indexB % total_color  #(0-->red,1-->yellow,2-->green)
    indexB = (indexB - color) // total_color
    indexB_col = indexB % board_dim
    indexB_row = (indexB - indexB_col) // board_dim

    man_dis = abs(indexA_row - indexB_row) + abs(indexA_col - indexB_col)
 
    if color == 0:
        return 1 if man_dis <= red_distance else 0
    elif color == 1:
        return 1 if (man_dis > red_distance and man_dis <= yellow_distace) else 0
    else:
        return 1 if man_dis > yellow_distace else 0



transition_Matrix = np.zeros((board_dim*board_dim, board_dim*board_dim))
for i in range(board_dim*board_dim):
    for j in range(board_dim*board_dim):
        transition_Matrix[i][j] = get_transitional_probability(i, j)

#Normalize Transition Matrix
norm = np.linalg.norm(transition_Matrix, ord=1, axis=1, keepdims=True) + 1e-9
transition_Matrix = transition_Matrix/norm

#Emission Matrix
print(color_to_distace)
emission_Matrix = np.zeros((board_dim*board_dim,board_dim * board_dim * total_color))
for i in range(board_dim*board_dim):
    for j in range(board_dim*board_dim*total_color):
        emission_Matrix[i][j] = get_emission_probability(i, j)

#Normalize Emission Matrix
norm = np.linalg.norm(emission_Matrix, ord=1, axis=1, keepdims=True) + 1e-9
emission_Matrix = emission_Matrix / norm

ghost_x = random.randint(0,board_dim-1)
ghost_y = random.randint(0, board_dim - 1)

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
        show_probability(last_X, last_Y)
        show_text(bust_text, centerX, centerY, 18, black, "magneto")
        pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and not bust_clicked:
            posX, posY = pygame.mouse.get_pos()
            # print(ghost_x, ghost_y)

            if posY < 100:
                if posX >= time_x and posX <= (time_x + button_width) and posY >= button_y and posY <= (button_y + button_height):
                    # probability[last_X*board_dim+last_Y] = last_X+last_Y
                    probability = np.matmul(probability, transition_Matrix)
                    norm = np.linalg.norm(probability, ord=1, axis=1, keepdims=True) + 1e-9
                    probability = probability / norm
                    ghost_x, ghost_y = move_ghost(ghost_x,ghost_y)
                elif posX >= bust_x and posX <= (bust_x + button_width) and posY >= button_y and posY <= (button_y + button_height):
                    change_color(last_X, last_Y, blue)
                    if ghost_x == last_X and ghost_y == last_Y:
                        bust_text = "HIT"
                    else:
                        bust_text = "MISS"
                    print(f"ghost location: {ghost_x} {ghost_y}")
                    bust_clicked = True

                show_probability()
                pygame.display.flip()

            else:
                posY = posY - 100
                p_j = int((posX - 0.001)) // square_size
                p_i = int((posY - 0.001)) // square_size
                last_X, last_Y = int(p_i), int(p_j)
                manhattan_distance = abs(p_i - ghost_x) + abs(p_j - ghost_y)
                if manhattan_distance <= red_distance:
                    color = red
                    color_index = 0
                elif manhattan_distance <= yellow_distace:
                    color = yellow
                    color_index = 1
                else:
                    color = green
                    color_index = 2

                change_color(p_i, p_j, color)
                emission_col = int((((board_dim * p_i) + p_j) * total_color) + color_index)
                emission_prob = emission_Matrix[:, emission_col]

                probability = (probability * emission_prob) / np.sum(emission_prob)
                norm = np.linalg.norm(probability, ord=1, axis=1, keepdims=True) + 1e-9
                probability = probability / norm

                show_probability()
                pygame.display.flip()

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    clock.tick(60)
