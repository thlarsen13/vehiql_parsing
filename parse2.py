from pythonds.basic import Stack
# from pythonds.trees import BinaryTree


# s = '( ( RIGHT(argument1, argument2) AND (ego.something=left_turn OR traffic_light.CONFIDENCE=0.9 ) ) OR t.COLOR=red )'
"""
Query Language Rules: 
There are three syntactic objects: words, parenthesis, and spaces. words & parenthesis must be seperated by parentheses. 
We allow n-ary operators, (AND, OR) and atomic statements. 

"""

# class Node:

#   def __init__(self):
#       self.node_type = "" 
#       self.children = []
#       self.data = ""

class ChristmasTree:
    def __init__(self, root): 
        self.key = root
        self.node_type = "" #TYPES: COMP, FUNCTION, 

        self.children = []

    def insertChild(self,newNode):

        if isinstance(newNode, ChristmasTree):
            t = newNode
        else:
            t = ChristmasTree(newNode)
        # if self.leftChild is not None:
        #     t.leftChild = self.leftChild

        return t


    def print_tree(self, depth = 0):
        print("   "*depth + "+---" + self.key)
        for child in self.children:
            child.print_tree(depth=depth+1)


binary_operators = ["AND", "OR", "LEFT", "RIGHT"]

def buildParseTree(word_list):
    # word_list = query.split() #create list of words 
    pStack = Stack()
    eTree = ChristmasTree('')
    pStack.push(eTree)
    currentTree = eTree

    for word in word_list: 
        if word == '(':
            new_child = currentTree.insertChild('')
            pStack.push(currentTree)
            currentTree = new_child

        elif word in binary_operators:
            currentTree.key = word
            new_child = currentTree.insertChild('')
            pStack.push(currentTree)
            currentTree = new_child

        elif word == ')':
            currentTree = pStack.pop()

        else:
            currentTree.key = word
            parent = pStack.pop()
            currentTree = parent

    return eTree


def find_char(query, word): 
    i = 0
    for q in query: 
        if q == word: 
            return i
        i += 1
    return -1

def find_char_from_back(query, word): 
    i = len(query) - 1
    while i >= 0: 
        if query[i] == word: 
            return i
        i -= 1
    return -1

#input is a LIST of words. inserts parenthesis to make it obvious how to construct the tree 
def resolve_syntax(query, current_op=None): 
    #SOLVE with recursion. 
    # order_of_tightness = ["(", "AND", "OR"] #operations on the left bind the tightest???
    print(query)
    i = find_char(query, "(")
    if i != -1: 
        j = find_char_from_back(query, ")")
        if j == -1 or j < i:
            print("AHHHHHH")
            exit() 
        before = resolve_syntax(query[:i])
        inside = resolve_syntax(query[i+1:j])
        after = resolve_syntax(query[j+1:])
        return before + ["("] + inside + [")"] + after

    for op in ["OR", "AND"]: 

        i = find_char(query, op)
        if i != -1: 
            before = resolve_syntax(query[:i], current_op=op)
            after = resolve_syntax(query[i+1:], current_op=op)
            if current_op == op: 
                return  before + [op] + after
            else:
                return ["("] + before + [op] + after + [")"]
    return query


def RPN_tree(query): 
    # pStack = Stack()
    # eTree = ChristmasTree('')
    # pStack.push(eTree)
    # currentTree = eTree
    priority = {
    "AND" : 0
    "OR" : 1
    }
    operStack = Stack()

    for word in query: 
        if word == '(':
            new_child = currentTree.insertChild('')
            pStack.push(currentTree)
            currentTree = new_child

        elif word in binary_operators: # push onto operator stack 
            op = operStack.top() 
            while op != '(' and priority[op] >  priority[word]: 
                operStack.pop() 
                currentTree.insertChild(queue)
            operStack.push(word)
            

        elif word == ')':
            currentTree = pStack.pop()

        else:
            currentTree.key = word
            parent = pStack.pop()
            currentTree = parent

    return eTree

def sentenceToTree(query): 
    query = query.split() 
    # query = resolve_syntax(query)
    print(query)
    pt = buildParseTree(query)
    pt.print_tree() 
q = '( ( ( argument1 RIGHT argument2 ) AND ( ego.something=left_turn OR traffic_light.CONFIDENCE=0.9 ) AND arg1 ) OR t.COLOR=red )'
# q = "( 1 AND ( ( 2 AND 2.5 ) OR 3 ) ) AND 4"
# q = '( argument1 RIGHT argument2 ) AND ( ego.something=left_turn OR traffic_light.CONFIDENCE=0.9 ) AND arg1 ) OR t.COLOR=red )'

sentenceToTree(q)