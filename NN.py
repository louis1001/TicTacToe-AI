import random
import math

def map_r(val, og_a, og_b, tg_a, tg_b, as_int = True):
    og_range = og_b - og_a
    constraint_val = val - og_a
    
    percent = constraint_val/og_range
    
    tg_range = tg_b - tg_a
    
    constraint_tg_val = percent * tg_range
    
    mapped = constraint_tg_val + tg_a
    
    if as_int:
        mapped= int(mapped)
    
    return mapped

class NeuralNet:
    
    def __init__(self, lyr_size):
        self.used = []

        self.layer_sizes = lyr_size

        self.weights = None

    max_iter = 50

    def sigmoid(self, x):
        sig = 1 / (1 + math.exp(-1 * x))
        return sig

    def activate_output(self, val):
        activated = map_r(val, -1, 1, 0, 9, True)
        return activated
    
    def guess(self, state):

        # # Randomized
        # choice = random.randint(0,8)
        # iters = 0
        # while choice in self.used:
        #     choice = random.randint(0,8)
        #     iters +=1
        #     if iters > self.max_iter:
        #         break
        
        # self.used.append(choice)

        # return choice

        prev_input = state[:]

        for index, layer in enumerate(self.weights):
            # Process the input of the previous layer, and calculate the next input
            
            current_sz = self.layer_sizes[index]
            segments = int(len(layer) / current_sz)

            outputs = []
            for x in range(current_sz):

                offset = segments * x
                node_weights = layer[offset : offset + segments]

                weigthed = node_weights * prev_input

                summed = sum(weigthed)

                result = self.sigmoid(summed)

                outputs.append(result)
            
            outputs.append(1)

            prev_input = outputs

        return self.activate_output(prev_input[0])

            # prev_input must be the output of the current layer.


