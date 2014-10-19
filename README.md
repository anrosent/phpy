PHPy
====

Templated dynamic web pages in the style of PHP - you can embed blocks of Python code into your content, and anything ```print```ed from that code block will be injected into the template in its place. 

The motivation here was to do something neat with code execution and ASTs, resulting in a little hack to redirect output from ```print``` into a buffer we can use to render the template and maintain state between code blocks.

### Request variables
In the style of PHP or the environment passed to CGI scripts, the variables ```_GET```, ```_POST```, and ```_COOKIES``` in the execution scope of the code blocks are populated with the appropriate data from the HTTP request being handled:

 - ```_GET``` is a multimap associating query string keys to a list containing all the values they are given in the query string.
 - ```_POST``` is a string containing the body data of POST requests.
 - ```_COOKIES``` is a ```http.cookies.SimpleCookie``` loaded with all ```Cookie``` header parameters



## Running the Server
To start serving, run
```
$   ./phpy <port>
```
There are some more args that it accepts (they're the same as ```http.server```).


## Examples

Let's first start our server.
```
$	./phpy 8000
```
####```_GET```

Here's an example PHPy template:
```
# hello.html

<html>
	<p> Hello, <? print(' and'.join(_GET.get('name', []))) ?>! </p>
</html>
```
The template is rendered to greet us and our friends when we access the page!
```
$	curl 'localhost:8000/examples/vartest.html?name=Anson&name=Friend'

<html>
    <p> Hello, Anson and Friend </p>
</html>
```

####```_POST```
We can process POSTs to our service containing JSON data as well!
```
# json.html
<? import json ?>
<? 

# Parse POST data as JSON
data = json.loads(_POST)

# Extract names from data if present
names = data.get('names', [])

?>

<html>
	<p> Hello, <? print( ' and '.join(names) ) ?>! </p>
</html>
```
Requesting this page via POST yields the same behavior as before.

```
$	curl 'localhost:8000/examples/json.html' -d '{"names": ["Anson", "Friend"]}'

<html>
        <p> Hello, Anson and Friend! </p>
</html>
```


## Testing
There are a few tests here, which compares the templated output of some prepared pages with the output we expect.
These are under ```tests```, and you can run them as follows.
```
$   ./phpy <port>
$   ./run_tests <port>
```

## TODO
As usual, several TODOs here.
 - Hook into ```SimpleHTTPServer```'s HTTP status code checks, e.g. 404 if file isn't on disk. In overriding some handlers I coded around this path, so server responds with nothing whenever error is hit, rather than HTTP error code. 
 - Figure out semantics of whitespace around silent code blocks on their own line - looks ugly if there's a lingering newline from each of them.
 - Python's semantic whitespace causes some friction in embedding code in the blocks over multiple lines. Maybe some way to reindent so we can pull multiline code blocks inside by a tab for readability. 
 - More official module loading system - add ```modules``` directory to ```sys.path``` in execution scope
 - Some way of specifying templated assets directory so we can restrict served files to a given directory
