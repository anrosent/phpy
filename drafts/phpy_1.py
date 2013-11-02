#Python Hypertext Preprocessor (First iteration: Not functional)
#Author: Anson Rosenthal (anrosent)
#10/2013

import sys

#next move is to make print statements redirect to capture print output in node
#   using AST
# also clean up parser

class ParseNode():
    def __init__(self, string, first, delim):
        buf = [first]
        for c in string:
            if c == delim:
                break
            buf.append(c)
        self.string = ''.join(buf)

    def generate(self):
        pass
        
class Text(ParseNode):
    def __init__(self, string, first, delim):
        ParseNode.__init__(self, string, first, delim)
        
    def generate(self):
        return self.string
        
class Code(ParseNode):
    def __init__(self, string, first, delim):
        ParseNode.__init__(self, string, first, delim)
        
    def generate(self):
        return str(eval(self.string))

class PyHPP():
    def __init__(self):
        self.buffer = None
        self.parse_seq = []
        self.delim = '#'
        self.in_code = False
        self.done = False
    
    def parse_full(self, string):
        nodes = []
        self.in_code = string[0] != self.delim
        self.buffer = iter(string)
        for c in self.buffer:
            if self.in_code:
                nodes.append(Text(self.buffer, c, self.delim))
            else:
                nodes.append(Code(self.buffer, c, self.delim))
            self.in_code = not self.in_code
            
        return ''.join(map(lambda node:node.generate(), nodes))
            
    # def advance(self):
        # self.buffer.__next__()
    
    # def parse(self,string):
        # splits = string.split(self.delim)
        # text_first = int((string[0] != self.delim))
        # splits[text_first::2] = map(str, map(eval, splits[text_first::2]))
        # return ''.join(splits)
        
if __name__ == '__main__':
    with open(sys.argv[1]) as inputfile:
        a = PyHPP()
        print(a.parse_full(inputfile.read()))
        