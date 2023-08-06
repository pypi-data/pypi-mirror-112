# cmdtools
[![tests](https://github.com/HugeBrain16/cmdtools/actions/workflows/python-package.yml/badge.svg)](https://github.com/HugeBrain16/cmdtools/actions/workflows/python-package.yml)
  
a module for parsing and processing commands.
  
## Installation
to install this module you can use the methods below 
  
- using pip: 
    + from pypi: `pip install cmdtools-py`  
    + from github repository: `pip install git+https://github.com/HugeBrain16/cmdtools.git`  
  
- from source: `python setup.py install`  
  
## Examples
Basic example
```py
import cmdtools

def ping():
    print("pong.")

cmd = cmdtools.Cmd('/ping')

cmd.process_cmd(ping)
```
  
Parse command with arguments
```py
import cmdtools

def greet(name):
    print(f"Hello, {name}, nice to meet you")

cmd = cmdtools.Cmd('/greet "Josh"')

cmd.process_cmd(greet)
```
  
Parsing command with more than one argument and different data types
```py
import cmdtools

def give(name, item_name, item_amount):
    print(f"You gave {item_amount} {item_name}s to {name}")

cmd = cmdtools.Cmd('/give "Josh" "Apple" 10', convert_args=True) # convert command arguments into specific datatypes

# check command
if cmd.match_args('ssi', max_args=3): # format indicates ['str','str','int'], only match 3 arguments
    cmd.process_cmd(give)
else:
    print('Correct Usage: /give <name: [str]> <item-name: [str]> <item-amount: [int]>')
```
  
command with attributes
```py
import cmdtools

def test():
    print(test.text)

cmd = cmdtools.Cmd('/test')

cmd.process_cmd(test,
    attrs={ # assign attributes to the callback
        'text': "Hello World"
    }
)
```
  
command with error handling example

using callback

```py
import cmdtools

def error_add(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == 'num1':
            print('you need to specify the first number')
        if error.param == 'num2':
            print('you need to specify the second number')

def add(num1, num2):
    print(num1 + num2)

cmd = cmdtools.Cmd('/add', convert_args=True)
cmd.process_cmd(add, error_add)
```

or using python error handler

```py
import cmdtools

def add(num1, num2):
    print(num1 + num2)

cmd = cmdtools.Cmd('/add')

try:
    cmd.process_cmd(add)
except Exception as error:
    if isinstance(error.exception, cmdtools.MissingRequiredArgument):
        if error.exception.param == "num1":
            print('you need to specify the first number')
        if error.exception.param == "num2":
            print('you need to specify the second number')
```
  
asynchronous support
```py
import cmdtools
import asyncio

async def _say(text):
    print(text)

async def main():
    cmd = cmdtools.Cmd('/say "Hello World"')

    await cmd.aio_process_cmd(_say)

asyncio.run(main())
```
  
## Exceptions
- ParsingError
- MissingRequiredArgument
- ProcessError