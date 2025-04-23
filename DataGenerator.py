import requests
import random
import os
from typing import Generator, Any

class Node:
    def __init__(self, data: Any|None = None) -> None:
        self.data = data
        self.next: Node|None = None

class LinkedList:
    def __init__(self) -> None:
        self.head: Node|None = None
        self.__size = 0

    def __repr__(self):
        output = ""
        nextNode = self.head
        while nextNode is not None:
            output += f"{nextNode.data} -> "
            nextNode = nextNode.next
        output += "None"
        return output

    def __len__(self) -> int:
        """ Return number of nodes in LinkedList"""
        if self.head and self.__size == 0:
            self.__recount()
        return self.__size
    
    def __getitem__(self, index) -> Any|None:
        if self.head:
            current = self.head
            i = 0
            while (i < index):
                current = current.next
                i += 1
                if current is None:
                    raise IndexError
            return current.data
        raise IndexError
    
    def __recount(self) -> int:
        self.__size = 0
        current = self.head
        while current is not None:
            self.__size += 1
            current = current.next
        return self.__size

    def prepend(self, data) -> None: 
        aNode = Node()
        aNode.data = data
        aNode.next, self.head = self.head, aNode
        self.__size += 1

    def append(self, data) -> None:
        if (type(data) is list):
            i = 0
            if self.head is None:
                self.head = Node(data[i])
                i += 1
            current = self.head
            while current.next is not None:
                current = current.next
            while i < len(data):
                self.__size += 1
                current.next = Node(data[i])
                current = current.next
            return
        
        aNode = Node(data)
        if self.head:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = aNode
            self.__size += 1
            return
        self.head = aNode
    
    def insertAfter(self, index, data) -> None:
        if self.head is None:
            self.head = Node(data)
            self.__size = 1
            return
        if index >= self.__size:
            raise IndexError
        current = self.head
        i = 0
        while (i < index):
            current = current.next
            i += 1
            if current is None:
                raise IndexError
        aNode = Node(data)
        aNode.next = current.next
        current.next = aNode
        self.__size += 1

    def remove(self, index) -> Any:
        current = self.head
        prev = None
        i = 0
        while (i < index) and (current is not None):
            prev = current
            current = current.next
            i += 1
        if current is None:
            raise IndexError
        if prev is None:
            self.head = current.next
        else:
            prev.next = current.next
            self.__size -= 1
        return current.data

    # precondition: give me a target that can be evaluated with == operator against the data
    def search(self, target) -> int:
        """ Give index of target else give -1"""
        i = -1
        if self.head:
            current = self.head
            i += 1
            while current.data != target:
                current = current.next
                i += 1
                if current is None:
                    return -1
            return i 
        return i

    def shuffle(self) -> None:
        # from here https://medium.com/@khemanta/shuffling-linked-list-nodes-a-uniform-approach-for-apple-challenge-14ffda6763c6
        indices = [i for i in range(self.__size)]
        # get new order by old index
        random.shuffle(indices)
        # empty first node
        head_new = Node()
        current_new = head_new

        for i in indices:
            current = self.head
            for _ in range(i):
                current = current.next
            # append value at index
            current_new.next = Node(current.data)
            # step forward
            current_new = current_new.next

        self.head = head_new.next

    def deepCopy(self) -> 'LinkedList':
        aList = LinkedList()
        current = self.head
        if not current:
            aList.head = None
            return aList
        aList.head = Node(current.data)
        aList.__size = 1
        current_new = aList.head
        current = current.next
        while current:
            current_new.next = Node(current.data)
            current_new = current_new.next
            current = current.next
            aList.__size += 1
        return aList


def getWords() -> list[str]:
    # got from stack overflow https://stackoverflow.com/questions/18834636/random-word-generator-python
    word_site = "https://www.mit.edu/~ecprice/wordlist.100000"
    response = requests.get(word_site)
    return [word.decode('ASCII') for word in response.content.splitlines()]

def getRandomWords(words) -> Generator[str]:
    
    return words[random.randint(0, len(words)-1)]

def generateDictionary(self, path, size):
    with open(path, 'w') as file:
        file.writelines('a')

    pass


if __name__ == "__main__":
    testList1 = LinkedList()
    WORDS = getWords()
    for _ in range(20):
        testList1.append(getRandomWords(WORDS))
    testList2 = testList1.deepCopy()
    testList2.shuffle()
    print(f"Test List 1:\n{testList1}")
    print(f"Test List 2:\n{testList2}")
