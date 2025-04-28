import requests
import random
import os



def getWords() -> list[str]:
    # got from stack overflow https://stackoverflow.com/questions/18834636/random-word-generator-python
    # word_site = "https://www.mit.edu/~ecprice/wordlist.100000"
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    return [word.decode('ASCII') for word in response.content.splitlines()]

def getRandomWords2(words:list):
    """Pick a random word that could be repeated"""
    return words[random.randint(0, len(words)-1)]

def getRandomWords(words:list):
    """Pick a random word that cannot be repeated"""
    temp = words.copy()
    random.shuffle(temp)
    for word in temp:
        yield word

def getRandomSentence(WORDS:list[str], minWords:int, maxWords:int):
    sentence = ""
    for _ in range(random.randint(minWords, maxWords)):
        sentence += getRandomWords2(WORDS) + ' '
    sentence = sentence[:-1] + '.'
    return sentence

def generateDictionaryFile(WORDS:list[str], path:str, size:int):
    dictList = [next(getRandomWords(WORDS))+'\n' for _ in range(size)]
    with open(path, 'w') as file:
        file.writelines(dictList)

def generateSentenceFile(WORDS:list[str], path:str, size:int, minWords:int, maxWords:int):
    sentList = [getRandomSentence(WORDS,minWords, maxWords)+'\n' for _ in range(size-1)]
    # including a real sentence for sanity check with punctuation
    sentList.append(' '.join("Hey y'all, Scott here; I hate walls! Have you ever realized there's a reason for these things to exist? That's right. You haven't because there isn't any. But for some reason, the wall companies have a monopoly on console video games.".split(' ')[:maxWords])+'.')
    with open(path, 'w') as file:
        file.writelines(sentList)

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

    dictPath = './dictionary.txt'
    sentPath = './sentences.txt'
    generateDictionaryFile(WORDS, dictPath, 20)
    generateSentenceFile(WORDS, sentPath, 20, 12, 25)