from binary_search_tree.linkedbst import LinkedBST
import codecs
import time
import random
import sys


def random_word():
    """
    return random word from list
    :return: str
    """
    return random.choice(readed_file)


def read_file():
    """
    read words from file
    :return: list
    """
    read = list()
    with codecs.open("base.lst", 'r', 'utf-8') as file1:
        lines = file1.readlines()
        for line in lines:
            read.append(line.strip().split()[0])
    return read


readed_file = read_file()[:10000]


def search_in_dict_with_key():
    """
    return time to search for 1000 words in the dictionary
    :return: float
    """
    dictionary = dict()
    dictionary.fromkeys(readed_file)
    start = time.time()
    for i in range(1000):
        dictionary.get(random_word())
    return time.time() - start


def search_in_dict():
    """
    return time to search for 1000 words in the dictionary
    :return: float
    """
    dictionary = dict()
    dictionary.fromkeys(readed_file)
    start = time.time()
    for i in range(1000):
        word = random_word()
        for i in dictionary:
            if dictionary[i] == word:
                break
    return time.time() - start


def search_in_tree():
    """
    return time to search for 1000 words in the tree
    :return: float
    """
    tree = LinkedBST()
    sys.setrecursionlimit(150000)
    for word in readed_file:
        tree.add(word)
    start = time.time()
    for i in range(1000):
        tree.find(random_word())
    return time.time() - start


def search_in_balanced_tree():
    """
    return time to search for 1000 words in the balanced tree
    :return: float
    """
    tree = LinkedBST()
    sys.setrecursionlimit(150000)
    for word in readed_file:
        tree.add(word)
    tree.rebalance()
    start = time.time()
    for i in range(1000):
        tree.find(random_word())
    return time.time() - start


print("Time to search for 1000 words in the dictionary with key : ", \
      search_in_dict_with_key())
print("Time to search for 1000 words in the dictionary : ", \
      search_in_dict())
print("Time to search for 1000 words in the tree : ", search_in_tree())
print("Time to search for 1000 words in the balanced tree : ",
      search_in_balanced_tree())
