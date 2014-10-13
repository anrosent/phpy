#!/usr/bin/env python3

import re, sys, ast, fileinput

#Delimiters of code elements
code_start = "<?"
code_stop = "?>"

#Compile regex to find code elements to be executed
find_code = re.compile("%s(.*?)%s"%(re.escape(code_start), re.escape(code_stop)), re.DOTALL | re.MULTILINE)

#Class to execute code and capture output from print statements - the idea is to mirror PHP's echo
class CaptureBuffer():

    # Init with dict to save state between code blocks and self to capture printed output
    def __init__(self):
        self.string = ''
        self.capture = ''
        self.var_dict = {'output_buffer':self}
        
    # Adds new code block into buffer
    def add(self, string):
        self.string = string
        self.capture = ''
        
    # Implement file writing interface so calls to 'print' can be redirected to buffer
    def write(self, string):
        if self.capture:
            self.capture += string
        else:
            self.capture += string
        
    # Sets the params we don't really care about of an AST node we inject
    def fake_node_pos(self, node):
        node.lineno = 0
        node.col_offset = 0
        return node
        
    # Return AST node containing name ref to this buffer
    def self_node(self):
        return self.fake_node_pos(ast.Name('output_buffer', ast.Load()))
    
    # Return empty string AST node
    def str_node(self):
        return self.fake_node_pos(ast.Str(''))
    
    # Returns keyword args we inject into print calls
    def get_print_keywords(self):
        return [ast.keyword('file',self.self_node()), ast.keyword('end', self.str_node())]
    
    #Transform all calls to 'print' to redirect from stdout to buffer, then execute code and return
    #captured output
    def capture_output(self):
        tree = ast.parse(self.string)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):

                # If this node is a call to print(), set the output file to this buffer
                if node.func.id == 'print':
                    node.keywords.extend(self.get_print_keywords())

        # Execute code block with same local state as other code blocks
        exec(compile(tree, '<string>', 'exec'), self.var_dict)

        # Reset buffer
        self.string = ''

        # Return captured output
        return self.capture.strip() + '' if self.capture else ''
    
    
#For each match, replace it with its output    
def process(string):
    
    # Init a buffer
    capture_buf = CaptureBuffer()    

    # Find and replace all code blocks with their output
    #
    # Note that this replacment is done in sequence by sub(), so we can rely on sequential
    # execution of our code blocks
    return find_code.sub(output_capturer(capture_buf), string)

#Captures output of each matched code element to be substituted for matched text    
def output_capturer(buf):

    def capture(match):
        # Get code block text
        contents = match.groups()[0].strip()

        # Add code to buffer
        buf.add(contents)

        # Execute and return captured output
        return buf.capture_output()

    # Return closure over buffer
    return capture

#Runs transformation on input file and prints result to stdout
#Usage: python phpy.py [input file]
#   if no input file specified, reads from stdin and prints result to stdout    
if __name__ == '__main__':
    print(process(''.join(fileinput.input())))
