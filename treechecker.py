import requests
import random
import re

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
    # sanity check
    dictList.append("hey\n")
    with open(path, 'w') as file:
        file.writelines(dictList)

def generateSentenceFile(WORDS:list[str], path:str, size:int, minWords:int, maxWords:int):
    sentList = [getRandomSentence(WORDS,minWords, maxWords)+'\n' for _ in range(size-1)]
    # including a real sentence for sanity check with punctuation
    sentList.append(' '.join("Hey y'all, Scott here; I hate walls! Have you ever realized there's a reason for these things to exist? That's right. You haven't because there isn't any. But for some reason, the wall companies have a monopoly on console video games.".split(' ')[:maxWords])+'.')
    with open(path, 'w') as file:
        file.writelines(sentList)


# AVL Tree

class Node:
  def __init__(self, data):
    self.data = data
    self.left = None
    self.right = None
    self.height = 0

class AVLTree:
  # Constructor
  def __init__(self):
    self.root = None

  def traverse(self):
    """generator preorder traverse from head"""
    yield from self._traverse(self.root)

  def _traverse(self, current):
    """generator preorder traverse from current node"""
    if current:
      yield current
      yield from self._traverse(current.left)
      yield from self._traverse(current.right)
  
  def getHeight(self, node):
    if not node:
      return -1
    return node.height

  def calculateHeight(self, node):
    if not node:
      return -1
    return max(self.getHeight(node.left), self.getHeight(node.right)) + 1

  def getBalance(self, node):
    if not node:
      return 0
    return self.getHeight(node.left) - self.getHeight(node.right)

  # Rotations
  def rightRotate(self, current):
    newRoot = current.left
    t2 = newRoot.right
    current.left = t2
    newRoot.right = current

    if current == self.root:
        self.root = newRoot

    current.height = self.calculateHeight(current)
    newRoot.height = self.calculateHeight(newRoot)
    return newRoot

  def leftRotate(self, current):
    newRoot = current.right
    t2 = newRoot.left
    current.right = t2
    newRoot.left = current
    
    if current == self.root:
        self.root = newRoot

    current.height = self.calculateHeight(current)
    current.height = self.calculateHeight(newRoot)
    return newRoot

  def leftRightRotate(self, current):
    current.left = self.leftRotate(current.left)
    return self.rightRotate(current)

  def rightLeftRotate(self, current):
    current.right = self.rightRotate(current.right)
    return self.leftRotate(current)
  
  def balanceTree(self):
    balance = self.getBalance(self.root)
    # if skewed left
    if balance > 1:
      # check for double rotation
      current = self.root.left
      if not current:
        return
      if self.getHeight(current.left) < self.getHeight(current.right):
        self.leftRightRotate(self.root)
        return
      self.rightRotate(self.root)
    # if skewed left
    if balance < -1:
      # check for double rotation
      current = self.root.right
      if not current:
        return
      if self.getHeight(current.right) < self.getHeight(current.left):
        self.rightLeftRotate(self.root)
        return
      self.leftRotate(self.root)

  # Insert
  def insert(self, data) -> None:
    if self.root is None:
        self.root = Node(data)
        return
    self._insert(self.root, data)
    self.balanceTree()

  def _insert(self, current, data):
    if current is None:
      return Node(data)
    # if not base case, navigate to correct subtree
    elif data <= current.data:
      current.left = self._insert(current.left, data)
    elif data > current.data:
      current.right = self._insert(current.right, data)
    return current

  # Search
  def search(self, data):
    return self._search(self.root, data)
  
  def _search(self, current, data):
    for node in self._traverse(current):
      if node.data == data:
        return node

  # Delete
  def delete(self, data):
    self._delete(self.root, data)
    self.balanceTree()
    return 

  def _delete(self, current, data):
    if current is None:
      return
    
    elif data < current.data:
      current.left = self._delete(current.left, data)
    elif data > current.data:
      current.right = self._delete(current.right, data)

    else:
      # when 0 children or
      # only right child
      if current.left is None:
        return current.right
      # only left child
      if current.right is None:
        return current.left
      
      # both children, inorder successor
      temp = current.right
      while temp.left is not None:
        temp = temp.left
      current.data = temp.data
      # delete old inorder successor
      current.right = self._delete(current.right, temp.data)

  # print the dictionary in-order traversal with balances; alphabet ascending order a-z
  def inorderTrav(self, node):
    if node:
      self.inorderTrav(node.left) # travel left if possible
      balance = self.getBalance(node)
      print(f"{node.data} (balance: {balance})")
      self.inorderTrav(node.right) # travel right if possible

# Read Dictionary File
'''
15 unique words
'''
def getDictionaryWords(path) -> list[str]:
  with open(path, 'r') as file:
    words = [word.rstrip() for word in file.readlines()]
  return words

# Read a document (spell checking)
'''
Split individual words; all lowercase
'''
def getWordsFromText(path) -> list[str]:
  tokenizeRegex = r'(\w+\'?\w+)' # does not account for apostraphes in compound or possessive words
  with open(path, 'r') as file:
    lines = file.readlines()
  tokens = []
  for line in lines:
    for token in re.finditer(tokenizeRegex, line):
      tokens.append(token[0].lower())

  return tokens

# =================================================

# https://docs.python.org/2/library/sets.html
if __name__ == "__main__":
  dictPath = './dictionary.txt'
  sentPath = './sentences.txt'
  WORDS = getWords()

  generateDictionaryFile(WORDS, dictPath, 20) # at least 15 unique words
  generateSentenceFile(WORDS, sentPath, 20, 12, 25) # 20 wrds, 12 min per sen, 25 max
  dictWords:list = getDictionaryWords(dictPath)
  tokens = getWordsFromText(sentPath)

  print("\nWords in Dictionary:\n")
  print(dictWords) # print words in dictionary
  print("\nTokens from Sentences:\n")
  print(tokens) # words from sentence
  
  tree = AVLTree() 
  for word in dictWords: #add dictionary words in tree
    tree.insert(word)

  # Displaying misspelled words and tree
  '''
  Print tree with inorder traversal
  '''
  misspelled = set()
  for token in tokens:
    if tree.search(token) is None:
        misspelled.add(token) # add misspelled word to set (not in dictionary); will only appear once
  print("\nMisspelled Words:\n") 
  print(misspelled) # show all final misspelled words

  print("\nInorder Traversal Tree:\n")
  tree.inorderTrav(tree.root)
  #print()
