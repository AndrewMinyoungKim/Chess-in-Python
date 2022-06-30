import pygame

from .constants import *

class Piece:
    def __init__(self, name, row, col, colour, win):
        
        self.name = name
        self.row = row
        self.col = col
        self.colour = colour
        if(self.colour == BLACK):
            self.colour_word = "Black"
        else:
            self.colour_word = "White"
        self.win = win
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.draw_piece(self.win)

    def __del__(self):
        if(not game_over):
            # different convenient ways to print a message with variables
            # print(self.colour_word, self.name, "taken")
            # print("The {0} {1} has been captured".format(self.colour_word, self.name))
            # print("The {} {} has been captured".format(self.colour_word, self.name))
            # print("The {colour} {piece} has been captured".format(colour = self.colour_word, piece = self.name))
            print(f"The {self.colour_word} {self.name} has been captured") # most convenient way imo, "f-strings"

    def calc_pos(self):
        self.x = SQUARE * self.col + SQUARE // 2
        self.y = SQUARE * self.row + SQUARE // 2

    def draw_piece(self, win):
        if self.colour == BLACK:
            colour_initial = 'b'
        elif self.colour == WHITE:
            colour_initial = 'w'

        piece = colour_initial + self.name
        png_image_path = "assets/" + piece + ".png"
        image = pygame.transform.scale(pygame.image.load(png_image_path), (SQUARE, SQUARE))
        win.blit(image, (self.x - image.get_width()//2, self.y - image.get_height()//2))

    def pawn_movement(self, erase, board, state, win):
        avail_moves = []

        # useful variables
        first_move = False
        if(self.colour == WHITE):
            direction = 1
            opponent = BLACK
            if(self.row == 1):
                first_move = True
        elif(self.colour == BLACK):
            direction = -1
            opponent = WHITE
            if(self.row == 6):
                first_move = True

        # forward movement
        if(self.row+direction >= 0 and self.row+direction < 8):
            row, col = self.row+direction, self.col
            if(not state[row][col]):
                if(erase):
                    board.draw_square(row, col, self.win, TILE_A if (row + col) % 2 == 0 else TILE_B)
                avail_moves.append((row, col))

                if(first_move):
                    if(not state[self.row+(2*direction)][self.col]):
                        row += direction
                        if(erase):
                            board.draw_square(row, col, self.win, TILE_A if (row + col) % 2 == 0 else TILE_B)
                        avail_moves.append((row, col))

        # diagonal attack
        #left side
        if(self.row+direction >= 0 and self.row+direction < 8 and self.col-1 >= 0):
            row, col = self.row+direction, self.col-1
            if(state[row][col]):
                if(state[row][col].colour != state[self.row][self.col].colour):
                    if(erase):
                        board.draw_selected_piece(row, col, self.win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                    avail_moves.append((row, col))

        #right side
        if(self.row+direction >= 0 and self.row+direction < 8 and self.col+1 < 8):
            row, col = self.row+direction, self.col+1
            if(state[row][col]):
                if(state[row][col].colour != state[self.row][self.col].colour):
                    if(erase):
                        board.draw_selected_piece(row, col, self.win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                    avail_moves.append((row, col))

        return avail_moves

    def knight_movement(self, erase, board, state, win):
        avail_moves = []

        #up side
        if(self.row-2 >= 0 and self.col-1 >= 0):
            row, col = self.row-2, self.col-1
            if(state[row][col]):
                if(state[row][col].colour != state[self.row][self.col].colour):
                    if(erase):
                        board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                    avail_moves.append((row, col))
            else:
                if(erase):
                    board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
                avail_moves.append((row, col))

        if(self.row-2 >= 0 and self.col+1 < 8):
            row, col = self.row-2, self.col+1
            if(state[row][col]):
                if(state[row][col].colour != state[self.row][self.col].colour):
                    if(erase):
                        board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                    avail_moves.append((row, col))
            else:
                if(erase):
                    board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
                avail_moves.append((row, col))

        #down side
        if(self.row+2 < 8 and self.col-1 >= 0):
            row, col = self.row+2, self.col-1
            if(state[row][col]):
                if(state[row][col].colour != state[self.row][self.col].colour):
                    if(erase):
                        board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                    avail_moves.append((row, col))
            else:
                if(erase):
                    board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
                avail_moves.append((row, col))

        if(self.row+2 < 8 and self.col+1 < 8):
            row, col = self.row+2, self.col+1
            if(state[row][col]):
                if(state[row][col].colour != state[self.row][self.col].colour):
                    if(erase):
                        board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                    avail_moves.append((row, col))
            else:
                if(erase):
                    board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
                avail_moves.append((row, col))

        #left side
        if(self.col-2 >= 0 and self.row-1 >= 0):
            row, col = self.row-1, self.col-2
            if(state[row][col]):
                if(state[row][col].colour != state[self.row][self.col].colour):
                    if(erase):
                        board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                    avail_moves.append((row, col))
            else:
                if(erase):
                    board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
                avail_moves.append((row, col))

        if(self.col-2 >= 0 and self.row+1 < 8):
            row, col = self.row+1, self.col-2
            if(state[row][col]):
                if(state[row][col].colour != state[self.row][self.col].colour):
                    if(erase):
                        board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                    avail_moves.append((row, col))
            else:
                if(erase):
                    board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
                avail_moves.append((row, col))

        #right side
        if(self.col+2 < 8 and self.row-1 >= 0):
            row, col = self.row-1, self.col+2
            if(state[row][col]):
                if(state[row][col].colour != state[self.row][self.col].colour):
                    if(erase):
                        board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                    avail_moves.append((row, col))
            else:
                if(erase):
                    board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
                avail_moves.append((row, col))

        if(self.col+2 < 8 and self.row+1 < 8):
            row, col = self.row+1, self.col+2
            if(state[row][col]):
                if(state[row][col].colour != state[self.row][self.col].colour):
                    if(erase):
                        board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                    avail_moves.append((row, col))
            else:
                if(erase):
                    board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
                avail_moves.append((row, col))

        return avail_moves

    def bishop_movement(self, erase, board, state, win):
        avail_moves = []
        row, col = self.row, self.col

        # NW
        row = self.row - 1
        col = self.col - 1
        while(row >= 0 and col >= 0 and not state[row][col]):
            if(erase):
                board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
            
            avail_moves.append((row, col))
            row -= 1
            col -= 1
        if(row >= 0 and col >= 0):
            if(state[row][col].colour != self.colour):
                if(erase):
                    board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                
                avail_moves.append((row, col))

        # NE
        row = self.row - 1
        col = self.col + 1
        while(row >= 0 and col < 8 and not state[row][col]):
            if(erase):
                board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
            
            avail_moves.append((row, col))
            row -= 1
            col += 1
        if(row >= 0 and col < 8):
            if(state[row][col].colour != self.colour):
                if(erase):
                    board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                
                avail_moves.append((row, col))

        # SE
        row = self.row + 1
        col = self.col + 1
        while(row < 8 and col < 8 and not state[row][col]):
            if(erase):
                board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
            
            avail_moves.append((row, col))
            row += 1
            col += 1
        if(row < 8 and col < 8):
            if(state[row][col].colour != self.colour):
                if(erase):
                    board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                
                avail_moves.append((row, col))

        # SW
        row = self.row + 1
        col = self.col - 1
        while(row < 8 and col >= 0 and not state[row][col]):
            if(erase):
                board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)

            avail_moves.append((row, col))
            row += 1
            col -= 1
        if(row < 8 and col >= 0):
            if(state[row][col].colour != self.colour):
                if(erase):
                    board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)

                avail_moves.append((row, col))

        return avail_moves

    # rook movement
    def rook_movement(self, erase, board, state, win):
        avail_moves = []
        row, col = self.row, self.col
        
        # file movement
        # up
        row = self.row - 1
        while(row >= 0 and not state[row][col]):
            if(erase):
                board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
            
            avail_moves.append((row, col))
            row -= 1
        if(row >= 0):
            if(state[row][col].colour != self.colour):
                if(erase):
                    board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)

                avail_moves.append((row, col))

        # down
        row = self.row + 1
        while(row < 8 and not state[row][col]):
            if(erase):
                board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
            
            avail_moves.append((row, col))
            row += 1
        if(row < 8):
            if(state[row][col].colour != self.colour):
                if(erase):
                    board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                
                avail_moves.append((row, col))

        row = self.row
        # rank movement
        # left
        col = self.col - 1
        while(col >= 0 and not state[row][col]):
            if(erase):
                board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
            
            avail_moves.append((row, col))
            col -= 1
        if(col >= 0):
            if(state[row][col].colour != self.colour):
                if(erase):
                    board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                
                avail_moves.append((row, col))
        
        # right
        col = self.col + 1
        while(col < 8 and not state[row][col]):
            if(erase):
                board.draw_square(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B)
            
            avail_moves.append((row, col))
            col += 1
        if(col < 8):
            if(state[row][col].colour != self.colour):
                if(erase):
                    board.draw_selected_piece(row, col, win, TILE_A if (row + col) % 2 == 0 else TILE_B, state)
                
                avail_moves.append((row, col))

        return avail_moves

    def queen_movement(self, erase, board, state, win):
        avail_moves = []
        straight = self.rook_movement(erase, board, state, win)
        diagonal = self.bishop_movement(erase, board, state, win)

        #using a list comprehension and normal loop to append
        avail_moves = [(x, y) for x, y, *_ in straight]
        for x, y in diagonal:
            avail_moves.append((x, y))

        return avail_moves

    def king_movement(self, erase, board, state, win):
        avail_moves = []
        left, right, up, down = False, False, False, False
        
        # straight file and rank
        if(self.row-1 >= 0):
            left = True
            if(state[self.row-1][self.col]):
                if(state[self.row-1][self.col].colour == state[self.row][self.col].colour):
                    pass
                else:
                    if(erase):
                        board.draw_selected_piece(self.row-1, self.col, win, TILE_A if (self.row-1 + self.col) % 2 == 0 else TILE_B, state)
                    avail_moves.append((self.row-1, self.col))
            else:
                if(erase):
                    board.draw_square(self.row-1, self.col, win, TILE_A if (self.row-1 + self.col) % 2 == 0 else TILE_B)
                avail_moves.append((self.row-1, self.col))
        if(self.row+1 < 8):
            right = True
            if(state[self.row+1][self.col]):
                if(state[self.row+1][self.col].colour == state[self.row][self.col].colour):
                    pass
                else:
                    if(erase):
                        board.draw_selected_piece(self.row+1, self.col, win, TILE_A if (self.row+1 + self.col) % 2 == 0 else TILE_B, state)
                    avail_moves.append((self.row+1, self.col))
            else:
                if(erase):
                    board.draw_square(self.row+1, self.col, win, TILE_A if (self.row+1 + self.col) % 2 == 0 else TILE_B)
                avail_moves.append((self.row+1, self.col))
        if(self.col-1 >= 0):
            up = True
            if(state[self.row][self.col-1]):
                if(state[self.row][self.col-1].colour == state[self.row][self.col].colour):
                    pass
                else:
                    if(erase):
                        board.draw_selected_piece(self.row, self.col-1, win, TILE_A if (self.row + self.col-1) % 2 == 0 else TILE_B, state)
                    avail_moves.append((self.row, self.col-1))
            else:
                if(erase):
                    board.draw_square(self.row, self.col-1, win, TILE_A if (self.row + self.col-1) % 2 == 0 else TILE_B)
                avail_moves.append((self.row, self.col-1))
        if(self.col+1 < 8):
            down = True
            if(state[self.row][self.col+1]):
                if(state[self.row][self.col+1].colour == state[self.row][self.col].colour):
                    pass
                else:
                    if(erase):
                        board.draw_selected_piece(self.row, self.col+1, win, TILE_A if (self.row + self.col+1) % 2 == 0 else TILE_B, state)
                    avail_moves.append((self.row, self.col+1))
            else:
                if(erase):
                    board.draw_square(self.row, self.col+1, win, TILE_A if (self.row + self.col+1) % 2 == 0 else TILE_B)
                avail_moves.append((self.row, self.col+1))

        # diagonals
        if(left and up):
            if(state[self.row-1][self.col-1]):
                if(state[self.row-1][self.col-1].colour == state[self.row][self.col].colour):
                    pass
                else:
                    if(erase):
                        board.draw_selected_piece(self.row-1, self.col-1, win, TILE_A if (self.row-1 + self.col-1) % 2 == 0 else TILE_B, state)
                    avail_moves.append((self.row-1, self.col-1))
            else:
                if(erase):
                    board.draw_square(self.row-1, self.col-1, win, TILE_A if (self.row-1 + self.col-1) % 2 == 0 else TILE_B)
                avail_moves.append((self.row-1, self.col-1))

        if(right and up):
            if(state[self.row+1][self.col-1]):
                if(state[self.row+1][self.col-1].colour == state[self.row][self.col].colour):
                    pass
                else:
                    if(erase):
                        board.draw_selected_piece(self.row+1, self.col-1, win, TILE_A if (self.row+1 + self.col-1) % 2 == 0 else TILE_B, state)
                    avail_moves.append((self.row+1, self.col-1))
            else:
                if(erase):
                    board.draw_square(self.row+1, self.col-1, win, TILE_A if (self.row+1 + self.col-1) % 2 == 0 else TILE_B)
                avail_moves.append((self.row+1, self.col-1))

        if(left and down):
            if(state[self.row-1][self.col+1]):
                if(state[self.row-1][self.col+1].colour == state[self.row][self.col].colour):
                    pass
                else:
                    if(erase):
                        board.draw_selected_piece(self.row-1, self.col+1, win, TILE_A if (self.row-1 + self.col+1) % 2 == 0 else TILE_B, state)
                    avail_moves.append((self.row-1, self.col+1))
            else:
                if(erase):
                    board.draw_square(self.row-1, self.col+1, win, TILE_A if (self.row-1 + self.col+1) % 2 == 0 else TILE_B)
                avail_moves.append((self.row-1, self.col+1))

        if(right and down):
            if(state[self.row+1][self.col+1]):
                if(state[self.row+1][self.col+1].colour == state[self.row][self.col].colour):
                    pass
                else:
                    if(erase):
                        board.draw_selected_piece(self.row+1, self.col+1, win, TILE_A if (self.row+1 + self.col+1) % 2 == 0 else TILE_B, state)
                    avail_moves.append((self.row+1, self.col+1))
            else:
                if(erase):
                    board.draw_square(self.row+1, self.col+1, win, TILE_A if (self.row+1 + self.col+1) % 2 == 0 else TILE_B)
                avail_moves.append((self.row+1, self.col+1))

        return avail_moves

    # movement of each piece
    def movement(self, erase, board, state, win):
        #white_piece = WHITE if self.colour == WHITE else BLACK
        if(self.name == 'P'):
            return self.pawn_movement(erase, board, state, win)
        elif(self.name == 'N'):
            return self.knight_movement(erase, board, state, win)
        elif(self.name == 'B'):
            return self.bishop_movement(erase, board, state, win)
        elif(self.name == 'R'):
            return self.rook_movement(erase, board, state, win)
        elif(self.name == 'Q'):
            return self.queen_movement(erase, board, state, win)
        elif(self.name == 'K'):
            return self.king_movement(erase, board, state, win)