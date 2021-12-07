from pythonds.basic import Stack


"""
Query Language Rules: 
There are two syntactic "words": functions and parenthesis. Anything not seperated by spaces will be treated as its own "word".  
We create a tree, with leaf nodes being functions, and everything else being AND/OR, according to SQL order of operations. 

"""

#like a Binary Tree but nodes can have multiple children
class ChristmasTree:
    def __init__(self, root): 

        self.logical_operators = ["AND", "OR"]
        self.function_symbols = ["LEFT", "RIGHT", "BEFORE", "AFTER"]
        self.comp_operators = ["<", ">", "="]

        self.key = root
        self.node_type = "" #TYPES: COMP, FUNCTION. TODO: keep track of this. 
        self.children = []

        #only used for comparison type 
        self.var = None #"ego"
        self.attr = None #"speed"
        self.comp_operator = None # < 
        self.target = None # 30 (mph)

        #only used for function types
        self.function = self.isFunctionSym()
        self.args = None


        if self.key in self.logical_operators:
            self.node_type = "LOGICAL_OPERATOR"
        elif self.function is not None: 
            self.node_type = "FUNCTION"
            L = len(self.function)
            rest = self.key[L+1:-1]
            self.args = rest.split(",")

        elif "." in self.key: 
            self.node_type = "COMPARISON"

            self.var = self.key.split(".")[0]
            rest = self.key.split(".")[1]

            found = False
            for op in self.comp_operators: 
                if op in rest: 
                    if found:
                        print("oops: multiple comp ops found")
                        print("exit")
                    i = rest.index(op)
                    self.attr = rest[:i]            
                    self.comp_operator = op
                    self.target = rest[i+1:]
                    found = True 
        else: 
            print(f"ERROR, {self.key} not recognized")
            exit()

    def isFunctionSym(self): 
        for sym in self.function_symbols: 
            if self.key[:len(sym)] == sym: 
                return sym 
        return None


    def insertChild(self,newNode): 

        if isinstance(newNode, ChristmasTree):
            t = newNode
        else:
            t = ChristmasTree(newNode)

        return t


    def print_tree(self, depth = 0):
        verbose = False 
        if depth == 0: 
            print(self.key)
        else: 
            print("     "*(depth-1) + "+--- " + self.key)
        if verbose and self.node_type == "COMPARISON": 
            print("     "*(depth) + f"var: {self.var}, attr: {self.attr}, op: {self.comp_operator}, target: {self.target}")
        if verbose and self.node_type == "FUNCTION": 
            print("     "*(depth) + f"function: {self.function}, args: {self.args}")
        for child in self.children:
            child.print_tree(depth=depth+1)



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


class ChristmasTreeFarmer(): 
    def __init__(self, query ): 
        self.priority = {
        "AND" : 1,
        "OR" : 0
        }
        self.operStack = Stack()
        self.treeStack = Stack()
        self.query = query

        self.logical_operators = ["AND", "OR"]


    def makeTree(self):
        i = 0
        while i < len(self.query):
            word = self.query[i] 

            if word in self.logical_operators: 
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
                tM = ChristmasTreeFarmer(self.query[i + 1 : j]) 
                newTree = tM.makeTree()
                # recurse into parenthesis, make tree, add it to the stack
                self.treeStack.push(newTree)
                i = j 
                #we recursively processed i->j, so skip ahead to the rest of the string

            else: #insert a new word 
                self.treeStack.push(ChristmasTree(word))
            i += 1

        while self.operStack.size() > 0: 
            self.pop_op() 
        ### check operStack is empty, and treeStack has only one tree 
        t = self.treeStack.pop() 
        if self.treeStack.size() != 0: 
            print("Error: operations have mismatched number of args (or I have a bug)")
            exit()
        return t 

    def pop_op(self): 
        op = self.operStack.pop()

        newTree = ChristmasTree(op)

        c1 = self.treeStack.pop() 
        newTree.children.append(c1)

        while (self.operStack.size() > 0) and self.operStack.peek() == op: 
          self.operStack.pop()
          ci = self.treeStack.pop()
          newTree.children.append(ci)

        c2 = self.treeStack.pop() 
        newTree.children.append(c2)

        self.treeStack.push(newTree)


def sentenceToTree(query): 
    query = query.split() 
    # query = resolve_syntax(query)
    # print(query)
    # pt = buildParseTree(query)
    tM = ChristmasTreeFarmer(query)
    pt = tM.makeTree()
    print("\nFINAL TREE\n")
    pt.print_tree() 

# q = '( ( ( RIGHTargument1,argument2 ) AND ( ego.something=left_turn OR traffic_light.CONFIDENCE=0.9 ) AND arg1 ) OR t.COLOR=red )'
# q = "1 AND 2 AND 2.5 OR 3 AND 4 OR 5"
q = 'taylor.hair=curly OR ( ego.something=left_turn OR traffic_light.CONFIDENCE=0.9 ) AND ( t.COLOR=green OR t.COLOR=red ) OR RIGHT(ego,traffic_light)'
print('Query parsed: ' + q)

sentenceToTree(q)