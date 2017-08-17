

class TTT:
    
    # Parameters to evalue (if any of this indexes have the same value, someone won).
    wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6],
        ]
    
    def __init__(self):
        # Initialize the grid with blank(2) values.
        self.grid = [2 for _ in range(9)]
        self.turn = 0
    
    def show_table(self, guide = False):
        for x in range(3):
            for y in range(3):
                print(['X', '0', '~'][self.grid[x*3 + y]],
             end=' ')
            
            if guide:
            
                print('\t\t', end="")
                
                row = 3*x
                print(0+row, 1+row, 2+row)
            else:
                print()
    
    def move(self, pos):
        
        # According to the current(boolean) turn, set the position in the grid to that value.
        self.grid[pos] = int(self.turn)
        
        self.turn = not self.turn
    
    def used(self, pos):
        return self.grid[pos] != 2
    
    def who_won(self):
        g = self.grid
        # The default return value is -1
        # (none won).
        result = -1
        
        # Compares every parameter defined in wins to find a winning row.
        for p in self.wins:
            if g[p[0]] == g[p[1]] == g[p[2]]:
                if g[p[0]] != 2:
                    # Returns the winning value.
                    result = g[p[0]]
        
        if result == -1:
            # Counts all left empty spaces,
            #if there's none, it's a tie.
            empt = [x for x in g if x == 2]
            if not empt:
                result = 3
        
        # Posible results:
        #  0  ~= X won
        #  1  ~= Y won
        # -1   = none has won
        #  3   = none won
        return result
