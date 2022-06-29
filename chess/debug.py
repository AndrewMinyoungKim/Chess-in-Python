class Debugger():
    def __init__(self):
        pass

    # print the entire state of the game to see every square's detail
    def print_state(self, state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if(state[i][j]):
                    print(f"{state[i][j].row}, {state[i][j].col}: {state[i][j].name}: {state[i][j]}")
                else:
                    print(f"{i}, {j}: {state[i][j]}")

    # print the piece object's information
    def print_piece(self, piece):
        print(f"Name: {piece.name}")
        print(f"Row: {piece.row}")
        print(f"Column: {piece.col}")
        print(f"Colour: {piece.colour}")
        print("+++++")