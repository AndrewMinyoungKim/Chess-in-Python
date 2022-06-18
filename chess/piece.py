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


    # CREATE A DRAW PAWN OPTIONS FUNCTION IN BOARD, AND JUST BRING BACK A LIST OF COORDINATES THAT ARE AVAILABLE FOR MOVING TO GAME SO YOU CAN CHECK FOR CHECKS TO ENSURE ITS A
    # VALID MOVE AND POP OUT ANY MOVES THAT CAUSE A CHECK
    # CHECK FOR WHEN YOUR OWN PIECE IS IN THE WAY, AND TRAIL STOPS WHEN YOU MEET OPPONENT PIECE, AND IF INDEX OUT OF RANGE OF BOARD
    def pawn_movement(self, erase, board, state, win):
        avail_moves = []

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

    def knight_movement(self, erase, board, state, win):
        avail_moves = []
        return avail_moves



    def bishop_movement(self, erase, board, state, win):
        avail_moves = []
        row, col = self.row, self.col
        box_colour = ORANGE

        # NW
        row = self.row - 1
        col = self.col - 1
        while(row >= 0 and col >= 0 and not state[row][col]):
            if(erase):
                box_colour = GREY if (row + col) % 2 == 0 else GREEN
            board.draw_square(row, col, win, box_colour)
            row -= 1
            col -= 1
        if(row >= 0 and col >= 0):
            if(state[row][col].colour != self.colour):
                if(erase):
                    box_colour = GREY if (row + col) % 2 == 0 else GREEN
                board.draw_selected_piece(row, col, win, box_colour, state)

        # NE
        row = self.row - 1
        col = self.col + 1
        while(row >= 0 and col < 8 and not state[row][col]):
            if(erase):
                box_colour = GREY if (row + col) % 2 == 0 else GREEN
            board.draw_square(row, col, win, box_colour)
            row -= 1
            col += 1
        if(row >= 0 and col < 8):
            if(state[row][col].colour != self.colour):
                if(erase):
                    box_colour = GREY if (row + col) % 2 == 0 else GREEN
                board.draw_selected_piece(row, col, win, box_colour, state)

        # SE
        row = self.row + 1
        col = self.col + 1
        while(row < 8 and col < 8 and not state[row][col]):
            if(erase):
                box_colour = GREY if (row + col) % 2 == 0 else GREEN
            board.draw_square(row, col, win, box_colour)
            row += 1
            col += 1
        if(row < 8 and col < 8):
            if(state[row][col].colour != self.colour):
                if(erase):
                    box_colour = GREY if (row + col) % 2 == 0 else GREEN
                board.draw_selected_piece(row, col, win, box_colour, state)

        # SW
        row = self.row + 1
        col = self.col - 1
        while(row < 8 and col >= 0 and not state[row][col]):
            if(erase):
                box_colour = GREY if (row + col) % 2 == 0 else GREEN
            board.draw_square(row, col, win, box_colour)
            row += 1
            col -= 1
        if(row < 8 and col >= 0):
            if(state[row][col].colour != self.colour):
                if(erase):
                    box_colour = GREY if (row + col) % 2 == 0 else GREEN
                board.draw_selected_piece(row, col, win, box_colour, state)

        #return avail_moves

    # rook movement
    #CHECK FOR CHECKS
    def rook_movement(self, erase, board, state, win):
        avail_moves = []
        row, col = self.row, self.col
        box_colour = ORANGE

        #CHECK FOR CHECKS
        # ADD TO LIST AVAILBLE MOVES AND RETURN TO GAME AND CALL BOARD FUNCTIONS FROM THERE



        # rank movement
        # left
        row = self.row - 1
        while(row >= 0 and not state[row][col]):
            if(erase):
                box_colour = GREY if (row + col) % 2 == 0 else GREEN
            board.draw_square(row, col, win, box_colour)
            row -= 1
        if(row >= 0):
            if(state[row][col].colour != self.colour):
                if(erase):
                    box_colour = GREY if (row + col) % 2 == 0 else GREEN
                board.draw_selected_piece(row, col, win, box_colour, state)

        # right
        row = self.row + 1
        while(row < 8 and not state[row][col]):
            if(erase):
                box_colour = GREY if (row + col) % 2 == 0 else GREEN
            board.draw_square(row, col, win, box_colour)
            row += 1
        if(row < 8):
            if(state[row][col].colour != self.colour):
                if(erase):
                    box_colour = GREY if (row + col) % 2 == 0 else GREEN
                board.draw_selected_piece(row, col, win, box_colour, state)

        row = self.row
        # file movement
        # up
        col = self.col - 1
        while(col >= 0 and not state[row][col]):
            if(erase):
                box_colour = GREY if (row + col) % 2 == 0 else GREEN
            board.draw_square(row, col, win, box_colour)
            col -= 1
        if(col >= 0):
            if(state[row][col].colour != self.colour):
                if(erase):
                    box_colour = GREY if (row + col) % 2 == 0 else GREEN
                board.draw_selected_piece(row, col, win, box_colour, state)
        
        # down
        col = self.col + 1
        while(col < 8 and not state[row][col]):
            if(erase):
                box_colour = GREY if (row + col) % 2 == 0 else GREEN
            board.draw_square(row, col, win, box_colour)
            col -= 1
        if(col < 8):
            if(state[row][col].colour != self.colour):
                if(erase):
                    box_colour = GREY if (row + col) % 2 == 0 else GREEN
                board.draw_selected_piece(row, col, win, box_colour, state)

        #return avail_moves

    def queen_movement(self, erase, board, state, win):
        avail_moves = []
        # straight = self.rook_movement(erase, board, state, win)
        # diagonal = self.bishop_movement(erase, board, state, win)

        #using a quick loop to append everything
        # for direction in (straight, diagonal):
        #    avail_moves.append(direction) #what is the name of the extended list?

        #using a list comprehension and normal loop to append
        # avail_moves = [straight[i] for i in straight]
        # for i in diagonal:
        #     avail_moves.append(diagonal[i])

        self.rook_movement(erase, board, state, win)
        self.bishop_movement(erase, board, state, win)

        # return avail_moves

    def king_movement(self, erase, board, state, win):
        avail_moves = []
        return avail_moves

    # movement of each piece
    # need to consider check! and mate!
    def movement(self, erase, board, state, win):
        #white_piece = WHITE if self.colour == WHITE else BLACK
        if(self.name == 'P'):
            self.pawn_movement(erase, board, state, win)
        elif(self.name == 'N'):
            self.knight_movement(erase, board, state, win)
        elif(self.name == 'B'):
            self.bishop_movement(erase, board, state, win)
        elif(self.name == 'R'):
            self.rook_movement(erase, board, state, win)
        elif(self.name == 'Q'):
            self.queen_movement(erase, board, state, win)
        elif(self.name == 'K'):
            self.king_movement(erase, board, state, win)
