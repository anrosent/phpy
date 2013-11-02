#!/usr/bin/env python
#Python Hypertext Preprocessor: PHPy
#Author: Anson Rosenthal (anrosent)
#10/2013

#3rd and final iteration. Regex sub >> parsing it yourself when structure is so simple!
import re, sys, ast

#Delimiters of code elements
code_start = "<?"
code_stop = "?>"

#Compile regex to find code elements to be executed
find_code = re.compile("%s(.*?)%s"%(re.escape(code_start), re.escape(code_stop)), re.DOTALL | re.MULTILINE)

#Class to execute code and capture output from print statements - the idea is to mirror PHP's echo
class CaptureBuffer():
    def __init__(self):
        self.string = ''
        self.capture = ''
        self.var_dict = {'output_buffer':self}
        
    def add(self, string):
        self.string = string
        self.capture = ''
        
    #Implement file writing interface so calls to 'print' can be redirected to buffer
    def write(self, string):
        self.capture += string
        
    def fake_node_pos(self, node):
        node.lineno = 0
        node.col_offset = 0
        return node
        
    def self_node(self):
        return self.fake_node_pos(ast.Name('output_buffer', ast.Load()))
    
    def str_node(self):
        return self.fake_node_pos(ast.Str(''))
    
    def get_print_keywords(self):
        return [ast.keyword('file',self.self_node()), ast.keyword('end', self.str_node())]
    
    #Transform all calls to 'print' to redirect from stdout to buffer, then execute code and return
    #captured output
    def capture_output(self):
        tree = ast.parse(self.string)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if node.func.id == 'print':
                    node.keywords.extend(self.get_print_keywords())
        exec(compile(tree, '<string>', 'exec'), self.var_dict)
        self.string = ''
        return self.capture
    
capture_buf = CaptureBuffer()    
    
#For each match, replace it with its output    
def process(string):
    return find_code.sub(capture_output, string)

#Captures output of each matched code element to be substituted for matched text    
def capture_output(match):
    contents = match.groups()[0].strip()
    capture_buf.add(contents)
    return capture_buf.capture_output()
    
#Runs transformation on input file and prints result to stdout
#Usage: python phpy.py [input file]
#   if no input file specified, reads from stdin and prints result to stdout    
#   FEATURE NOTE: single-pass parse and evaluate INSTEAD OF full read and store, then eval and replace
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(process(''.join(sys.stdin.readlines())))
    elif len(sys.argv) == 2:
        with open(sys.argv[1]) as inputfile:
            print(process(inputfile.read()))
    else:
        print("Usage: python phpy.py [input_file]")
    