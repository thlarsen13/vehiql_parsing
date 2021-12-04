from pythonds.basic import Stack
# from pythonds.trees import BinaryTree


# s = '( ( RIGHT(argument1, argument2) AND (ego.something=left_turn OR traffic_light.CONFIDENCE=0.9 ) ) OR t.COLOR=red )'
"""
Query Language Rules: 
There are three syntactic objects: words, parenthesis, and spaces. words & parenthesis must be seperated by parentheses. 
We allow n-ary operators, (AND, OR) and atomic statements. 

"""

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

        return t


    def print_tree(self, depth = 0):
        print("   "*depth + "+---" + self.key)
        for child in self.children:
            child.print_tree(depth=depth+1)


binary_operators = ["AND", "OR"]


def find_close(query, i): 
    j = i + 1 
    count = 1 
    while count > 0: 
        if j > len(query): 
            print("oops, no ) found for ( at position i = " + str(i) + " in:")
            print(query)
            exit() 
        if query[j] == '(': 
            count += 1 
        elif query[j] == ')': 
            count -= 1 
        j += 1 
    return j - 1


class treeMaker(): 
    def __init__(self, query ): 
        # pStack = Stack()
        # eTree = ChristmasTree('')
        # pStack.push(eTree)
        # currentTree = eTree
        self.priority = {
        "AND" : 1,
        "OR" : 0
        }
        self.operStack = Stack()
        self.treeStack = Stack()
        self.query = query

    def makeTree(self):
        i = 0
        while i < len(self.query):
            word = self.query[i] 
            print(word)
            
            if word in binary_operators: 
                if (self.operStack.size() > 0) and self.priority[self.operStack.peek()] > self.priority[word]: 
                #we have a tighter op, so we put all of those into a tree 
                    self.pop_op() 

                self.operStack.push(word)

            elif word == "(": #recurse into the parenthesis, add a tree 
                j = find_close(self.query, i)
                if j < i: 
                    print(self.query)
                    print(i, j)
                    print("unmatched (, AHHHH")
                    exit() 
                tM = treeMaker(self.query[i + 1 : j]) 
                newTree = tM.makeTree()
                # recurse into parenthesis, make tree, add it to the stack
                self.treeStack.push(newTree)
                i = j 

            else: #insert a new word 
                self.treeStack.push(ChristmasTree(word))
            i += 1

        while self.operStack.size() > 0: 
            self.pop_op() 
        ### check operStack is empty, and treeStack has only one tree 
        t = self.treeStack.pop() 
        assert self.treeStack.size() == 0
        return t 

    def pop_op(self): 
        op = self.operStack.pop()

        newTree = ChristmasTree(op)

        c1 = self.treeStack.pop() 
        newTree.children.append(c1)
        # print("\n---c1---")
        # c1.print_tree()

        while (self.operStack.size() > 0) and self.operStack.peek() == op: 
          self.operStack.pop()
          ci = self.treeStack.pop()
          newTree.children.append(ci)
          # print("\n---ci---")
          # ci.print_tree()

        c2 = self.treeStack.pop() 
        newTree.children.append(c2)
        # print("---c2---")
        # c2.print_tree()

        self.treeStack.push(newTree)


def sentenceToTree(query): 
    query = query.split() 
    # query = resolve_syntax(query)
    # print(query)
    # pt = buildParseTree(query)
    tM = treeMaker(query)
    pt = tM.makeTree()
    print("\n FINAL TREE \n")
    pt.print_tree() 
# q = '( ( ( RIGHTargument1,argument2 ) AND ( ego.something=left_turn OR traffic_light.CONFIDENCE=0.9 ) AND arg1 ) OR t.COLOR=red )'
# q = "1 AND 2 AND 2.5 OR 3 AND 4"
q = '( ego.something=left_turn OR traffic_light.CONFIDENCE=0.9 ) AND ( arg1 OR t.COLOR=red ) OR 1 OR 3'

sentenceToTree(q)
