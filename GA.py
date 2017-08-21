import numpy
import os
import copy
import random
import pickle
from NN import NeuralNet
from TicTacToe import TTT

ios = True
try:
    import console
    import TUi
except:
    import basicInterface
    ios = False


class RandomPlayer:

    def guess(self):
        return random.randint(0,9)

def fill_genes():
    a = numpy.random.uniform(-1, 1, 180)
    b = numpy.random.uniform(-1, 1, 513)
    c = numpy.random.uniform(-1, 1, 504)
    d = numpy.random.uniform(-1, 1, 19)

    new_genes = numpy.array([a, b, c, d]).transpose()

    return new_genes


# class Subject:
#
#     mutation_rate = 0.01
#
#     def __init__(self, dna = None, name=''):
#
#         if dna is None:
#             self.genes = fill_genes()
#         else:
#             self.genes = dna
#
#         self.name = name
#         self.wins = 0
#         self.plays = 0
#         self.nn = NeuralNet([18, 27, 18, 1])
#         self.nn.weights = self.genes
#         self.fitness = 0
#
#     def guess(self, state, p2 = True):
#         inputs = []
#
#         for x in state:
#             if p2 and (x != 2):
#                 inputs.append(int(not x))
#             else:
#                 inputs.append(x)
#
#         inputs.append(1)
#
#         return self.nn.guess(inputs)
#
#     def mutate(self, ws=None):
#         if ws is None:
#             ws = copy.deepcopy(self.genes)
#         else:
#             ws = copy.deepcopy(ws)
#
#         for ly in ws:
#             for wg in ly:
#                 if random.random() > self.mutation_rate:
#                     change = random.triangular(-0.3, 0.3)
#                     wg += change
#
#         return ws
#
#     def reproduce(self):
#         new_genes = copy.deepcopy(self.genes)
#
#         new_genes = self.mutate(new_genes)
#
#         return Subject(new_genes)
#
#     def calculate_fitness(self):
#         proportion_won = self.wins / self.plays
#         self.fitness = proportion_won
#         return self.fitness

class Subject:
    mutation_rate = 0.01

    def __init__(self, dna=None, name=''):

        if dna is None:
            self.genes = fill_genes()
        else:
            self.genes = dna

        self.name = name
        self.wins = 0
        self.plays = 0
        self.nn = NeuralNet([18, 27, 18, 1])
        self.nn.weights = self.genes
        self.fitness = 0

    def guess(self, state, p2=True):
        inputs = []

        for x in state:
            if p2 and (x != 2):
                inputs.append(int(not x))
            else:
                inputs.append(x)

        inputs.append(1)

        return self.nn.guess(inputs)

    def mutate(self, ws=None):
        if ws is None:
            ws = copy.deepcopy(self.genes)
        else:
            ws = copy.deepcopy(ws)

        for ly in ws:
            for wg in ly:
                if random.random() > self.mutation_rate:
                    change = random.triangular(-0.3, 0.3)
                    wg += change

        return ws

    def reproduce(self, other):
        new_genes = (self.genes + other.genes) / 2

        new_subj = Subject(new_genes)
        return new_subj


    def calculate_fitness(self):
        proportion_won = self.wins / self.plays
        self.fitness = proportion_won
        return self.fitness


class GA:

    def __init__(self, pop_size = 50):
        
        self.pop_size = pop_size
        
        self.generations = 0
        
        self.population = [Subject(name = 'S-{}-{}'.format(self.generations, cont)) for cont in range(pop_size)]
        
        self.processed = {}
    
    def get_best_fitness(self, worst = False):



        fitness = [x for x in self.population]
        fitness.sort(key=lambda x: x.calculate_fitness())

        if worst:
            return fitness[0]
        else:
            return fitness[-1]
    
    def average_fitness(self):
        fitness = [x.calculate_fitness() for x in self.population]
        return sum(fitness)/len(fitness)
    
    def prep_next_gen(self):
        
        gen_cont = self.generations + 1
        
        new_gen = []
        cont = 0
        
        for _ in range(self.pop_size):
            
            parent1 = None
            parent2 = None
            while True:
                parent1 = random.choice(self.population)
                if random.random() < parent1.calculate_fitness():
                    break

            while True:
                parent2 = random.choice(self.population)
                if random.random() < parent2.calculate_fitness():
                    break

            new_subj = parent1.reproduce(parent2)
            new_subj.name = 'S-{}-{}'.format(gen_cont, cont)
            cont += 1
            
            new_gen.append(new_subj)
        
        self.population = new_gen
        self.generations = gen_cont
    
    values = ['X', '0', '~']
    
    def generation(self):
        # A for controls how many games each player will have.
        for step in range(20):
            
            # Makes a copy of the population and shuffles it
            # to randomize the pairs.
            current_pop = self.population[:]
            random.shuffle(current_pop)
            
            # Play until all of the subject have played a game.
            while len(current_pop) > 0:

                # Pick a pair of Subjects from the top of the list
                # to play against each other.
                player1 = current_pop.pop()
                player2 = current_pop.pop()
                
                # Increment the counter of plays of both Subjects
                player1.plays += 1
                player2.plays += 1
                
                # Initialize the board.
                current_t = TTT()
                players = [player1, player2]
                
                # Play til someone wins the game
                while current_t.who_won() == -1:
                    # Gets the guess of the current player
                    
                    next_move = players[current_t.turn].guess(current_t.grid)
                    
                    if current_t.used(next_move):
                        # If the guess is invalid, exit the game.
                        # That player lost.
                        break
                    else:
                        # If the move is valid, make it.
                        current_t.move(next_move)
                
                #current_t.show_table()
                
                # The winner is calculated according to the boards function.
                winner = current_t.who_won()

                if winner == -1:
                    # This is used when someone made a bad move. The player
                    # that has not the turn wins.
                    players[not current_t.turn].wins += 1
                    
                elif winner == 3:
                    # If it's a tie, both win.
                    
                    player1.wins += 1
                    player2.wins += 1
                    # print("It's a tie")
                    # print("X", player1.wins, "0", player2.wins)
                    
                else:
                    # If the game ended normally (one got three in a row)
                    # increment the winner's wins counter.
                    
                    players[winner].wins += 1
                    # print(self.values[winner], 'won')
        
        print('Done')

    def get_best_against_random(self):
        for step in range(20):

            # Makes a copy of the population and shuffles it
            # to randomize the pairs.
            current_pop = self.population[:]

            # Play until all of the subject have played a game.
            while len(current_pop) > 0:

                # Pick a pair of Subjects from the top of the list
                # to play against each other.
                player1 = current_pop.pop()
                player2 = RandomPlayer()

                # Increment the counter of plays of both Subjects
                player1.plays += 1

                # Initialize the board.
                current_t = TTT()
                players = [player1, player2]

                # Play til someone wins the game
                while current_t.who_won() == -1:
                    # Gets the guess of the current player

                    next_move = players[current_t.turn].guess(current_t.grid)

                    if current_t.used(next_move):
                        # If the guess is invalid, exit the game.
                        # That player lost.
                        break
                    else:
                        # If the move is valid, make it.
                        current_t.move(next_move)

                # current_t.show_table()

                # The winner is calculated according to the boards function.
                winner = current_t.who_won()

                if winner == -1:
                    # This is used when someone made a bad move. The player
                    # that has not the turn wins.
                    players[not current_t.turn].wins += 1

                elif winner == 3:
                    # If it's a tie, both win.

                    player1.wins += 1
                    player2.wins += 1
                    # print("It's a tie")
                    # print("X", player1.wins, "0", player2.wins)

                else:
                    # If the game ended normally (one got three in a row)
                    # increment the winner's wins counter.

                    players[winner].wins += 1
                    # print(self.values[winner], 'won')
            
# for x in a.population:
#     print(x.name + ": "+ str(x.wins) + "/" + str(x.plays) + " = " + str(x.wins/x.plays))

save_path = 'Saves'
file_template = 'gen-{}-save.pkl'


def save_state(obj):
    
    save_file = os.path.join(save_path, file_template.format(obj.generations))
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    
    if not os.path.exists(save_file):
        os.system('touch ' + save_file)
    
    str_save = pickle.dumps(obj)

    with open(save_file, 'wb') as f:
        f.write(str_save)

genetic_a = GA()


def summary(ga):
    print('-'*40)
    print('Generation: ' + str(ga.generations))
    best_f = ga.get_best_fitness().fitness
    print('Best fitness: ' + str(best_f))
    print('-'*40)


def step_generations(count = 1, prep = True, random_scoring = True):
    
    while count > 0:
    
        print('Starting Generation', genetic_a.generations)

        if random_scoring:
            genetic_a.generation()
        else:
            genetic_a.get_best_against_random()

        if genetic_a.generations % 50 == 0:
            # save_state(genetic_a)
            pass
        
        summary(genetic_a)
        
        if prep:
            genetic_a.prep_next_gen()
        
        count -= 1


if ios:
    interface = TUi.show
else:
    interface = basicInterface.show


def main():
    while True:

        print('Funciones:')
        print('1- Avanzar una generacion')
        print('2- Avanzar n generaciones')
        print('3- Guardar estado actual')
        print('4- Jugar contra el mejor')
        print('5- Jugar contra el peor')
        print('6- Salir')

        response = input()

        num_generations = 0

        if response == '1':
            num_generations = 1
        elif response == '2':
            print('¿Cuantas generaciones?')
            try:
                num_generations = int(input())
            except ValueError:
                continue
        elif response == '3':
            save_state(genetic_a)
        elif response == '4':
            step_generations(1, False)
            best = genetic_a.get_best_fitness()
            try:
                interface(best)
            except KeyboardInterrupt:
                pass
            continue
        elif response == '5':
            step_generations(1, False)
            best = genetic_a.get_best_fitness()
            try:
                interface(best, True)
            except KeyboardInterrupt:
                pass
            continue
        elif response == '6':
            break

        if ios:
            console.clear()
        else:
            os.system('cls')

        step_generations(num_generations)


if __name__ == '__main__':
    main()
