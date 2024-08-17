import pandas as pd
import numpy as np
import re

def words(string:str, n:int=1):
    '''
    Returns a list of all substrings where each substring is a sequence of n consecutive words.
    '''
    words: list[str] = string.split()
    n_words: list[list] = []

    for i in range(len(words)):
        if len(words[i:i+n]) >= n:
            n_words.append(words[i:i+n])

    return n_words

def graph(string:str, overlap:int=1):
    n: int = overlap + 1
    str_arr: list[list] = [" ".join(word) for word in words(string=string, n=n)]
    word_arr: list[str] = words(string=string, n=n)
    index: set[list] = set(str_arr)
    matrix: dict[float] = {word:[0]*len(index) for word in index}
    graph: pd.DataFrame = pd.DataFrame(matrix, index=matrix.keys())
    ref: dict[dict] = {col:{} for col in graph}

    for i, word in enumerate(word_arr):
        curr = word_arr[i][:n-1]
        prev = word_arr[i-1][1-n:]

        if curr == prev:
            row = " ".join(word_arr[i])
            col = " ".join(word_arr[i-1])
            graph.loc[row, col] += 1
            ref[col][row] = graph.loc[row, col]

    for col in ref.keys():
        total = sum(graph[col])
        for row, val in ref[col].items():
            graph.loc[row, col] = val/total

    return graph

def generate(start:str, stop:str, matrix:pd.DataFrame, n:int):
    chain: list[str] = []
    current: str = start
    count: int = 0

    while (current != stop) or (count < n):
        word = np.random.choice(matrix.index, p=matrix[current])
        chain.append(word.split()[-1])
        current = word
        count += 1

    return " ".join(chain)

def main():
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
    text = "The quick brown fox jumped over the lazy dog."
    matrix = graph(string=text, overlap=1)
    print(matrix.drop(columns=["lazy dog."]))

    # print(matrix)

    # with open("./the-velveteen-rabbit.txt") as file:
    #     text = file.read()
    #     matrix = graph(string=text, overlap=3)
    #     matrix.to_csv("./tvr.csv", index_label="Word")

    # matrix = pd.read_csv("./tvr.csv", index_col=0)
    start = np.random.choice(matrix.columns)
    stop = np.random.choice(matrix.index)
    string = generate(start=start, stop=stop, matrix=matrix, n=50)
    print(string)

    return

if __name__ == "__main__":
    main()