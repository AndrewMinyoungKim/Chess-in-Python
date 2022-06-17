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