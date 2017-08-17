# TicTacToe AI

This attempt is based in a mix of Neural network (fully-connected feed-forward) and a genetic algorithm.
(with a direct reproduction, cloning the parent).

Although the behavior and methods to do it are still not clear, the objective is.
The goal is to get a neural network that, given a list of inputs (the current state of the
game), returns a number between 0 and 8, representing a position in the table, and that
number is the next move the NN decides to make.
At the end, the trainned model must be able to win or tie every match it's tested in.


### - Current Model

#### Neural Network Structure.
(Hipothetical)

Possible states:

      0 = Empty

      1 = X

      2 = 0

#### - Inputs:

Table's current state:

    grid = [8 x (0, o 1, o 2)]
    --------------------------

    [2, 2, 2,

     2, 2, 2,

     2, 2, 2]
	   ^
    Empty Table.

The previous grid is the backend for the game, and the input for the neural network.

#### - Neural Network:
	
####Layers:

    Input	Layer:	 9 nodes
    -
    First 	Layer: 	18 nodes
    -
    Second 	Layer: 	27 nodes
    -
    Third 	Layer:	18 nodes
    -
    Output	Layer:	 1 nodes

####Weights:

		Input	-> 	First : ((9+1) x 18) 180
		-
		First	->	Second:	((18+1) x 18) 513
		-
		Second	->	Third :	((18+1) x 18) 504
		-
		Third	->	Output: ((18+1) x  1) 19


Weights are stored in a numpy array, with the format:

    weigths = [{72}, {486}, {486}, {18}]

Every weight at the begining has random a value between -1 and 1.

####Activation Function:

For the input, it's linear. For the hidden layers, sigmoidal. For the output, linear[?] (0...8)

####Guess:

> So... this part depends on the type of neural network I'm gonna use.
Since my current choice is a feed-forward network, the guessing step is made as follows:
(please correct me if any of this isn't right).

Inputs go into the input layer, pass to the first one being multiplied by that layers's weights, 
every node in the first layer calculates its result summing up the inputs times the weights, 
pass through the activation function and go through their connections to the next layer, repeating 
the process until reaching the output layer, which returns one of the posible positions in the grid.

####Train:

This is where things get complicated for me, because there's not much of a score in the game to be
returning as feedback for the network. There are many ways it could go, and setting in code which 
ways are better than others would go against the goal of the project: train the model to _learn_ 
how to play, and always win.

So, since I can't set a score reference for every move made by the network, thus I can't tell it 
what its error is, the training will be made in the Genetic Algorithm.


###Genetic Algorithm

###Subject:

The population for this GA will be a list of 50 Subjects.

A Subject contains a matrix of weights, the neural network that uses those weights to make a prediction,
and a few functions to handle the actions of the neural network and the score calculations for the GA.

####Some of the functions are:

+ <b>Move:</b>
Calls the neural networks guess functions, and returns its result.

+ <b>Calculate Fitness:</b>
				Based on the average of win and lost games (and number of bad moves made, like trying to move in 
				a used cell) gives a fitness score for the subject. How well it behaved.

+ <b>Mutation:</b>
				Given a matrix of weights randomly adjust a few (or none) of them and return the matrix.

+ <b>Reproduce:</b>
				Copies its weights into a new matrix, passes it to the mutation, creates a new Subject with
				those genes and returns the new subject.

####Main Process:

Having a starting population of 50 random subjects, the selection process consists in...

I've got two ways of doing it:

- Making them fight each other, by picking two random Subjects from the list and making them play a game.
That's done until all of them have played 20 times.

    Or

- Making them play with a random player, also playing 20 times for each Subject.


Whatever method I choose, the process will be the same:

For every Subject tested:
			
- Pass the grid to the subject, calling the Move function.

- If the move was ilegal (if it was made in an occupied cell), it loses, because it can't continue the
game. If the same grid is given to it, the same wrong result will come up.

- At the end of the match, calculate the final fitness of the Subject, assigning more points if it won, 
less if it lost or in the middle if it tied.

After all the matches have been done, its time to prepare the next generation.

The new_generation list is initialized empty.
A loop runs 50 times, to fill the new generation, and chooses randomly one of the current generation's
Subject to be reproduced, based on its fitness; if the fitness is high, then the probability to be chose too.
The new Subject, returned by the parent's Reproduce function is then added to the new generation and the loop
starts again, until the list is full.

With the new generation the main process starts again.

A save of the model (the list of weights in the GA) is made every... 15-ish generations as a Python Pickl.


- - -

Thats the current idea I have for the project. Maybe (definitely) there's a better way to do this. I just learned about
Q learning, that's based on a list of previous actions too. But, since I'm still new and trying to learn in this field,
maybe this way is the best I can come up with and try to acomplish.

A copy of my current code is included in the zip file, although it isn't finished, gives an idea of the way I'm going
with the programming part of it.