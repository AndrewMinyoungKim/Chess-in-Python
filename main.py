import pygame
import sys

from chess.constants import WIDTH, HEIGHT, SQUARE
from chess.game import Game

class Main:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')

    def get_x_y_pos(self, pos):
        x, y = pos
        row = y // SQUARE
        col = x // SQUARE
        return row, col

    def run(self):
        self.done = False
        self.clock = pygame.time.Clock()
        self.game = Game(self.window)

        while not self.done:

            self.clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pos = pygame.mouse.get_pos()
                    self.row, self.col = self.get_x_y_pos(self.pos)

                    self.game.mouseclick(self.row, self.col)

            self.game.update()


if __name__ == '__main__':
    play = Main()
    play.run()