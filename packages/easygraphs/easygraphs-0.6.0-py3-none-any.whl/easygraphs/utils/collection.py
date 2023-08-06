'''

Author: Zeng Siwei
Date: 2021-01-29 16:16:06
LastEditors: Zeng Siwei
LastEditTime: 2021-04-09 16:16:10
Description: 

'''

class Incdict(object):
    '''
    Renumber items. Just traverse items using incdict[item] to get the new order.

    Returns: 
	
    Usage: 
        dict_node = incdict()
        list_src, list_dst = [], []
        for i, line in enumerate(file):
            tokens = line.strip().split()
                list_src.append(dict_node[tokens[0]])
                list_dst.append(dict_node[tokens[1]])
        del dict_node
    '''

    def __init__(self, items = None, start_from_one = False):
        self.dict = dict()
        self.cnt = 0
        if start_from_one:
            self.cnt = 1
        if items:
            for item in items:
                self.__getitem__(item)

    
    def __getitem__(self, k):
        obj = self.dict.get(k, None)
        if obj is None:
            self.dict[k] = self.cnt
            self.cnt += 1
        return self.dict[k]

    def __setitem__(self, k, v):
        raise NotImplementedError("__setitem__ is not supported")

    def __len__(self):
        return len(self.dict)

    def get(self, k):
        return self.__getitem__(k)

    def items(self):
        return self.dict.items()


# A tree data structure which stores a list of degrees and can quickly retrieve the min degree element,
# or modify any of the degrees, each in logarithmic time. It works by creating a binary tree with the 
# given elements in the leaves, where each internal node stores the min of its two children. 
import math
class MinTree:
    def __init__(self, degrees):
        self.height = int(math.ceil(math.log(len(degrees), 2)))
        self.numLeaves = 2 ** self.height
        self.numBranches = self.numLeaves - 1
        self.n = self.numBranches + self.numLeaves
        self.nodes = [float('inf')] * self.n
        for i in range(len(degrees)):
            self.nodes[self.numBranches + i] = degrees[i]
        for i in reversed(list(range(self.numBranches))):
            self.nodes[i] = min(self.nodes[2 * i + 1], self.nodes[2 * i + 2])

    def getMin(self):
        cur = 0
        for i in range(self.height):
            cur = (2 * cur + 1) if self.nodes[2 * cur + 1] <= self.nodes[2 * cur + 2] else (2 * cur + 2)
        # print "found min at %d: %d" % (cur, self.nodes[cur])
        return (cur - self.numBranches, self.nodes[cur])

    def getVal(self, idx):
        return self.nodes[idx+self.numBranches]

    def changeVal(self, idx, delta):
        cur = self.numBranches + idx
        self.nodes[cur] += delta
        for i in range(self.height):
            cur = (cur - 1) // 2
            nextParent = min(self.nodes[2 * cur + 1], self.nodes[2 * cur + 2])
            if self.nodes[cur] == nextParent:
                break
            self.nodes[cur] = nextParent

    def dump(self):
        print("numLeaves: %d, numBranches: %d, n: %d, nodes: " % (self.numLeaves, self.numBranches, self.n))
        cur = 0
        for i in range(self.height + 1):
            for j in range(2 ** i):
                print(self.nodes[cur], end=' ')
                cur += 1
            print('')