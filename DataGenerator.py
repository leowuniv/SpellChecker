import requests
import random
import os
from typing import Generator, Any



def getWords() -> list[str]:
    # got from stack overflow https://stackoverflow.com/questions/18834636/random-word-generator-python
    word_site = "https://www.mit.edu/~ecprice/wordlist.100000"
    response = requests.get(word_site)
    return [word.decode('ASCII') for word in response.content.splitlines()]

def getRandomWords2(words:list):
    return words[random.randint(0, len(words)-1)]

def getRandomWords(words:list) -> Generator[str]:
    temp = words.copy()
    random.shuffle(temp)
    for word in temp:
        yield word

def generateDictionary(self, path, size):
    with open(path, 'w') as file:
        file.writelines('a')

    pass


if __name__ == "__main__":
    testList1 = []
    WORDS = getWords()
    i = 0
    for word in getRandomWords(WORDS):
        testList1.append(word)
        i += 1
        if i >= 20:
            break
    print(f"Test List 1:\n{testList1}")
