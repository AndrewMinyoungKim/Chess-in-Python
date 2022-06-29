WIDTH, HEIGHT = 800, 800
ROW, COL = 8, 8
SQUARE = HEIGHT//COL
#SQUARE = pygame.display.get_window_size() // ROW # not initialized

# the players
WHITE = 0xFFFFFF
BLACK = 0x000

# board colours
GREY = (240, 233, 216)
GREEN = (110, 235, 125)

ORANGE = 0xf5a031 # used for normal move display
RED = 0xed0c1b # used for check display
GOLD = 0xFFD700 # Winning Checkmate Colour!
BROWN = 0xDAA06D # Losing Checkmate Colour :(
PURPLE = 0x6134eb # highlight selected piece
NAVY = (15, 28, 48) # padding/borders

# back rank setup order at start of match
BACK_RANK_SETUP = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
# set of the back rank pieces, and add pawns, thus a set containing every piece type
PIECE_TYPE = set(BACK_RANK_SETUP)
PIECE_TYPE.add('P')
#PIECE_TYPE.update('PO')

# dictionary for file names
FILE = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

# one global variable to show whether the game is completed or not
game_over = False