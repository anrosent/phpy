#Python Hypertext Preprocessor (Second iteration: Not functional)
#Author: Anson Rosenthal (anrosent)
#10/2013

#Figured out scheme for output capture using ast, but parsing still a pain

import ast, sys

code_start_delim = "<?"
code_stop_delim = "?>"

class TextNode():
    def __init__(self, string):
        self.string = string
        
    def capture_output(self):
        return self.string
        
class CodeNode():
    def __init__(self, string):
        self.string = string
        self.capture = ''
        
    def self_node(self):
        return ast.Name('self')
        
    def write(self, string):
        self.capture += string
    
    def capture_output(self):
        tree = ast.parse(self.string)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if node.func.id == 'print':
                    node.keywords.append(ast.keyword('file',self.self_node()))
        exec(self.string)
        return self.capture

def parse(string):
    nodes = []
    return parse_rec(iter(string.lstrip(code_start_delim)), nodes, string.startswith(code_start_delim))
    
def parse_rec(string_iter, nodes, in_code):
    if in_code:
        nodes.append(get_code_node(string_iter))
    else:
        nodes.append(get_text_node(string_iter))
    return parse_rec(string_iter, nodes, not in_code)
    
def get_code_node(string_iter):
    buf = []
    delim_match = 0
    while delim_match < len(code_stop_delimeter):
        c = string_iter.__next__()
        if c == code_stop_delimeter[delim_match]:
            delim_match += 1
        buf.append(c)
    return ''.join(buf[:-len(code_stop_delimeter)])
    
def get_text_node(string_iter):
    buf = []
    delim_match = 0
    for c in string_iter:
        if c == code_start_delimeter[delim_match]:
            delim_match += 1
        el
        buf.append(c)
    return ''.join(buf[:-len(code_stop_delimeter)])
    
    
    
def parse_full(string):
    return ''.join(node.capture_output() for node in parse(string))
    
if __name__ == '__main__':
    with open(sys.argv[1]) as inputfile:
        print(parse_full(inputfile.read()))