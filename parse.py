from pythonds.basic import Stack
# from pythonds.trees import BinaryTree


# s = '( ( RIGHT(argument1, argument2) AND (ego.something=left_turn OR traffic_light.CONFIDENCE=0.9 ) ) OR t.COLOR=red )'
"""
Query Language Rules: 
There are three syntactic objects: words, parenthesis, and spaces. words & parenthesis must be seperated by parentheses. 
We only allow BINARY operators, and atomic statements. 

"""

# class Node:

#   def __init__(self):
#       self.node_type = "" 
#       self.children = []
#       self.data = ""

class BinaryTree:
    def __init__(self, root): 
        self.key = root
        self.node_type = "" #TYPES: COMP, FUNCTION, 

        self.leftChild = None
        self.rightChild = None
        # self.children = []

    def insertLeft(self,newNode):

        if isinstance(newNode, BinaryTree):
            t = newNode
        else:
            t = BinaryTree(newNode)

        if self.leftChild is not None:
            t.leftChild = self.leftChild

        self.leftChild = t

    def insertRight(self,newNode):
        if isinstance(newNode,BinaryTree):
            t = newNode
        else:
            t = BinaryTree(newNode)

        if self.rightChild is not None:
            t.rightChild = self.rightChild
        self.rightChild = t

    def print_tree(self, depth = 0):
        print("  "*depth + "+--" + self.key)
        if self.leftChild:
            self.leftChild.print_tree(depth=depth+1)
        if self.rightChild:
            self.rightChild.print_tree(depth=depth+1)

binary_operators = ["AND", "OR", "LEFT", "RIGHT"]

def buildParseTree(query):
    word_list = query.split() #create list of words 
    pStack = Stack()
    eTree = BinaryTree('')
    pStack.push(eTree)
    currentTree = eTree

    for word in word_list: 
        if word == '(':
            currentTree.insertLeft('')
            pStack.push(currentTree)
            currentTree = currentTree.leftChild

        elif word in binary_operators:
            currentTree.key = word
            currentTree.insertRight('')
            pStack.push(currentTree)
            currentTree = currentTree.rightChild

        elif word == ')':
            currentTree = pStack.pop()

        elif word not in binary_operators + ['/', ')']:
            currentTree.key = word
            parent = pStack.pop()
            currentTree = parent

    return eTree

s = '( ( ( argument1 RIGHT argument2 ) AND ( ego.something=left_turn OR traffic_light.CONFIDENCE=0.9 ) ) OR t.COLOR=red )'
t = '( ( ( ( argument1 RIGHT argument2 ) AND ( ego.something=left_turn OR t.CONFIDENCE=0.9 ) ) OR t.COLOR=red ) AND t.class=traffic_light )'
q = "( ( 10 AND 5 ) OR 3 )"
pt = buildParseTree(s)
pt.print_tree() 