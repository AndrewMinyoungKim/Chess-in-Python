import pygame

from .constants import *

class Piece:
    def __init__(self, name, row, col, colour, win):
        
        self.name = name
        self.row = row
        self.col = col
        self.colour = colour
        self.win = win
        self.x = 0
        self.y = 0
        self.avail_moves = []
        self.calc_pos()
        self.draw_piece(self.win)

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


    def pawn_movement(self, erase, board, state, win, colour):

        first_move = False
        if(colour == WHITE):
            direction = 1
            opponent = BLACK
            if(self.row == 1):
                first_move = True
        elif(colour == BLACK):
            direction = -1
            opponent = WHITE
            if(self.row == 6):
                first_move = True

        # erase movements from previously selected piece
        if(erase):
            board.draw_square(self.row+direction, self.col, self.win, GREY if (self.row+direction + self.col) % 2 == 0 else GREEN)
            if(first_move):
                board.draw_square(self.row+(2*direction), self.col, self.win, GREY if (self.row+(2*direction) + self.col) % 2 == 0 else GREEN)

        # regular pawn movements
        else:
            board.draw_square(self.row+direction, self.col, self.win, ORANGE)
            if(first_move): # allow two space up moves for first pawn movements
                board.draw_square(self.row+(2*direction), self.col, self.win, ORANGE)

            # check diagonal attacks
            # don't go out of list index range if one of the rook's pawns
            if(self.col == 0):
                if(state[self.row+direction][self.col+direction]):
                    if(state[self.row+direction][self.col+direction].colour == opponent):
                        board.draw_square(self.row+direction, self.col+1, self.win, ORANGE)
                        state[self.row+direction][self.col+1].draw_piece(win)
            elif(self.col == 7):
                if(state[self.row+direction][self.col-1]):
                    if(state[self.row+direction][self.col-1].colour == opponent):
                        board.draw_square(self.row+direction, self.col-1, self.win, ORANGE)
                        state[self.row+direction][self.col-1].draw_piece(win)
            else:
                if(state[self.row+direction][self.col+direction]):
                    if(state[self.row+direction][self.col+direction].colour == opponent):
                        board.draw_square(self.row+direction, self.col+1, self.win, ORANGE)
                        state[self.row+direction][self.col+1].draw_piece(win)

                if(state[self.row+direction][self.col-1]):
                    if(state[self.row+direction][self.col-1].colour == opponent):
                        board.draw_square(self.row+direction, self.col-1, self.win, ORANGE)
                        state[self.row+direction][self.col-1].draw_piece(win)

    def knight_movement(self, erase, board, state, win, colour):
        pass

    def bishop_movement(self, erase, board, state, win, colour):
        pass

    def rook_movement(self, erase, board, state, win, colour):
        pass

    def queen_movement(self, erase, board, state, win, colour):
        pass

    def king_movement(self, erase, board, state, win, colour):
        pass

    # movement of each piece
    # need to consider check! and mate!
    def movement(self, erase, board, state, win):
        
        # PAWN MOVES
        if(self.name == 'P'):
            if(self.colour == WHITE):
                self.pawn_movement(erase, board, state, win, WHITE)
            else:
                self.pawn_movement(erase, board, state, win, BLACK)
            
        elif(self.name == 'N'):
            pass
        elif(self.name == 'B'):
            pass
        elif(self.name == 'R'):
            pass
        elif(self.name == 'Q'):
            pass
        elif(self.name == 'K'):
            pass
        else:
            print("O fucc")
            #raise ValueError('A very specific bad thing happened.')
