from TicTacToe import TTT
ios = True
try:
    import console
except:
    import os
    ios = False

import random

values = ["X", "O", "•", "nadie"]

guide = False

def show_table(g):
    for x in range(3):
        for y in range(3):
            print(values[g.grid[x*3 + y]],
         end=' ')
        
        if guide:
        
            print('\t\t', end="")
            
            row = 3*x
            print(0+row, 1+row, 2+row)
        else:
            print()

def show(agent = None):

    keep_playing = 'y'

    while keep_playing != 'n':
        g = TTT()
        
        while g.who_won() == -1:
            if ios:
                console.clear()
            else:
                os.system('cls')
            show_table(g)
            if not g.turn:
                print("Escribe una posicion, jugador", int(g.turn) + 1)
                p = int(input())
                
                if p > 8:
                    continue
            else:
                if agent != None:
                    p = agent.guess(g.grid)
                else:
                    p = random.randint(0,8)
                
            if g.grid[p] == 2:
                g.move(p)
        
        if ios:
            console.clear()
        else:
            os.system('cls')
        
        show_table(g)
        
        print("\n\n")
        
        print(values[g.who_won()], "ganó!!")
        
        keep_playing = input("Seguir? (y/n)\n")[0]

if __name__ == '__main__':
    show()