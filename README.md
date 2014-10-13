PHPy
====

Templated dynamic web pages in the style of PHP - you can embed blocks of Python code into your content, and anything ```print```ed from that code block will be injected into the template in its place. 

The motivation here was to do something neat with code execution and ASTs, resulting in a little hack to redirect output from ```print``` into a buffer we can use to render the template and maintain state between code blocks.

## Running
To start serving, run
```
$   ./phpy <port>
```
There are some more args that it accepts (they're the same as ```http.server```).

## Testing
There are a few tests here, which compares the templated output of some prepared pages with the output we expect.
These are under ```tests```, and you can run them as follows.
```
$   ./phpy 9000
$   ./run_tests
```
