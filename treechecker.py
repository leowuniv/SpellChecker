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

    current.height = self.calculateHeight(current)
    newRoot.height = self.calculateHeight(newRoot)
    return newRoot

  def leftRotate(self, current):
    newRoot = current.right
    t2 = newRoot.left
    current.right = t2
    newRoot.left = current
    
    #if current == self.root:
    #self.root = newRoot

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

# Displaying misspelled words and tree
'''
Print tree with inorder traversal
'''

if __name__ == "__main__":
  dictPath = './dictionary.txt'
  dictWords = getDictionaryWords(dictPath)