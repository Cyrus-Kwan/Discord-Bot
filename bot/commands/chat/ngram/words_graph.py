import pandas as pd
from decimal import *

def words(string:str, n:int=1):
    words = string.split()
    chunks = [" ".join(words[i:i+n]) for i in range(len(words))]
    return chunks

def graph(string:str, n:int=1):
    keys = set(words(string=string, n=n))
    split = words(string=string, n=n)
    matrix = {word:[0.0]*len(keys) for word in keys}
    graph = pd.DataFrame(matrix, index=matrix.keys())

    for col in graph:
        for word, row in enumerate(split):
            if n == 1:
                if split[word-1] == col:
                    graph.loc[row, col] += 1.0
            else:
                if split[word].split()[1-n:] == col.split()[:n-1]:
                    # print(f"{split[word].split()} | {col.split()}, {row}, {col}")
                    graph.loc[col, row] += 1.0

    for col in graph:
        total = graph[col].sum()
        if total != 0:
            graph[col] = graph[col]/total

    return graph

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

    # text = "The quick brown fox jumped over the lazy dog."

    # matrix = graph(string=text, n=2)

    # print(matrix)

    with open("./green-eggs-and-ham.txt") as file:
        text = file.read()
        matrix = graph(string=text, n=3)
        matrix.to_csv("./geah.csv", index_label="Word")

    #     for col in matrix:
    #         print(sum(matrix[col]))
    return

if __name__ == "__main__":
    main()