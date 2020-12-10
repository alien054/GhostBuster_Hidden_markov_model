import pygame
import time
import sys

arg_count = len(sys.argv)
if (arg_count != 3) and sys.argv[1] != "-dim":
    print("""
          #usage
          python gui.py [-dim <board_dimension>]
          
          @flag
          -dim : sets dimension of board
                for 8*8 -dim must set to 8
                for 6*6 -dim must set to 6
          """)
    sys.exit()

elif sys.argv[1] == "-dim":
    board_dim = int(sys.argv[2])


#init pygame
pygame.init()
# Constants
filePath = "game.txt"

display_width = 480
display_height = 580

# board_dim = 8
board_width = display_width
board_height = display_height - 100

square_size = board_width // board_dim

piece_centerX = (board_height // (board_dim*2))
piece_centerY = (board_width // (board_dim*2)) + 100
piece_radius = piece_centerX - 2

game_quit = False

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (100, 100, 100)
yellow = (255, 213, 0)
charcol = (60, 73, 96)
ash = (73, 80, 87)
wood = (64, 64, 64)
wood_light = (151, 157, 172)
wood_dark = (4, 102, 200)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Line of action')
clock = pygame.time.Clock()


def show_text(msg, x, y, size, color, font="magneto", sysfont=True):
    if sysfont:
        font = pygame.font.SysFont(font, size)
    else:
        font = pygame.font.Font(font, size)
    TextSurf = font.render(msg, True, color)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((x), (y))
    gameDisplay.blit(TextSurf, TextRect)


def init_file(path):
    output = ""
    output += str(0) + "\n"
    output += str(1) + "\n"

    if board_dim == 8:
        # output += "0 1 1 1 1 1 1 0\n2 0 0 0 0 0 0 2\n2 0 0 0 0 0 0 2\n2 0 0 0 0 0 0 2\n2 0 0 0 0 0 0 2\n2 0 0 0 0 0 0 2\n2 0 0 0 0 0 0 2\n0 1 1 1 1 1 1 0"
        output += "0 2 2 2 2 2 2 0\n1 0 0 0 0 0 0 1\n1 0 0 0 0 0 0 1\n1 0 0 0 0 0 0 1\n1 0 0 0 0 0 0 1\n1 0 0 0 0 0 0 1\n1 0 0 0 0 0 0 1\n0 2 2 2 2 2 2 0"

    elif board_dim == 6:
        # output += "0 1 1 1 1 0\n2 0 0 0 0 2\n2 0 0 0 0 2\n2 0 0 0 0 2\n2 0 0 0 0 2\n0 1 1 1 1 0"
        output += "0 2 2 2 2 0\n1 0 0 0 0 1\n1 0 0 0 0 1\n1 0 0 0 0 1\n1 0 0 0 0 1\n0 2 2 2 2 0"

    with open(path, "w") as file:
        file.write(output)


def draw_banner(white_type,black_type,turn,winner = "0"):
    gameDisplay.fill(charcol, rect=(0, 0, 600, 100))
    
    show_text("White: {}".format(white_type), 400, 33, 18, white)
    show_text("Black: {}".format(black_type), 400, 66, 18, black)
    if turn == "1":
        show_text("Whites Move", 100, 50, 25, white)
    elif turn == "2":
        show_text("Blacks Move", 100, 50, 25, black)

    elif turn == "100" or turn == "200":
        if winner == "1":
            winner = "White"
        elif winner == "2":
            winner = "Black"

        show_text("{} Wins".format(winner), 100, 50, 25, white)
    # pygame.display.flip()

def draw_board():
    w = board_width / board_dim
    h = board_height / board_dim

    board = pygame.Surface((board_width, board_height))
    board.fill(white)
    for x in range(0, board_dim):
        for y in range(0, board_dim):
            color = wood_light if (x+y) % 2 == 0 else wood_dark
            pygame.draw.rect(board, color, (y*w, x*w, w, h))

    gameDisplay.blit(board, (0, 100))
    # pygame.display.flip()

def draw_piece_Loop(board):
    for i in range(0, board_dim):
        for j in range(0, board_dim):
            draw_piece("red", i, j)
            if board[i][j] == "1":
                draw_piece("white", i, j)
            elif board[i][j] == "2":
                draw_piece("black", i, j)

def draw_piece(color, i, j):
    outer = piece_radius
    inner = piece_radius - (piece_radius * 0.30)

    centerX = piece_centerX + (j*(square_size))
    centerY = piece_centerY + (i*(square_size))
    position = (centerX, centerY)

    if color == "red" :
        show_text("{} {}".format(i,j), centerX,centerY, 15, charcol)
    else:
        image = pygame.draw.circle(gameDisplay, color, position, outer, width=5)
        image = pygame.draw.circle(gameDisplay, color, position, inner, width=15)


def read_file(path):
    with open(path,"r") as file:
        turn = file.readline().replace("\n", "")
        previous = file.readline().replace("\n", "")
        # print(line)

        board = []
        for i in range(0, board_dim):
            line = file.readline()
            line = line.replace("\n", "")
            temp = list(line.split(" "))
            board.append(temp)

    return turn, previous, board
    

def write_file(path,turn, previous, board):
    output = ""
    output += str(turn) + "\n"
    output += str(previous) + "\n"

    for i in range(0, board_dim):
        for j in range(0, board_dim):
            output += str(board[i][j])
            if j != board_dim - 1:
                 output += " "
        if i != board_dim - 1:
            output += "\n"
    
    print(output)
    with open(path, "w") as file:
        file.write(output)

def getHorizontalPieceCount(board, position):
    count = 0
    (posX,posY) = position  #tuple unpack
    for i in range(0, board_dim):
        if board[posX][i] == "1" or board[posX][i] == "2":
            count = count + 1
    
    return count


def getVerticalPieceCount(board, position):
    count = 0
    (posX, posY) = position  # tuple unpack
    for i in range(0, board_dim):
        if board[i][posY] == "1" or board[i][posY] == "2":
            count = count + 1
    return count


def getFirstDiagonalPieceCount(board, position):
    count = 0
    (posX, posY) = position
    
    if posX >= posY:
        row = posX - posY
        col = 0
    else:
        row = 0
        col = posY - posX
    
    while (row < board_dim and col < board_dim):
        if board[row][col] == "1" or board[row][col] == "2":
            count = count + 1
        row = row + 1
        col = col + 1
    
    return count


def getSecondDiagonalPieceCount(board, position):
    count = 0
    (posX, posY) = position

    if (posX+posY)<board_dim:
        row = 0
        col = posX + posY
    else:
        col = board_dim - 1
        row = (posX+posY) - col

    while (row < board_dim and col >= 0):
        if board[row][col] == "1" or board[row][col] == "2":
            count = count + 1
        row = row + 1
        col = col - 1

    return count

def getAvailableMoves(board, position, playerColor: str, opponentColor: str):
    (posX, posY) = position
    availableMoves = []
    if (board[posX][posY] != playerColor):
        print("Not our piece")
        return availableMoves
    
    #Right move
    pieceCount = getHorizontalPieceCount(board, position)
    row = posX
    column = posY
    movesTaken = 0

    column = column + 1  #right move taken
    while (column < board_dim):
        if board[row][column] == opponentColor:
            if movesTaken == (pieceCount - 1):
                movesTaken = movesTaken + 1
            else:
                break
        elif board[row][column] == playerColor:
            if movesTaken == (pieceCount - 1):
                break;
            else:
                movesTaken = movesTaken + 1
        elif board[row][column] == "0":
            movesTaken = movesTaken + 1
        
        if movesTaken == pieceCount:
            availableMoves.append((row, column))
            break

        column = column + 1
    
    #Left move
    pieceCount = getHorizontalPieceCount(board, position)
    row = posX
    column = posY
    movesTaken = 0

    column = column - 1  # left move taken
    while (column >= 0):
        if board[row][column] == opponentColor:
            if movesTaken == (pieceCount - 1):
                movesTaken = movesTaken + 1
            else:
                break
        elif board[row][column] == playerColor:
            if movesTaken == (pieceCount - 1):
                break
            else:
                movesTaken = movesTaken + 1
        elif board[row][column] == "0":
            movesTaken = movesTaken + 1

        if movesTaken == pieceCount:
            availableMoves.append((row, column))
            break
    
        column = column - 1

    #Up move
    pieceCount = getVerticalPieceCount(board, position)
    row = posX
    column = posY
    movesTaken = 0

    row = row - 1  # up move taken
    while (row >= 0):
        if board[row][column] == opponentColor:
            if movesTaken == (pieceCount - 1):
                movesTaken = movesTaken + 1
            else:
                break
        elif board[row][column] == playerColor:
            if movesTaken == (pieceCount - 1):
                break
            else:
                movesTaken = movesTaken + 1
        elif board[row][column] == "0":
            movesTaken = movesTaken + 1

        if movesTaken == pieceCount:
            availableMoves.append((row, column))
            break

        row = row - 1

    #Down move
    pieceCount = getVerticalPieceCount(board, position)
    row = posX
    column = posY
    movesTaken = 0

    row = row + 1  # down move taken
    while (row < board_dim):
        if board[row][column] == opponentColor:
            if movesTaken == (pieceCount - 1):
                movesTaken = movesTaken + 1
            else:
                break
        elif board[row][column] == playerColor:
            if movesTaken == (pieceCount - 1):
                break
            else:
                movesTaken = movesTaken + 1
        elif board[row][column] == "0":
            movesTaken = movesTaken + 1

        if movesTaken == pieceCount:
            availableMoves.append((row, column))
            break

        row = row + 1

    #Lower Right move
    pieceCount = getFirstDiagonalPieceCount(board, position)
    row = posX
    column = posY
    movesTaken = 0

    row = row + 1  # Lower Right move taken
    column = column + 1
    while (row < board_dim and column < board_dim):
        if board[row][column] == opponentColor:
            if movesTaken == (pieceCount - 1):
                movesTaken = movesTaken + 1
            else:
                break
        elif board[row][column] == playerColor:
            if movesTaken == (pieceCount - 1):
                break
            else:
                movesTaken = movesTaken + 1
        elif board[row][column] == "0":
            movesTaken = movesTaken + 1

        if movesTaken == pieceCount:
            availableMoves.append((row, column))
            break

        row = row + 1
        column = column + 1

    #Upper Left move
    pieceCount = getFirstDiagonalPieceCount(board, position)
    row = posX
    column = posY
    movesTaken = 0

    row = row - 1  # Upper Left move taken
    column = column - 1
    while (row >= 0 and column >= 0):
        if board[row][column] == opponentColor:
            if movesTaken == (pieceCount - 1):
                movesTaken = movesTaken + 1
            else:
                break
        elif board[row][column] == playerColor:
            if movesTaken == (pieceCount - 1):
                break
            else:
                movesTaken = movesTaken + 1
        elif board[row][column] == "0":
            movesTaken = movesTaken + 1

        if movesTaken == pieceCount:
            availableMoves.append((row, column))
            break

        row = row - 1
        column = column - 1

    #Lower Left move
    pieceCount = getSecondDiagonalPieceCount(board, position)
    row = posX
    column = posY
    movesTaken = 0

    row = row + 1  # Lower Left move taken
    column = column - 1
    while (row < board_dim and column >= 0):
        if board[row][column] == opponentColor:
            if movesTaken == (pieceCount - 1):
                movesTaken = movesTaken + 1
            else:
                break
        elif board[row][column] == playerColor:
            if movesTaken == (pieceCount - 1):
                break
            else:
                movesTaken = movesTaken + 1
        elif board[row][column] == "0":
            movesTaken = movesTaken + 1

        if movesTaken == pieceCount:
            availableMoves.append((row, column))
            break

        row = row + 1
        column = column - 1

    #Upper Right move
    pieceCount = getSecondDiagonalPieceCount(board, position)
    row = posX
    column = posY
    movesTaken = 0

    row = row - 1  # Upper Right move taken
    column = column + 1
    while (row >= 0 and column < board_dim):
        if board[row][column] == opponentColor:
            if movesTaken == (pieceCount - 1):
                movesTaken = movesTaken + 1
            else:
                break
        elif board[row][column] == playerColor:
            if movesTaken == (pieceCount - 1):
                break
            else:
                movesTaken = movesTaken + 1
        elif board[row][column] == "0":
            movesTaken = movesTaken + 1

        if movesTaken == pieceCount:
            availableMoves.append((row, column))
            break

        row = row - 1
        column = column + 1

    return availableMoves

def isConnected(position, other):
    (posX, posY) = position
    (otherX, otherY) = other
    
    if ((posX + 1) == otherX) and (posY == otherY):
        return True #down
    elif ((posX - 1) == otherX) and (posY == otherY):
        return True  #up
    elif (posX == otherX) and ((posY + 1) == otherY):
        return True  #right
    elif (posX == otherX) and ((posY - 1) == otherY):
        return True  #left
    elif ((posX + 1) == otherX) and ((posY + 1) == otherY):
        return True  #lower right
    elif ((posX - 1) == otherX) and ((posY + 1) == otherY):
        return True  # upper right
    elif ((posX - 1) == otherX) and ((posY - 1) == otherY):
        return True  # upper left
    elif ((posX + 1) == otherX) and ((posY - 1) == otherY):
        return True  # lower left
    else:
        return False

def getPiecesOfSameColor(board, color: str):
    pieces = []

    for i in range(0, board_dim):
        for j in range(0, board_dim):
            if board[i][j] == color:
                pieces.append((i, j)) #append as a tuple

    return pieces

def isGameOVer(board, color: str):
    connectedPieces = []
    playerPieces = getPiecesOfSameColor(board, color)
    totalPiece = len(playerPieces)
    
    if len(playerPieces) == 1:
        return True

    start = playerPieces[0]
    connectedPieces.append(start)
    playerPieces.remove(start)

    temp = []

    while True:
        temp.clear()
        for playerPiece in playerPieces:
            for connectedPiece in connectedPieces:
                if isConnected(playerPiece, connectedPiece):
                    temp.append(playerPiece)
                    break
        
        if len(temp) == 0:
            return False
        for p in temp:
            connectedPieces.append(p)
            playerPieces.remove(p)
        
        if len(connectedPieces) == totalPiece:
            return True 

    

gameDisplay.fill(ash, rect=(0, 0, display_width, display_height))
show_text("Choose Color:", 235, 180, 22, yellow)
box_width,box_height,box_x,vsHuman_y,vsAI_y = 140,50,170,225,300
pygame.draw.rect(gameDisplay, wood_dark, (box_x, vsHuman_y, box_width, box_height))
pygame.draw.rect(gameDisplay, wood_light, (box_x, vsAI_y, box_width, box_height))
show_text("vs Human", 240, 250,25, black)
show_text("vs AI",240,325, 25, white)
pygame.display.flip()

opponent_selected = False
while not opponent_selected:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            posX, posY = pygame.mouse.get_pos()
            print("x:{}, y:{}".format(posX, posY))
            if posX >= box_x and posX <= box_x + box_width and posY >= vsHuman_y and posY <= vsHuman_y + box_height:
                twoPlayer = True
                white_type = "Human"
                black_type = "Human"
                opponent_selected = True
            if posX >= box_x and posX <= box_x + box_width and posY >= vsAI_y and posY <= vsAI_y + box_height:
                twoPlayer = False
                opponent_selected = True


gameDisplay.fill(wood, rect=(0, 0, display_width, display_height))
show_text("Choose Color:", 235, 180, 22, yellow)
box_width,box_height,box_x,white_y,black_y = 140,50,170,225,300
pygame.draw.rect(gameDisplay, wood_dark, (box_x, white_y, box_width, box_height))
pygame.draw.rect(gameDisplay, wood_light, (box_x, black_y, box_width, box_height))
show_text("White", 240, 250,32, white)
show_text("Black",240,325, 32, black)
pygame.display.flip()

color_selected = False
while not color_selected:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            posX, posY = pygame.mouse.get_pos()
            print("x:{}, y:{}".format(posX, posY))
            if posX >= box_x and posX <= box_x + box_width and posY >= white_y and posY <= white_y + box_height:
                player1 = "1"
                if not twoPlayer:
                    white_type = "Human"
                    black_type = "AI"
                color_selected = True
            if posX >= box_x and posX <= box_x + box_width and posY >= black_y and posY <= black_y + box_height:
                player1 = "2"
                if not twoPlayer:
                    white_type = "AI"
                    black_type = "Human"
                color_selected = True

#player1 by default human
player2 = "1" if player1 == "2" else "2"

init_file(filePath)

while not game_quit:
    turn, previous, board = read_file(filePath)
    
    if turn == "0" or turn == "100" or turn == "200":

        draw_board()

        #Drawing pieces
        draw_piece_Loop(board)

        if turn == "100":
            draw_banner(white_type,black_type,turn, previous)
        elif turn == "200":
            previous_ = int(previous)
            previous_ = (previous_ % 2) + 1
            draw_banner(white_type, black_type, turn, str(previous_))
        elif turn == "0":
            previous_ = int(previous)
            next_turn = (previous_ % 2) + 1
            draw_banner(white_type, black_type, str(next_turn))
            write_file(filePath, next_turn, previous_, board)  # original
            #write_file("init.txt", previous, previous, board) #this is for debuging

    pygame.display.flip()
        
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and turn == player1:
            posX, posY = pygame.mouse.get_pos()
            posY = posY - 100
            p_j = int((posX - 0.001))  // square_size
            p_i = int((posY - 0.001)) // square_size
            # print("x:{}, y:{}".format(posX, posY))
            # print("i:{}, j:{}".format(p_i, p_j))
            if board[p_i][p_j] == player1:
                draw_board()
                draw_piece_Loop(board)
                draw_piece("yellow", p_i, p_j)
                pygame.display.flip()

                validMoves = getAvailableMoves(board, (p_i, p_j), player1, player2)

                for move in validMoves:
                    (moveX, moveY) = move
                    draw_piece("yellow", moveX, moveY)
                    pygame.display.flip()

                player1_move_taken = False
                while not player1_move_taken:
                    for secondEvent in pygame.event.get():
                        if secondEvent.type == pygame.MOUSEBUTTONUP:
                            new_posX, new_posY = pygame.mouse.get_pos()
                            new_posY = new_posY - 100
                            new_p_j = int((new_posX - 0.001))  // square_size
                            new_p_i = int((new_posY - 0.001)) // square_size
                            # print("new_x:{}, new_y:{}".format(new_posX, new_posY))
                            # print("new_i:{}, new_j:{}".format(new_p_i, new_p_j))
                            player1_move_taken = True

                            if (new_p_i, new_p_j) in validMoves:
                                board[p_i][p_j] = "0"
                                board[new_p_i][new_p_j] = player1
                                draw_board()
                                draw_piece_Loop(board)
                                # draw_banner(white_type,black_type,player2)
                                pygame.display.flip()
                                
                                if isGameOVer(board,player1):
                                    print("player1 wins")
                                    write_file(filePath, "100", player1, board)  #turn=100 previous=player1; meaning --> player1 declare himself winner
                                elif isGameOVer(board,player2):
                                    print("player2 wins")
                                    write_file(filePath, "200", player1, board)  #turn=200 previous=player1; meaning --> player1 declare player2 winner
                                else:
                                    write_file(filePath, 0, player1, board)  #turn=0 previous=player1; meaning--> next turn servers

                            else:
                                draw_board()
                                draw_piece_Loop(board)
                                pygame.display.flip()


            else:
                draw_board()
                draw_piece_Loop(board)
                pygame.display.flip()
            #player1 completed

            
            #player2 if human starts
        if event.type == pygame.MOUSEBUTTONUP and twoPlayer and turn == player2:
            posX, posY = pygame.mouse.get_pos()
            posY = posY - 100
            p_j = int((posX - 0.001))  // square_size
            p_i = int((posY - 0.001)) // square_size
            # print("x:{}, y:{}".format(posX, posY))
            # print("i:{}, j:{}".format(p_i, p_j))
            if board[p_i][p_j] == player2:
                draw_board()
                draw_piece_Loop(board)
                draw_piece("yellow", p_i, p_j)
                pygame.display.flip()

            validMoves = getAvailableMoves(board, (p_i, p_j), player2, player1)

            for move in validMoves:
                (moveX, moveY) = move
                draw_piece("yellow", moveX, moveY)
                pygame.display.flip()

            player2_move_taken = False
            while not player2_move_taken:
                for secondEvent in pygame.event.get():
                    if secondEvent.type == pygame.MOUSEBUTTONUP:
                        new_posX, new_posY = pygame.mouse.get_pos()
                        new_posY = new_posY - 100
                        new_p_j = int((new_posX - 0.001))  // square_size
                        new_p_i = int((new_posY - 0.001)) // square_size
                        # print("new_x:{}, new_y:{}".format(new_posX, new_posY))
                        # print("new_i:{}, new_j:{}".format(new_p_i, new_p_j))
                        player2_move_taken = True

                        if (new_p_i, new_p_j) in validMoves:
                            board[p_i][p_j] = "0"
                            board[new_p_i][new_p_j] = player2
                            draw_board()
                            draw_piece_Loop(board)
                            # draw_banner(white_type,black_type,player2)
                            pygame.display.flip()
                            
                            if isGameOVer(board,player2):
                                print("player2 wins")
                                write_file(filePath, "100", player2, board)  #turn=100 previous=player2; meaning --> player2 declare himself winner
                            elif isGameOVer(board,player1):
                                print("player1 wins")
                                write_file(filePath, "200", player2, board)  #turn=200 previous=player2; meaning --> player2 declare player2 winner
                            else:
                                write_file(filePath, 0, player2, board)  #turn=0 previous=player1; meaning--> next turn servers

                        else:
                            draw_board()
                            draw_piece_Loop(board)
                            pygame.display.flip()


        else:
            draw_board()
            draw_piece_Loop(board)
            pygame.display.flip()
            #player2 complete
        

            
            

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    time.sleep(0.2)  # this sleep is must for synchronization
    clock.tick(60)
