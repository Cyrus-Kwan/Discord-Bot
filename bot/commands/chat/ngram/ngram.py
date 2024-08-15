# N-Grams
# -------------------------------------------------------------------------------
'''
A N-Gram is a type of stochastic process.
A N-Gram is a collection of random variables where the future states only depend on the current state.
N-Grams can be either discrete or continous.

For a N-Gram transition matrix:
- Each row must total to 1 (sum of probabilities of each transition)
- The probabilities must be non-negative

A N-Gram can be simulated from an initial distribution and transition matrix.
In our case, the initial state is New york City. From the initial state we can travel to:
    Paris, Cairo, Seoul or even within New York City.

The transition matrix contains the one step transition probabilities of moving from state to state.
'''
import pandas as pd
import numpy as np
import random
from words_graph import *

def ngram(start:str, stop:str, matrix:pd.DataFrame, n:int=None):
    current: str = start
    chain: list[str] = [start]

    if n:
        for i in range(n):
            word = poly_prob(matrix[current])
            chain.append(word.split()[-1])
            current = word
    else:
        while current != stop:
            word = poly_prob(matrix[current])
            chain.append(word.split()[-1])
            current = word
    
    return chain

def poly_prob(series:pd.Series):
    '''
    Returns the respective index based on the non-uniform probability distribution of a given series.
    '''
    if round(sum(series), 0) != 1:
        raise ValueError("The sum of probabilities must equal to 1.")
    cumulative = 0
    result = random.random()
    for i, value in series.items():
        cumulative += value
        if result <= cumulative:
            return i

def main():
    # transition_matrix = {
    # "NYC": [0.25, 0, 0.75, 1],
    # "Paris": [0.25, 0.25, 0, 0],
    # "Cairo": [0.25, 0.25, 0.25, 0],
    # "Seoul": [0.25, 0.5, 0, 0],
    # }

    # matrix_df = pd.DataFrame(data=transition_matrix, index=transition_matrix.keys())

    # text = """
    #     This is the house that Jack built. 
    #     This is the malt 
    #     That lay in the house that Jack built. 
    #     This is the rat, 
    #     That ate the malt 
    #     That lay in the house that Jack built. 
    #     This is the cat 
    #     That killed the rat, 
    #     That ate the malt 
    #     That lay in the house that Jack built. 
    # """

    # matrix = graph(string=text, n=1)
    # print(matrix)
    # generated = " ".join(ngram(start="That", stop="rat,", matrix=matrix, n=50))
    # print(generated)


    matrix = pd.read_csv("./geah.csv", index_col=0)
    generated = " ".join(ngram(start="in a tree.", stop="Let me be!", matrix=matrix, n=50))
    print(generated)

    return

if __name__ == "__main__":
    main()
