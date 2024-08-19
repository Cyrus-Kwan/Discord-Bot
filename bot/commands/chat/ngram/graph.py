import numpy as np
import json
import asyncio

def words(string:str, n:int=1):
    '''
    Returns a list of all substrings where each substring is a sequence of n consecutive words.
    '''
    words: list[str] = string.split()
    n_words: list[list] = []

    for i in range(len(words)):
        if len(words[i:i+n]) >= n:
            sub_str: str = words[i:i+n]
            n_words.append(sub_str)

    return n_words

def adj_graph(string:str, union:int=1):
    '''
    Returns adjacency list that contains only the relationships between each state and the next
    '''
    n: int = union + 1
    word_arr: list[str] = [" ".join(word) for word in words(string=string, n=n)]
    slice_arr: list[str] = words(string=string)

    graph: dict = {word:{} for word in word_arr}

    for i in range(len(word_arr)):
        curr_slice: list[str] = slice_arr[i][1-n:]
        next_slice: list[str] = slice_arr[i][:n-1]
        curr: str = word_arr[i]
        prev: str = word_arr[i-1]

        if prev in graph[curr].keys():
            graph[curr][prev] += 1
        else:
            graph[curr][prev] = 1

    for curr in graph.keys():
        total = sum(graph[curr].values())
        for prev in graph[curr].keys():
            graph[curr][prev] = graph[curr][prev]/total

    return graph

def main():
    with open(file="./4chan.txt", mode="r") as file:
        text = file.read()
        train = adj_graph(string=text, union=2)
        dump = json.dumps(train, indent=2)

    with open(file="./train_4c.json", mode="w") as new_file:
        new_file.write(dump)

if __name__ == "__main__":
    main()