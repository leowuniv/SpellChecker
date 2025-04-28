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

  def leftRotate
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

  # Insert
  def insert:
    pass

  # Search
  def search:
    pass

  # Delete
  def delete:
    pass
